import os
from bs4 import BeautifulSoup

# Directory to search
root_dir = '/home/user/MyProject/Basis_linux'

# Sections to remove (text of the link)
sections_to_remove = [
    "Ссылки",
    "RHCSA",
    "Полезные ссылки",
    "Проблемы и решения",
    "Changelog"
]

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Find the sidebar menu
        sidebar = soup.find('div', class_='wy-menu-vertical')
        if sidebar:
            # Find all ul tags within the sidebar
            ul_tags = sidebar.find_all('ul', recursive=False)
            
            for ul in ul_tags:
                # Check if this ul contains any of the unwanted links
                should_remove = False
                for link in ul.find_all('a'):
                    if link.get_text(strip=True) in sections_to_remove:
                        should_remove = True
                        break
                
                if should_remove:
                    ul.decompose()
                    modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Walk through all files
count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files.")
