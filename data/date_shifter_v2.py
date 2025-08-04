#!/usr/bin/env python3
"""
Script to shift dates in JIRA CSV data forward by 4064 days (11.1 years)
using regex-based approach to handle complex CSV structure.
"""
import re
from datetime import datetime, timedelta

# Date shift amount calculated: 4064 days
SHIFT_DAYS = 4064

def shift_date_match(match):
    """Callback function to shift a date match."""
    date_str = match.group(0)
    
    try:
        # Handle different timestamp formats
        if '.' in date_str:
            # Format: "2008-08-09 06:37:25.631"
            dt_part = date_str[:19]  # Take just the datetime part
            microseconds = date_str[19:]  # Keep the milliseconds part
            dt = datetime.strptime(dt_part, '%Y-%m-%d %H:%M:%S')
        else:
            # Format: "2013-12-16 23:26:05"
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            microseconds = ""
        
        # Shift the date
        shifted_dt = dt + timedelta(days=SHIFT_DAYS)
        
        # Format back to string
        shifted_str = shifted_dt.strftime('%Y-%m-%d %H:%M:%S')
        return shifted_str + microseconds
        
    except ValueError:
        # If parsing fails, return original
        return date_str

def process_file():
    """Process the file using regex to find and shift all dates."""
    input_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET.csv'
    output_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv'
    
    # Regex pattern to match timestamps in the format YYYY-MM-DD HH:MM:SS[.microseconds]
    date_pattern = r'20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?'
    
    print("Reading input file...")
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    print("Finding and shifting dates...")
    # Count matches before replacement
    matches = re.findall(date_pattern, content)
    print(f"Found {len(matches)} date timestamps to shift")
    
    # Replace all dates with shifted versions
    shifted_content = re.sub(date_pattern, shift_date_match, content)
    
    print("Writing output file...")
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(shifted_content)
    
    # Verify some shifts by checking first few matches
    if matches:
        print(f"\nSample transformations:")
        sample_matches = matches[:5]
        for original in sample_matches:
            shifted = shift_date_match(re.match(date_pattern, original))
            print(f"  {original} → {shifted}")
    
    print(f"\nComplete! Shifted {len(matches)} dates")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    process_file()