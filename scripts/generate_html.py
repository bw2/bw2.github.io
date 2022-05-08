import glob
import jinja2
import markdown
import re

#%%

with open("scripts/blog_post_template.html", "rt") as f:
    blog_post_template = jinja2.Template(f.read())


#%%

for markdown_file_path in glob.glob("*.md"):
    if markdown_file_path == "README.md":
        continue
        
    print(f"Reading {markdown_file_path}")
    output_path = re.sub(".md$", ".html", markdown_file_path)

    with open(markdown_file_path, "rt") as f:
        markdown_html = markdown.markdown(f.read())

    with open(output_path, "wt") as f:
        f.write(blog_post_template.render(markdown_html=markdown_html))


#%%