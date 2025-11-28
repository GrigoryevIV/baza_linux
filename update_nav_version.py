import os
from bs4 import BeautifulSoup
import time

root_dir = '/home/user/MyProject/Basis_linux'
version = str(int(time.time()))  # Use timestamp as version

def update_navigation_links(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Find and update navigation JS link
        nav_js = soup.find('script', src=lambda x: x and 'navigation_improvements.js' in x)
        if nav_js:
            nav_js['src'] = f'/_static/js/navigation_improvements.js?v={version}'
            modified = True
        
        # Find and update navigation CSS link
        nav_css = soup.find('link', href=lambda x: x and 'navigation_improvements.css' in x)
        if nav_css:
            nav_css['href'] = f'/_static/css/navigation_improvements.css?v={version}'
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
            if update_navigation_links(os.path.join(root, file)):
                updated += 1
            count += 1

print(f"Processed {count} HTML files, updated {updated} files with version {version}.")
