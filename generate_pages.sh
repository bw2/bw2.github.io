set -ex

git pull
python3 scripts/generate_html.py

git stat
git add -u
git commit -m "." .
git push
