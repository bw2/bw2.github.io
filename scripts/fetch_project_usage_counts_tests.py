"""Tests for fetch_project_usage_counts.py. Run from the scripts directory:

    python3 -m unittest fetch_project_usage_counts_tests
"""

import datetime
import unittest

from fetch_project_usage_counts import (
    fill_in_project_usage_count_placeholders,
    find_placeholders,
    get_date_range_of_last_full_weeks,
    normalize_paper_title,
    parse_google_scholar_profile_page,
)

# rows in the format of a Google Scholar profile page, including a title with <i> formatting and a Unicode hyphen,
# a paper with no citations, a merged paper with two cluster IDs, and two papers with the same title
GOOGLE_SCHOLAR_PROFILE_PAGE_HTML = """
<table><tbody id="gsc_a_b">
<tr class="gsc_a_tr"><td class="gsc_a_t"><a href="/citations?view_op=view_citation" class="gsc_a_at"><i>seqr</i>: A web‐based analysis tool</a></td>
<td class="gsc_a_c"><a href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;cites=2764357361710126723" class="gsc_a_ac gs_ibl">149</a></td></tr>
<tr class="gsc_a_tr"><td class="gsc_a_t"><a href="/citations?view_op=view_citation" class="gsc_a_at">Diagnosing missed cases</a></td>
<td class="gsc_a_c"><a href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;cites=9736194330297635545,15246350528695278218" class="gsc_a_ac gs_ibl">12</a></td></tr>
<tr class="gsc_a_tr"><td class="gsc_a_t"><a href="/citations?view_op=view_citation" class="gsc_a_at">A paper nobody cited</a></td>
<td class="gsc_a_c"><a href="javascript:void(0)" class="gsc_a_ac gs_ibl gsc_a_acm"></a></td></tr>
<tr class="gsc_a_tr"><td class="gsc_a_t"><a href="/citations?view_op=view_citation" class="gsc_a_at">REViewer</a></td>
<td class="gsc_a_c"><a href="javascript:void(0)" class="gsc_a_ac gs_ibl gsc_a_acm"></a></td></tr>
<tr class="gsc_a_tr"><td class="gsc_a_t"><a href="/citations?view_op=view_citation" class="gsc_a_at">REViewer</a></td>
<td class="gsc_a_c"><a href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;cites=9920225529052595829" class="gsc_a_ac gs_ibl">80</a></td></tr>
</tbody></table>
"""


class FindPlaceholdersTests(unittest.TestCase):

    def test_finds_each_kind_once_and_keeps_colons_in_titles(self):
        markdown_text = (
            "{{weekly_visitors:seqr.broadinstitute.org}}, {{github_stars:broadinstitute/seqr}}, "
            "{{google_scholar_citations:seqr: A web-based analysis tool}}\n"
            "{{github_stars:broadinstitute/seqr}} {{not_a_placeholder:x}}")
        self.assertEqual(find_placeholders(markdown_text), [
            ("weekly_visitors", "seqr.broadinstitute.org"),
            ("github_stars", "broadinstitute/seqr"),
            ("google_scholar_citations", "seqr: A web-based analysis tool"),
        ])


class ParseGoogleScholarProfilePageTests(unittest.TestCase):

    def setUp(self):
        self.citations = parse_google_scholar_profile_page(GOOGLE_SCHOLAR_PROFILE_PAGE_HTML)

    def test_matches_titles_despite_formatting_and_hyphen_characters(self):
        self.assertEqual(self.citations[normalize_paper_title("seqr: A web-based analysis tool")], {
            "count": 149, "cited_by_url": "https://scholar.google.com/scholar?cites=2764357361710126723"})

    def test_links_to_all_cluster_ids_of_a_merged_paper(self):
        self.assertEqual(
            self.citations[normalize_paper_title("Diagnosing missed cases")]["cited_by_url"],
            "https://scholar.google.com/scholar?cites=9736194330297635545,15246350528695278218")

    def test_paper_with_no_citations(self):
        self.assertEqual(self.citations[normalize_paper_title("A paper nobody cited")],
                         {"count": 0, "cited_by_url": None})

    def test_keeps_the_more_cited_of_two_papers_with_the_same_title(self):
        self.assertEqual(self.citations[normalize_paper_title("REViewer")]["count"], 80)

    def test_page_with_no_papers(self):
        self.assertEqual(parse_google_scholar_profile_page("<html>Please show you're not a robot</html>"), {})


class GetDateRangeOfLastFullWeeksTests(unittest.TestCase):

    def test_date_ranges(self):
        monday_nov_9, sunday_nov_15 = datetime.date(2026, 11, 9), datetime.date(2026, 11, 15)
        # on a Monday, the last full week ended the day before
        self.assertEqual(get_date_range_of_last_full_weeks(datetime.date(2026, 11, 16), 1),
                         (monday_nov_9, sunday_nov_15))
        # on a Sunday, that day's week isn't over yet
        self.assertEqual(get_date_range_of_last_full_weeks(sunday_nov_15, 1),
                         (datetime.date(2026, 11, 2), datetime.date(2026, 11, 8)))
        # on a Tuesday, when the weekly GitHub Actions run happens
        self.assertEqual(get_date_range_of_last_full_weeks(datetime.date(2026, 11, 17), 12),
                         (datetime.date(2026, 8, 24), sunday_nov_15))


class FillInProjectUsageCountPlaceholdersTests(unittest.TestCase):

    def test_formats_each_kind(self):
        project_usage_counts = {
            "github_stars": {"bw2/ConfigArgParse": {"count": 761}, "bw2/step-pipeline": {"count": 1}},
            "google_scholar_citations": {
                "Some paper": {"count": 11947, "cited_by_url": "https://scholar.google.com/scholar?cites=1,2"},
                "Uncited paper": {"count": 0, "cited_by_url": None},
            },
            "weekly_visitors": {"liftover.broadinstitute.org": {
                "count": 1234, "averaged_from": "2026-08-24", "averaged_to": "2026-11-15"}},
        }
        markdown_text = (
            "{{github_stars:bw2/ConfigArgParse}}, {{github_stars:bw2/step-pipeline}}, "
            "{{google_scholar_citations:Some paper}}, {{google_scholar_citations:Uncited paper}}, "
            "{{weekly_visitors:liftover.broadinstitute.org}}")
        self.assertEqual(fill_in_project_usage_count_placeholders(markdown_text, project_usage_counts), (
            "[761 GitHub stars](https://github.com/bw2/ConfigArgParse/stargazers), "
            "[1 GitHub star](https://github.com/bw2/step-pipeline/stargazers), "
            "[11,947 citations](https://scholar.google.com/scholar?cites=1,2), 0 citations, "
            "1,234 weekly visitors [Google Analytics average: 8/24/2026 to 11/15/2026]"))

    def test_leaves_out_weekly_visitor_counts_under_the_minimum(self):
        project_usage_counts = {
            "github_stars": {"broadinstitute/seqr": {"count": 221}},
            "weekly_visitors": {
                "seqr.broadinstitute.org": {"count": 151},
                "genelookup.broadinstitute.org": {"count": 48},
                "liftover.broadinstitute.org": {
                    "count": 1000, "averaged_from": "2026-08-24", "averaged_to": "2026-11-15"},
            },
        }
        markdown_text = (
            "- first<br /><b>Users:</b> {{weekly_visitors:seqr.broadinstitute.org}}, "
            "{{github_stars:broadinstitute/seqr}}\n"
            "- last<br /><b>Users:</b> {{github_stars:broadinstitute/seqr}}, "
            "{{weekly_visitors:genelookup.broadinstitute.org}}\n"
            "- only<br /><b>Users:</b> {{weekly_visitors:genelookup.broadinstitute.org}}\n"
            "- two left out<br /><b>Users:</b> {{weekly_visitors:seqr.broadinstitute.org}}, "
            "{{weekly_visitors:genelookup.broadinstitute.org}}\n"
            "- at the minimum<br /><b>Users:</b> {{weekly_visitors:liftover.broadinstitute.org}}\n")
        self.assertEqual(fill_in_project_usage_count_placeholders(markdown_text, project_usage_counts), (
            "- first<br /><b>Users:</b> [221 GitHub stars](https://github.com/broadinstitute/seqr/stargazers)\n"
            "- last<br /><b>Users:</b> [221 GitHub stars](https://github.com/broadinstitute/seqr/stargazers)\n"
            "- only\n"
            "- two left out\n"
            "- at the minimum<br /><b>Users:</b> 1,000 weekly visitors [Google Analytics average: 8/24/2026 to "
            "11/15/2026]\n"))

    def test_missing_counts_are_shown_as_question_marks(self):
        markdown_text = ("{{github_stars:bw2/ConfigArgParse}}, {{google_scholar_citations:Some paper}}, "
                         "{{weekly_visitors:liftover.broadinstitute.org}}")
        self.assertEqual(fill_in_project_usage_count_placeholders(markdown_text, {}), (
            "[?? GitHub stars](https://github.com/bw2/ConfigArgParse/stargazers), ?? citations, ?? weekly visitors"))


if __name__ == "__main__":
    unittest.main()
