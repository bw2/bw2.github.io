set -ex

git pull
python3 scripts/fetch_project_usage_counts.py  # refreshes the visitor, star and citation counts on the projects page
python3 scripts/generate_html.py
git add -u
git add projects.md projects.html project_usage_counts.json  # new files, which git add -u skips until they're tracked
git stat
git commit -m "." .
git push
