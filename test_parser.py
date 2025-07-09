from parser.html_parser import extract_tables_from_html, print_table_sample

html_path = "data/raw/scraped_page.html"
tables = extract_tables_from_html(html_path)

print_table_sample(tables)
