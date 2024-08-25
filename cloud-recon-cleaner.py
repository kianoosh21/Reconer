import re
import sys

def extract_domains(input_file):
    domains = set()  # Use a set to avoid duplicates

    # Regular expression to match valid domain names within brackets
    domain_pattern = re.compile(r'\[(.*?)\]')

    with open(input_file, 'r') as infile:
        for line in infile:
            matches = domain_pattern.findall(line)
            for match in matches:
                for domain in match.split(','):
                    domain = domain.strip().lstrip('*.')  # Remove *. from the beginning
                    if is_valid_domain(domain):
                        domains.add(domain)

    # Print the unique domains to the terminal
    for domain in sorted(domains):  # Sort the domains for easier reading
        print(domain)

def is_valid_domain(domain):
    # Simple regex to validate domain names, allowing multiple subdomains
    return re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain) is not None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 process_cloudrecon.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    extract_domains(input_file)
