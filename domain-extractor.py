import sys
from urllib.parse import urlparse

def extract_domain(url):
    # Ensure the URL has a scheme
    if not urlparse(url).scheme:
        url = 'http://' + url  # Add a scheme to parse correctly
    
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    # Extract domain name from hostname
    domain_parts = hostname.split('.')
    if len(domain_parts) > 2:
        return '.'.join(domain_parts[-2:])
    return hostname

def main(input_file):
    try:
        with open(input_file, 'r') as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()
            if url:  # Skip empty lines
                domain = extract_domain(url)
                print(domain)
    
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 domain-extractor.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    main(input_file)
