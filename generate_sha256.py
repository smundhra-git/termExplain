#!/usr/bin/env python3
"""
Generate SHA256 hashes for Python packages
"""

import hashlib
import requests
import re

packages = [
    ("google-generativeai", "0.3.0"),
    ("click", "8.1.0"),
    ("rich", "13.0.0"),
    ("colorama", "0.4.6"),
    ("python-dotenv", "1.0.0"),
    ("requests", "2.31.0")
]

def get_sha256(url):
    """Get SHA256 hash of a file from URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return hashlib.sha256(response.content).hexdigest()
    except Exception as e:
        print(f"Error getting SHA256 for {url}: {e}")
        return None

def main():
    print("Generating SHA256 hashes for Python packages...")
    print()
    
    for package, version in packages:
        # Try different URL patterns
        urls = [
            f"https://files.pythonhosted.org/packages/source/{package[0].lower()}/{package}/{package}-{version}.tar.gz",
            f"https://files.pythonhosted.org/packages/source/{package[0].lower()}/{package.replace('-', '_')}/{package}-{version}.tar.gz",
            f"https://files.pythonhosted.org/packages/source/{package[0].lower()}/{package.replace('-', '')}/{package}-{version}.tar.gz"
        ]
        
        sha256 = None
        working_url = None
        
        for url in urls:
            sha256 = get_sha256(url)
            if sha256:
                working_url = url
                break
        
        if sha256:
            print(f'  resource "{package}" do')
            print(f'    url "{working_url}"')
            print(f'    sha256 "{sha256}"')
            print(f'  end')
            print()
        else:
            print(f"❌ Could not get SHA256 for {package} {version}")
            print()

if __name__ == "__main__":
    main() 