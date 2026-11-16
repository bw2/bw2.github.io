"""Fetch the usage numbers shown on the projects page and save them to project_usage_counts.json.

projects.md marks each number with a placeholder, and generate_html.py fills the placeholders in from
project_usage_counts.json when it renders projects.html. This script finds the placeholders in projects.md and
fetches the current value of each one:

    {{github_stars:OWNER/REPO}}            the repo's star count, from the GitHub REST API
    {{google_scholar_citations:TITLE}}     "Cited by" count and link of the paper with this title, read from the
                                           Google Scholar profile page below
    {{weekly_visitors:WEBSITE}}            the website's Google Analytics active users per week, averaged over the
                                           last 12 full weeks (Monday to Sunday)

If a value can't be fetched, it prints a warning and keeps the value saved by the previous run, so a failure never
blocks publishing.

It only reads. Google Analytics is queried with the read-only scope, so the script can't change any property's
settings, and Google Scholar is read only through the profile page, which Scholar's robots.txt lets scripts read.

It runs every week in GitHub Actions (.github/workflows/update_project_usage_counts.yml), which signs in to Google as
the robot account (service account) bw2-github-io-usage-counts@cmg-analysis.iam.gserviceaccount.com without any
stored key. That account has no Google Cloud roles. It can read a website's visitor counts only after someone adds it
as a Viewer in that website's Google Analytics property (Admin > Property access management). cmg-analysis must have
analyticsdata.googleapis.com enabled.

Usage, from the repo root (update_pages.sh also runs this before generate_html.py):
    python3 scripts/fetch_project_usage_counts.py
"""

import datetime
import html
import json
import os
import re
import urllib.request

PROJECTS_MARKDOWN_PATH = "projects.md"
PROJECT_USAGE_COUNTS_PATH = "project_usage_counts.json"

# pagesize=100 lists every paper on the first page. Scholar's robots.txt allows /citations?user= pages, but not
# paging through them with cstart=.
GOOGLE_SCHOLAR_PROFILE_URL = "https://scholar.google.com/citations?user=OWObMaoAAAAJ&hl=en&pagesize=100"

# The Google Analytics 4 property ID of each website (in Google Analytics: Admin > Property details).
GOOGLE_ANALYTICS_PROPERTY_ID_BY_WEBSITE = {
    "trexplorer.broadinstitute.org": "495559599",
    "seqr.broadinstitute.org": "371440737",
    "spliceailookup.broadinstitute.org": "354221379",
    "genelookup.broadinstitute.org": "535286382",
    "liftover.broadinstitute.org": "253463776",
}

NUMBER_OF_WEEKS_TO_AVERAGE = 12

# Google Scholar turns away requests that don't look like they come from a browser.
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36")

PLACEHOLDER_REGEX = re.compile(r"\{\{(github_stars|google_scholar_citations|weekly_visitors):([^}]+)\}\}")


def find_placeholders(markdown_text):
    """Find the usage count placeholders in a Markdown page.

    Args:
        markdown_text: text of the Markdown page.

    Returns:
        list of (kind, key) tuples, e.g. ("github_stars", "broadinstitute/seqr"), in order of first appearance,
        without repeats.
    """
    return list(dict.fromkeys((kind, key.strip()) for kind, key in PLACEHOLDER_REGEX.findall(markdown_text)))


def load_project_usage_counts(path=PROJECT_USAGE_COUNTS_PATH):
    """Load the counts saved by the previous run, or return an empty dict if there's no saved file yet."""
    if not os.path.isfile(path):
        return {}
    with open(path, "rt") as f:
        return json.load(f)


def download_text(url, user_agent, extra_headers=None):
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, **(extra_headers or {})})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def fetch_github_star_count(repo):
    """Return the star count of the GitHub repo "OWNER/REPO"."""
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        # GitHub Actions sets this. Without it, all requests from GitHub's shared servers count against one small limit
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    repo_info_json = download_text(f"https://api.github.com/repos/{repo}", "project-usage-counts-script", headers)
    return json.loads(repo_info_json)["stargazers_count"]


def normalize_paper_title(title):
    """Lowercase the title and keep only letters and digits, so that different hyphen or quote characters don't
    prevent a match (Scholar writes "web‐based" with a Unicode hyphen, for example)."""
    return re.sub(r"[^a-z0-9]", "", title.lower())


def parse_google_scholar_profile_page(page_html):
    """Read each paper's "Cited by" count and link from a Google Scholar profile page.

    Args:
        page_html: HTML of the profile page.

    Returns:
        dict that maps each paper's normalized title (see normalize_paper_title) to a dict with "count" and
        "cited_by_url" ("cited_by_url" is None for a paper with no citations). When two papers have the same title,
        keeps the one with more citations.
    """
    citations_by_normalized_title = {}
    for row_html in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page_html, re.DOTALL):
        title_match = re.search(r'class="gsc_a_at">(.*?)</a>', row_html, re.DOTALL)
        if not title_match:
            continue
        title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1)))  # drops formatting like <i>seqr</i>
        count_match = re.search(r'class="gsc_a_ac[^"]*"[^>]*>([0-9]*)</a>', row_html)
        count = int(count_match.group(1)) if count_match and count_match.group(1) else 0
        # Scholar sometimes merges several versions of a paper (e.g. the preprint), and then lists all their IDs
        cluster_ids_match = re.search(r"cites=([0-9,]+)", row_html)
        normalized_title = normalize_paper_title(title)
        previously_found = citations_by_normalized_title.get(normalized_title)
        if previously_found is None or count > previously_found["count"]:
            citations_by_normalized_title[normalized_title] = {
                "count": count,
                "cited_by_url": f"https://scholar.google.com/scholar?cites={cluster_ids_match.group(1)}"
                                if cluster_ids_match else None,
            }
    return citations_by_normalized_title


def fetch_google_scholar_citations_by_normalized_title():
    """Load the Google Scholar profile page once and return parse_google_scholar_profile_page's result for it."""
    citations_by_normalized_title = parse_google_scholar_profile_page(
        download_text(GOOGLE_SCHOLAR_PROFILE_URL, BROWSER_USER_AGENT))
    if not citations_by_normalized_title:
        raise ValueError("found no papers on the Google Scholar profile page (Scholar may have asked for a CAPTCHA)")
    return citations_by_normalized_title


def get_date_range_of_last_full_weeks(today, number_of_weeks):
    """Return the (first Monday, last Sunday) of the last `number_of_weeks` full weeks before `today`."""
    last_sunday = today - datetime.timedelta(days=today.isoweekday())  # isoweekday() is 1 on Monday, 7 on Sunday
    first_monday = last_sunday - datetime.timedelta(days=7 * number_of_weeks - 1)
    return first_monday, last_sunday


def create_google_analytics_session():
    """Return an HTTP session that sends requests with the default Google login, using only the read-only Analytics
    scope. In GitHub Actions, that login is the robot account described at the top of this file.
    """
    import google.auth  # imported here so that generate_html.py, which imports this module, doesn't need it
    import google.auth.transport.requests
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/analytics.readonly"])
    return google.auth.transport.requests.AuthorizedSession(credentials)


def fetch_average_weekly_active_users(google_analytics_session, property_id, first_monday, last_sunday):
    """Return a Google Analytics property's active users per week, averaged over the weeks in the date range.

    Args:
        google_analytics_session: session from create_google_analytics_session().
        property_id: the Google Analytics 4 property ID.
        first_monday: datetime.date of the first day of the first week.
        last_sunday: datetime.date of the last day of the last week.

    Returns:
        the average, rounded to the nearest integer. Weeks with no visitors count as 0.
    """
    response = google_analytics_session.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport",
        json={
            "dateRanges": [{"startDate": first_monday.isoformat(), "endDate": last_sunday.isoformat()}],
            "dimensions": [{"name": "isoYearIsoWeek"}],
            "metrics": [{"name": "activeUsers"}],
        },
        timeout=60)
    if not response.ok:
        raise RuntimeError(f"Google Analytics returned HTTP {response.status_code}: {response.text[:500]}")
    number_of_weeks = ((last_sunday - first_monday).days + 1) // 7
    weekly_active_users = [int(row["metricValues"][0]["value"]) for row in response.json().get("rows", [])]
    return round(sum(weekly_active_users) / number_of_weeks)


def fill_in_project_usage_count_placeholders(markdown_text, project_usage_counts):
    """Replace each placeholder with its saved count, written as Markdown.

    Args:
        markdown_text: text of a Markdown page that may contain placeholders.
        project_usage_counts: dict loaded from project_usage_counts.json.

    Returns:
        the text with each placeholder replaced. A placeholder with no saved count is shown as "??", and a warning
        is printed.
    """
    def format_placeholder(match):
        kind, key = match.group(1), match.group(2).strip()
        saved = project_usage_counts.get(kind, {}).get(key)
        if saved is None:
            print(f"WARNING: no saved {kind} count for {key}, so showing ?? (run scripts/fetch_project_usage_counts.py)")
        count = f"{saved['count']:,}" if saved else "??"
        if kind == "github_stars":
            return f"[{count} GitHub {'star' if count == '1' else 'stars'}](https://github.com/{key}/stargazers)"
        if kind == "google_scholar_citations":
            citations = f"{count} {'citation' if count == '1' else 'citations'}"
            return f"[{citations}]({saved['cited_by_url']})" if saved and saved["cited_by_url"] else citations
        return f"{count} weekly visitors"

    return PLACEHOLDER_REGEX.sub(format_placeholder, markdown_text)


def main():
    with open(PROJECTS_MARKDOWN_PATH, "rt") as f:
        placeholders = find_placeholders(f.read())
    previous_project_usage_counts = load_project_usage_counts()
    today = datetime.date.today()
    first_monday, last_sunday = get_date_range_of_last_full_weeks(today, NUMBER_OF_WEEKS_TO_AVERAGE)
    kinds_of_placeholders = {kind for kind, _ in placeholders}

    # Load the Scholar profile page and sign in to Google Analytics once, up front, so that a failure is reported
    # for each affected placeholder without retrying the same request for each of them
    google_scholar_citations, google_scholar_error = {}, None
    if "google_scholar_citations" in kinds_of_placeholders:
        try:
            google_scholar_citations = fetch_google_scholar_citations_by_normalized_title()
        except Exception as e:
            google_scholar_error = e
    google_analytics_session, google_analytics_error = None, None
    if "weekly_visitors" in kinds_of_placeholders:
        try:
            google_analytics_session = create_google_analytics_session()
        except Exception as e:
            google_analytics_error = e

    project_usage_counts = {}
    number_of_values_kept_from_previous_run = 0
    for kind, key in placeholders:
        try:
            if kind == "github_stars":
                fetched = {"count": fetch_github_star_count(key)}
            elif kind == "google_scholar_citations":
                if google_scholar_error:
                    raise google_scholar_error
                if normalize_paper_title(key) not in google_scholar_citations:
                    raise ValueError("no paper with this title on the Google Scholar profile page")
                fetched = dict(google_scholar_citations[normalize_paper_title(key)])
            else:
                if google_analytics_error:
                    raise google_analytics_error
                if key not in GOOGLE_ANALYTICS_PROPERTY_ID_BY_WEBSITE:
                    raise ValueError("this website has no property ID in GOOGLE_ANALYTICS_PROPERTY_ID_BY_WEBSITE")
                fetched = {"count": fetch_average_weekly_active_users(
                    google_analytics_session, GOOGLE_ANALYTICS_PROPERTY_ID_BY_WEBSITE[key], first_monday, last_sunday)}
        except Exception as e:
            previous = previous_project_usage_counts.get(kind, {}).get(key)
            print(f"WARNING: couldn't fetch {kind} for {key}: {e}")
            if previous is not None:
                print(f"    keeping the value from {previous['fetched_on']}: {previous['count']:,}")
                project_usage_counts.setdefault(kind, {})[key] = previous
                number_of_values_kept_from_previous_run += 1
            continue
        fetched["fetched_on"] = today.isoformat()
        project_usage_counts.setdefault(kind, {})[key] = fetched
        print(f"{kind:25} {fetched['count']:>8,}  {key}")

    with open(PROJECT_USAGE_COUNTS_PATH, "wt") as f:
        json.dump(project_usage_counts, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")

    number_of_values_saved = sum(len(counts_by_key) for counts_by_key in project_usage_counts.values())
    print(f"Saved {number_of_values_saved} of {len(placeholders)} values to {PROJECT_USAGE_COUNTS_PATH} "
          f"({number_of_values_kept_from_previous_run} kept from the previous run). Weekly visitors are averaged "
          f"over {first_monday} to {last_sunday}.")


if __name__ == "__main__":
    main()
