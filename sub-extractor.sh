#!/bin/bash

# Check if a file is provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 subdomains.txt"
  exit 1
fi

# Assign the argument to a variable
file="$1"

# Process each line in the file
awk -F. '
{
  if (NF > 2) {
    subdomain=""
    for (i=1; i<=NF-2; i++) {
      if (i > 1) {
        subdomain=subdomain"."$i
      } else {
        subdomain=$i
      }
    }
    print subdomain
  }
}
' "$file" | sort -u
