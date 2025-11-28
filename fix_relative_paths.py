import os
from bs4 import BeautifulSoup

root_dir = '/home/user/MyProject/Basis_linux'

def get_relative_prefix(filepath, root):
    # Calculate depth relative to root
    rel_path = os.path.relpath(filepath, root)
    depth = rel_path.count(os.sep)
    return '../' * depth

def fix_relative_paths(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate correct prefix
        # e.g. for basis/header/commands.html -> ../../
        # for basis.html -> (empty)
        rel_dir = os.path.dirname(os.path.relpath(filepath, root_dir))
        if rel_dir == '.':
            prefix = ''
        else:
            depth = rel_dir.count(os.sep) + 1
            prefix = '../' * depth
            
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Fix <script src="...">
        for script in soup.find_all('script', src=True):
            src = script['src']
            # Target our injected scripts which might be wrong
            # They currently look like "_static/js/..." or "/_static/js/..."
            if 'modern_search.js' in src or 'navigation_improvements.js' in src:
                # Strip any existing prefix to get clean filename
                filename = src.split('/')[-1]
                # Reconstruct correct path
                new_src = f"{prefix}_static/js/{filename}"
                # Preserve query params if any
                if '?' in src:
                    query = src.split('?')[-1]
                    new_src = f"{prefix}_static/js/{filename.split('?')[0]}?{query}"
                
                if script['src'] != new_src:
                    script['src'] = new_src
                    modified = True

        # Fix <link href="...">
        for link in soup.find_all('link', href=True):
            href = link['href']
            if 'modern_search.css' in href or 'navigation_improvements.css' in href:
                filename = href.split('/')[-1]
                new_href = f"{prefix}_static/css/{filename}"
                if '?' in href:
                    query = href.split('?')[-1]
                    new_href = f"{prefix}_static/css/{filename.split('?')[0]}?{query}"
                
                if link['href'] != new_href:
                    link['href'] = new_href
                    modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        return False
            
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
            if fix_relative_paths(filepath):
                updated += 1
            count += 1

print(f"Processed {count} HTML files, updated {updated} files.")
