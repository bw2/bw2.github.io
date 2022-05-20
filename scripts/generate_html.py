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
    output_prefix = re.sub(".md$", "", markdown_file_path)
    output_html_path = f"{output_prefix}.html"
    title = os.path.basename(output_prefix)
    with open(markdown_file_path, "rt") as f:
        markdown_html = markdown.markdown(f.read())

    with open(output_html_path, "wt") as f:
        f.write(blog_post_template.render(markdown_html=markdown_html, title=title))


#%%
