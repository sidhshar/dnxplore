import markdown

def markdown_file_to_html(md_file_path: str, html_file_path: str):
    """
    Convert a Markdown file to an HTML file.

    :param md_file_path: Path to the Markdown file to convert.
    :param html_file_path: Path to save the converted HTML file.
    """
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()
    
    html = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc'])
    
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html)

# Example usage
markdown_file_to_html('api.md', 'api.html')
