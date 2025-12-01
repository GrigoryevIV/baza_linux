import os
from bs4 import BeautifulSoup

filepath = '/home/user/MyProject/Basis_linux/basis.html'

def remove_rhcsa_link():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Find and remove "64. Про сертификацию RHCSA" from sidebar
        # It's in a li with class toctree-l1
        for link in soup.find_all('a'):
            if "64. Про сертификацию RHCSA" in link.get_text():
                # Remove the parent li
                li = link.find_parent('li')
                if li:
                    li.decompose()
                    modified = True
                    print("Removed '64. Про сертификацию RHCSA'")

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

remove_rhcsa_link()
