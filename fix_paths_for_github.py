import os
import re
from bs4 import BeautifulSoup

root_dir = '/home/user/MyProject/Basis_linux'

def fix_paths(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace absolute paths with relative paths
        # /_static/ -> _static/
        # /_images/ -> _images/
        content = content.replace('="/_static/', '="_static/')
        content = content.replace('="/_images/', '="_images/')
        content = content.replace("='/_static/", "='_static/")
        content = content.replace("='/_images/", "='_images/")
        
        # Also fix in inline styles and scripts
        content = content.replace('url(/_static/', 'url(_static/')
        content = content.replace('url(/_images/', 'url(_images/')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

# Walk through all HTML files
count = 0
updated = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if fix_paths(filepath):
                updated += 1
            count += 1

print(f"Processed {count} HTML files, updated {updated} files.")
