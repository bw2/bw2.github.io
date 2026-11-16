import glob
import jinja2
import markdown
import os
import re

# Markdown pages whose file names don't start with a date. They are rendered with no date in the header.
UNDATED_MARKDOWN_FILES = {"projects.md"}

with open("scripts/blog_post_template.html", "rt") as f:
    blog_post_template1 = jinja2.Template(f.read())

with open("scripts/blog_post_template2.html", "rt") as f:
    blog_post_template2 = jinja2.Template(f.read())

for markdown_file_path in glob.glob("*.md"):
    if markdown_file_path == "README.md":
        continue

    print(f"Reading {markdown_file_path}")
    output_prefix = re.sub(".md$", "", markdown_file_path)

    date_posted = output_prefix.split("-")

    if markdown_file_path in UNDATED_MARKDOWN_FILES:
        year = None
        date_shown_in_header = ""
    else:
        try:
            year = int(date_posted[0])
            month = int(date_posted[1])
            date = int(date_posted[2])
        except Exception as e:
            print(f"Skipping .md file: {markdown_file_path}")
            continue
        date_shown_in_header = f"{month}/{date}/{year}"

    output_html_path = f"{output_prefix}.html"

    with open(markdown_file_path, "rt") as f:
        markdown_file_contents = f.read()

    for line in markdown_file_contents.split("\n"):
        if line.startswith("## "):
            title = line.strip("##").strip()
            break
    else:
        raise ValueError(f"Title not found in {markdown_file_path}. No line starts with '## '")

    # handle literal / code blocks
    markdown_file_contents = markdown_file_contents.replace("<code> </code>", "")
    markdown_file_contents = re.sub("```\n*(.*?)\n*```", r"<pre><code>\1</code></pre>", markdown_file_contents, flags=re.DOTALL)
    markdown_html = markdown.markdown(markdown_file_contents)

    blog_post_template = blog_post_template2 if year is None or year > 2022 else blog_post_template1

    output_html = blog_post_template.render(
        markdown_html=markdown_html,
        title=title,
        date=date_shown_in_header,
    )
    with open(output_html_path, "wt") as f:
        f.write(output_html)

#%%
