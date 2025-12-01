import os
from bs4 import BeautifulSoup

root_dir = '/home/user/MyProject/Basis_linux'
target_file = os.path.join(root_dir, 'basis.html')

def inspect_sidebar(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the sidebar menu
        sidebar = soup.find('div', class_='wy-menu-vertical')
        if sidebar:
            print(f"--- Sidebar links in {filepath} ---")
            for link in sidebar.find_all('a'):
                text = link.get_text(strip=True)
                print(f"Link: '{text}'")
        else:
            print("Sidebar not found")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

inspect_sidebar(target_file)
