import os
from bs4 import BeautifulSoup

root_dir = '/home/user/MyProject/Basis_linux'

def remove_footer_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Find footer
        footer = soup.find('footer')
        if footer:
            # Find and remove the contentinfo div with copyright
            contentinfo = footer.find('div', role='contentinfo')
            if contentinfo:
                contentinfo.decompose()
                modified = True
            
            # Remove text nodes and links related to Sphinx/Read the Docs/Dark theme
            # We'll look for these patterns and remove them
            for element in list(footer.descendants):
                if element.name is None:  # Text node
                    text = str(element).strip()
                    if any(phrase in text for phrase in ['Собрано при помощи', 'Dark theme provided by']):
                        element.extract()
                        modified = True
                elif element.name == 'a':
                    href = element.get('href', '')
                    if any(domain in href.lower() for domain in ['sphinx', 'readthedocs', 'mrdogebro']):
                        # Remove the entire text around this link
                        parent_text = element.parent
                        if parent_text:
                            parent_text.extract()
                            modified = True
                        break
        
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
            if remove_footer_text(os.path.join(root, file)):
                updated += 1
            count += 1

print(f"Processed {count} HTML files, updated {updated} files.")
