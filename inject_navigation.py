import os
from bs4 import BeautifulSoup

root_dir = '/home/user/MyProject/Basis_linux'

def inject_navigation(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Add CSS to head
        if soup.head:
            if not soup.head.find('link', href=lambda x: x and 'navigation_improvements.css' in x):
                css_link = soup.new_tag('link', rel='stylesheet', type='text/css', href='/_static/css/navigation_improvements.css')
                soup.head.append(css_link)
                modified = True
        
        # Add JS to body (end)
        if soup.body:
            if not soup.body.find('script', src=lambda x: x and 'navigation_improvements.js' in x):
                js_script = soup.new_tag('script', src='/_static/js/navigation_improvements.js')
                soup.body.append(js_script)
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
            if inject_navigation(os.path.join(root, file)):
                updated += 1
            count += 1

print(f"Processed {count} HTML files, updated {updated} files.")
