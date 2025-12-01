import os
from bs4 import BeautifulSoup

filepath = '/home/user/MyProject/Basis_linux/basis.html'

def find_headers():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        print(f"--- Headers in {filepath} ---")
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = header.get_text(strip=True)
            # Remove the "" symbol which is often added by Sphinx
            text = text.replace('', '').strip()
            print(f"Header ({header.name}): '{text}'")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

find_headers()
