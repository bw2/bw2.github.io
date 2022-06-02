import glob
import jinja2
import markdown
import os
import re

#%%

with open("scripts/blog_post_template.html", "rt") as f:
    blog_post_template = jinja2.Template(f.read())


#%%

for markdown_file_path in glob.glob("*.md"):
    if markdown_file_path == "README.md":
        continue

    print(f"Reading {markdown_file_path}")
    output_prefix = re.sub(".md$", "", markdown_file_path)
    output_html_path = f"{output_prefix}.html"
    title = os.path.basename(output_prefix)
    with open(markdown_file_path, "rt") as f:
        markdown_html = markdown.markdown(f.read())

    date_posted = output_prefix.split("-")
    year = int(date_posted[0])
    month = int(date_posted[1])
    date = int(date_posted[2])

    markdown_html.replace("</h2>", f"""<div style="color:grey; position:relative; float:right; font-size:15px">{year}/{month}/{date}/</div></h2>""")
    with open(output_html_path, "wt") as f:
        f.write(blog_post_template.render(markdown_html=markdown_html, title=title))


#%%
