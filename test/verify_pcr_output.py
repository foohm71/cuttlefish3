#!/usr/bin/env python3
"""
Script to verify the generated PCR tickets CSV file.
"""
import csv
from collections import Counter

def verify_pcr_output():
    """Verify the generated PCR tickets."""
    input_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv'
    
    # Increase CSV field size limit
    csv.field_size_limit(10000000)
    
    projects = []
    keys = []
    priorities = []
    types = []
    dates = []
    
    rows_processed = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) >= 18:
                projects.append(row[5])
                keys.append(row[3])
                priorities.append(row[4])
                types.append(row[12])
                dates.append(row[1][:10])  # Just the date part
                rows_processed += 1
    
    print(f"Total tickets processed: {rows_processed}")
    print()
    
    # Project distribution
    project_counts = Counter(projects)
    print("Project distribution:")
    for project, count in project_counts.most_common():
        print(f"  {project}: {count}")
    print()
    
    # Priority distribution
    priority_counts = Counter(priorities)
    print("Priority distribution:")
    for priority, count in priority_counts.most_common():
        print(f"  {priority}: {count}")
    print()
    
    # Type distribution
    type_counts = Counter(types)
    print("Type distribution:")
    for itype, count in type_counts.most_common():
        print(f"  {itype}: {count}")
    print()
    
    # Date range
    dates_clean = [d.strip('"') for d in dates if d.strip('"')]
    dates_clean.sort()
    print(f"Date range: {dates_clean[0]} to {dates_clean[-1]}")
    print()
    
    # Sample keys
    print("Sample PCR keys:")
    sample_keys = [k.strip('"') for k in keys[:10]]
    for key in sample_keys:
        print(f"  {key}")
    print()
    
    # Verify PCR pattern
    pcr_keys = [k.strip('"') for k in keys if k.strip('"').startswith('PCR-')]
    print(f"Total PCR keys: {len(pcr_keys)}")
    if pcr_keys:
        pcr_numbers = [int(k.split('-')[1]) for k in pcr_keys]
        print(f"PCR range: PCR-{min(pcr_numbers)} to PCR-{max(pcr_numbers)}")

if __name__ == "__main__":
    verify_pcr_output()