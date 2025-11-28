import os
from bs4 import BeautifulSoup

root_dir = '/home/user/MyProject/Basis_linux'

def remove_source_link(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Find and remove the "View page source" link
        # It's typically in the breadcrumbs area with class "wy-breadcrumbs-aside"
        aside = soup.find('li', class_='wy-breadcrumbs-aside')
        if aside:
            aside.decompose()
            modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

# Walk through all files
count = 0
updated = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            if remove_source_link(os.path.join(root, file)):
                updated += 1
            count += 1

print(f"Processed {count} HTML files, updated {updated} files.")
