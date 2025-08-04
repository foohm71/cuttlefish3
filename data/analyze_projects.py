#!/usr/bin/env python3
"""
Script to analyze projects and patterns in the shifted JIRA CSV data.
"""
import csv
from collections import Counter

def analyze_projects():
    """Extract and analyze project information."""
    input_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv'
    
    # Increase CSV field size limit
    csv.field_size_limit(10000000)
    
    projects = []
    project_names = []
    keys = []
    titles = []
    types = []
    priorities = []
    
    rows_processed = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip header
        
        print("Header:", header)
        print()
        
        for row in reader:
            if len(row) >= 18:  # Ensure we have all columns
                projects.append(row[5])  # project
                project_names.append(row[6])  # project_name
                keys.append(row[3])  # key
                titles.append(row[11])  # title
                types.append(row[12])  # type
                priorities.append(row[4])  # priority
                
                rows_processed += 1
                if rows_processed >= 15000:  # Limit for analysis
                    break
    
    print(f"Analyzed {rows_processed} rows\n")
    
    # Count unique values
    project_counts = Counter(projects)
    project_name_counts = Counter(project_names)
    type_counts = Counter(types)
    priority_counts = Counter(priorities)
    
    print("Top Projects:")
    for project, count in project_counts.most_common(10):
        print(f"  {project}: {count}")
    
    print("\nTop Project Names:")
    for name, count in project_name_counts.most_common(10):
        print(f"  {name}: {count}")
    
    print("\nTop Issue Types:")
    for itype, count in type_counts.most_common(10):
        print(f"  {itype}: {count}")
    
    print("\nTop Priorities:")
    for priority, count in priority_counts.most_common(10):
        print(f"  {priority}: {count}")
    
    print("\nSample Keys (first 20):")
    for i, key in enumerate(keys[:20]):
        print(f"  {key}")
    
    print("\nSample Titles (first 5):")
    for i, title in enumerate(titles[:5]):
        print(f"  {title[:100]}...")

if __name__ == "__main__":
    analyze_projects()