while read -r domain; do awk -v domain="$domain" '{print $0"."domain}' subdomains.txt; done < domains.txt > combined.txt
