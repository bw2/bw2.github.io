set -ex

git pull
python3 scripts/generate_html.py
git add -u
git add projects.md projects.html  # the undated projects page, which git add -u skips until it's tracked
git stat
git commit -m "." .
git push
