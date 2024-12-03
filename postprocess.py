import os
import re
import sys
import subprocess

# Define the base URL
base_url = "https://raw.githubusercontent.com/fskelly/fskelly.me/main/static/"

# Regular expression to find Hugo figure shortcodes
figure_url_pattern = re.compile(r'{{<\s*figure\s+src="([^"]+)"\s+alt="([^"]+)"\s*>}}')

def update_image_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all figure shortcodes
    matches = figure_url_pattern.findall(content)

    # Update each URL
    for match in matches:
        src, alt = match
        if not src.startswith('http'):
            new_url = base_url + src.lstrip('/')
            new_figure = f'{{{{< figure src="{new_url}" alt="{alt}" >}}}}'
            old_figure = f'{{{{< figure src="{src}" alt="{alt}" >}}}}'
            content = content.replace(old_figure, new_figure)

    # Save the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    update_image_urls(file_path)

    # Call the PowerShell script
    subprocess.run(["powershell.exe", "-File", "./commit.ps1"], check=True)

if __name__ == "__main__":
    main()