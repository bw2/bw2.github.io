set -ex

git pull
python3 scripts/generate_html.py

git add -u
git commit -m "." .
git push
