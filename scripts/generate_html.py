import glob
import jinja2
import markdown
import os
import re

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

    try:
        year = int(date_posted[0])
        month = int(date_posted[1])
        date = int(date_posted[2])
    except Exception as e:
        print(f"Skipping .md file: {markdown_file_path}")
        continue

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

    markdown_file_contents = re.sub("```(.*?)```", r"<pre><code>\1</pre></code>", markdown_file_contents, flags=re.DOTALL)
    markdown_html = markdown.markdown(markdown_file_contents)

    blog_post_template = blog_post_template2 if year > 2022 else blog_post_template1

    output_html = blog_post_template.render(
        markdown_html=markdown_html,
        title=title,
        date=f"{month}/{date}/{year}",
    )
    with open(output_html_path, "wt") as f:
        f.write(output_html)

#%%
