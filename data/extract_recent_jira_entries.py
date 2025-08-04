#!/usr/bin/env python3
"""
Extract the most recent 5000 JIRA entries from JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv
based on the created date field for MVP use.
"""

import pandas as pd
import csv
from datetime import datetime

def extract_recent_entries(input_file, output_file, num_entries=5000):
    """
    Extract the most recent entries from JIRA CSV based on created date.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        num_entries (int): Number of recent entries to extract
    """
    print(f"📂 Loading JIRA data from: {input_file}")
    
    # Set CSV field size limit for large JIRA descriptions
    csv.field_size_limit(10000000)
    
    # Read the CSV file
    try:
        df = pd.read_csv(input_file, low_memory=False)
        print(f"✅ Loaded {len(df)} total entries")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Check if created column exists
    if 'created' not in df.columns:
        print("❌ 'created' column not found in CSV")
        print(f"Available columns: {list(df.columns)}")
        return
    
    # Convert created column to datetime with mixed format handling
    print("🕐 Converting created dates...")
    try:
        df['created'] = pd.to_datetime(df['created'], format='mixed', errors='coerce')
        
        # Check for any failed conversions
        null_dates = df['created'].isnull().sum()
        if null_dates > 0:
            print(f"⚠️  {null_dates} dates could not be converted and were set to NaT")
            # Remove rows with invalid dates
            df = df.dropna(subset=['created'])
            print(f"✅ Proceeding with {len(df)} entries with valid dates")
        else:
            print(f"✅ Successfully converted {len(df)} dates")
            
    except Exception as e:
        print(f"❌ Error converting dates: {e}")
        return
    
    # Sort by created date (most recent first)
    print("📅 Sorting by created date (most recent first)...")
    df_sorted = df.sort_values('created', ascending=False)
    
    # Get date range info
    latest_date = df_sorted['created'].iloc[0]
    oldest_date = df_sorted['created'].iloc[-1]
    print(f"📊 Date range: {oldest_date} to {latest_date}")
    
    # Extract the most recent entries
    print(f"✂️  Extracting {num_entries} most recent entries...")
    df_recent = df_sorted.head(num_entries)
    
    # Show extracted date range
    extracted_latest = df_recent['created'].iloc[0]
    extracted_oldest = df_recent['created'].iloc[-1]
    print(f"📋 Extracted date range: {extracted_oldest} to {extracted_latest}")
    
    # Show project distribution in extracted data
    if 'project' in df_recent.columns:
        project_counts = df_recent['project'].value_counts().head(10)
        print(f"\n🏗️  Top projects in extracted data:")
        for project, count in project_counts.items():
            print(f"   {project}: {count} issues")
    
    # Save to output file
    print(f"💾 Saving to: {output_file}")
    try:
        df_recent.to_csv(output_file, index=False)
        print(f"✅ Successfully saved {len(df_recent)} entries")
        
        # Verify file size
        file_size_mb = pd.read_csv(output_file).memory_usage(deep=True).sum() / 1024 / 1024
        print(f"📁 Output file size: ~{file_size_mb:.1f} MB")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return
    
    print(f"\n🎉 Extraction complete!")
    print(f"   Original entries: {len(df):,}")
    print(f"   Extracted entries: {len(df_recent):,}")
    print(f"   Reduction: {((len(df) - len(df_recent)) / len(df) * 100):.1f}%")

if __name__ == "__main__":
    input_file = "JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv"
    output_file = "JIRA_OPEN_DATA_LARGESET_DATESHIFTED_ABRIDGED.csv"
    num_entries = 5000
    
    print("🚀 JIRA Data Extraction for MVP")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print(f"   Entries to extract: {num_entries}")
    print("-" * 50)
    
    extract_recent_entries(input_file, output_file, num_entries)