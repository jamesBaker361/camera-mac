from difflib import HtmlDiff

def diff_files_html(file1, file2, output_html):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Generate HTML diff
    html_diff = HtmlDiff()
    html_content = html_diff.make_file(lines1, lines2, file1, file2)

    # Write to an output file
    with open(output_html, 'w') as output_file:
        output_file.write(html_content)

    print(f"Diff written to {output_html}")

# Usage
diff_files_html('/Users/jbaker15/Desktop/config.txt', '/Users/jbaker15/Desktop/config_bad.txt', 'diff_output.html')
