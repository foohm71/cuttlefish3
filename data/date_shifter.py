#!/usr/bin/env python3
"""
Script to shift dates in JIRA CSV data forward by 4064 days (11.1 years)
to make the dataset appear more recent.
"""
import csv
import re
from datetime import datetime, timedelta

# Date shift amount calculated: 4064 days
SHIFT_DAYS = 4064

def parse_and_shift_date(date_str):
    """Parse a date string and shift it forward by SHIFT_DAYS."""
    if not date_str or date_str == 'NULL' or not date_str.startswith('"'):
        return date_str
    
    # Remove quotes
    clean_date = date_str.strip('"')
    
    # Skip non-date values (like "Fixed", "Complete", etc.)
    if not re.match(r'20\d{2}-\d{2}-\d{2}', clean_date):
        return date_str
    
    try:
        # Handle different timestamp formats
        if '.' in clean_date:
            # Format: "2008-08-09 06:37:25.631"
            dt = datetime.strptime(clean_date[:19], '%Y-%m-%d %H:%M:%S')
            microseconds = clean_date[19:]  # Keep the milliseconds part
        else:
            # Format: "2013-12-16 23:26:05"
            dt = datetime.strptime(clean_date, '%Y-%m-%d %H:%M:%S')
            microseconds = ""
        
        # Shift the date
        shifted_dt = dt + timedelta(days=SHIFT_DAYS)
        
        # Format back to string
        shifted_str = shifted_dt.strftime('%Y-%m-%d %H:%M:%S')
        return f'"{shifted_str}{microseconds}"'
        
    except ValueError:
        # If parsing fails, return original
        return date_str

def process_csv():
    """Process the CSV file and shift dates in columns 2, 10, and 14."""
    input_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET.csv'
    output_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv'
    
    # Increase CSV field size limit
    csv.field_size_limit(10000000)  # 10MB limit
    
    rows_processed = 0
    dates_shifted = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if len(row) >= 14:  # Ensure we have enough columns
                original_row = row.copy()
                
                # Shift dates in columns: created (1), resolved (9), updated (13) - 0-indexed
                for col_idx in [1, 9, 13]:
                    if col_idx < len(row):
                        original = row[col_idx]
                        shifted = parse_and_shift_date(original)
                        if shifted != original:
                            dates_shifted += 1
                        row[col_idx] = shifted
            
            writer.writerow(row)
            rows_processed += 1
            
            # Progress indicator
            if rows_processed % 10000 == 0:
                print(f"Processed {rows_processed} rows, shifted {dates_shifted} dates")
    
    print(f"Complete! Processed {rows_processed} rows, shifted {dates_shifted} dates")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    process_csv()