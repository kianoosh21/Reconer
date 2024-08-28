#!/bin/bash

# Set the filenames
raw_domains="RAWDomains.txt"
massdns_output="output.txt"
live_domains="live_domains.txt"
isp_output="isp.txt"

# Step 1: Run massdns to resolve domains
echo "Running massdns to resolve domains..."
./massdns $raw_domains -r resolver.txt -o S -w $massdns_output

# Step 2: Filter live domains and save to live_domains.txt
echo "Filtering live domains..."
grep -v "NXDOMAIN" $massdns_output | awk '{gsub(/\.$/,"",$1); print $1}' | sort -u > $live_domains

# Step 3: Look up the ISP for each live domain and save to isp.txt while also printing it to the console
echo "Looking up ISPs for live domains..."
echo

# Initialize the ISP output file
> $isp_output

# Process each live domain in parallel using GNU Parallel
cat $live_domains | parallel -j 8 "
    ip=\$(dig +short {} | tail -n1);
    if [ -n \"\$ip\" ]; then
        isp=\$(whois \"\$ip\" | grep -i \"OrgName\|orgname\" | head -1 | awk -F: '{print \$2}' | xargs);
        echo \"{} - \$isp\" | tee -a $isp_output;
    else
        echo \"{} - No IP found\" | tee -a $isp_output;
    fi
"

# Final output messages
echo "Report: Success!"
echo "Live domains saved to $live_domains"
echo "ISP information saved to $isp_output"
