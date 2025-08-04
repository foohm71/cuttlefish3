#!/usr/bin/env python3
"""
Script to generate 2,860 synthetic PCR release tickets across 5 projects
over an 11-year timespan with weekly release cadence.
"""
import csv
import random
from datetime import datetime, timedelta

# Project configurations
PROJECTS = {
    'FLEX': {
        'name': 'Apache Flex',
        'repo': 'ASF',
        'modules': ['FlexCore', 'FlexUI', 'FlexCompiler', 'FlexAIR', 'FlexFramework', 'FlexSDK'],
        'components': ['DataBinding', 'DisplayObject', 'EventDispatcher', 'UIComponent', 'Container', 'Module'],
        'version_base': '4.16',
        'assignee_range': (12000, 12500),
        'reporter_range': (12000, 12500)
    },
    'JBIDE': {
        'name': 'JBoss Tools',
        'repo': 'JBOSS',
        'modules': ['JBTCore', 'JBTServer', 'JBTWeb', 'JBTData', 'JBTAppServer', 'JBTDebug'],
        'components': ['Eclipse Integration', 'Server Runtime', 'Web Tools', 'Database Tools', 'Debugger', 'Wizard'],
        'version_base': '4.28',
        'assignee_range': (8000, 9000),
        'reporter_range': (8000, 9000)
    },
    'RF': {
        'name': 'RichFaces',
        'repo': 'JBOSS',
        'modules': ['RFCore', 'RFComponents', 'RFThemes', 'RFValidator', 'RFAjax', 'RFSkin'],
        'components': ['UIComponent', 'AjaxBehavior', 'Validator', 'Converter', 'Theme Engine', 'ResourceHandler'],
        'version_base': '5.0',
        'assignee_range': (15000, 16000),
        'reporter_range': (15000, 16000)
    },
    'SPR': {
        'name': 'Spring Framework',
        'repo': 'SPRING',
        'modules': ['SpringCore', 'SpringMVC', 'SpringSecurity', 'SpringData', 'SpringBoot', 'SpringCloud'],
        'components': ['IOC Container', 'AOP Framework', 'Data Access', 'Web Framework', 'Security', 'Boot Starter'],
        'version_base': '6.1',
        'assignee_range': (25000, 26000),
        'reporter_range': (25000, 26000)
    },
    'HBASE': {
        'name': 'HBase',
        'repo': 'ASF',
        'modules': ['HBaseCore', 'HBaseMaster', 'HBaseRegion', 'HBaseClient', 'HBaseAdmin', 'HBaseCoprocessor'],
        'components': ['RegionServer', 'HMaster', 'WAL', 'MemStore', 'HFile', 'ZooKeeper Integration'],
        'version_base': '2.5',
        'assignee_range': (8000, 8500),
        'reporter_range': (8000, 8500)
    }
}

# Release types and their probabilities
RELEASE_TYPES = [
    ('Major', 0.1),     # 10% major releases
    ('Minor', 0.3),     # 30% minor releases  
    ('Patch', 0.6)      # 60% patch releases
]

# Bug fix categories
BUG_CATEGORIES = [
    'memory leak', 'performance optimization', 'null pointer exception', 'concurrency issue',
    'configuration error', 'API compatibility', 'security vulnerability', 'resource cleanup',
    'thread safety', 'connection timeout', 'validation error', 'parsing issue',
    'serialization problem', 'cache invalidation', 'dependency conflict', 'encoding issue'
]

# Feature categories  
FEATURE_CATEGORIES = [
    'new API endpoint', 'enhanced UI component', 'improved logging', 'configuration option',
    'integration support', 'monitoring capability', 'debugging tool', 'performance metric',
    'user interface enhancement', 'workflow improvement', 'automation feature', 'documentation update'
]

def generate_version(base_version, release_count, release_type):
    """Generate a version string based on release count and type."""
    major, minor = base_version.split('.')
    major, minor = int(major), int(minor)
    
    if release_type == 'Major':
        major += release_count // 52  # Major version per year
        minor = 0
        patch = 0
    elif release_type == 'Minor':
        minor += (release_count // 4)  # Minor every month
        patch = 0
    else:  # Patch
        patch = release_count % 10
    
    return f"{major}.{minor}.{patch}"

def generate_bug_fixes(project_key, count=None):
    """Generate realistic bug fix descriptions."""
    if count is None:
        count = random.randint(3, 15)
    
    fixes = []
    for _ in range(count):
        bug_type = random.choice(BUG_CATEGORIES)
        component = random.choice(PROJECTS[project_key]['components'])
        ticket_num = random.randint(1000, 99999)
        fixes.append(f"Fixed {bug_type} in {component} module ({project_key}-{ticket_num})")
    
    return fixes

def generate_features(project_key, count=None):
    """Generate realistic feature descriptions."""
    if count is None:
        count = random.randint(1, 8)
    
    features = []
    for _ in range(count):
        feature_type = random.choice(FEATURE_CATEGORIES)
        module = random.choice(PROJECTS[project_key]['modules'])
        features.append(f"Added {feature_type} to {module}")
    
    return features

def generate_release_description(project_key, version, release_type, release_count):
    """Generate comprehensive release description."""
    project_info = PROJECTS[project_key]
    project_name = project_info['name']
    
    # Generate bug fixes and features
    bug_fixes = generate_bug_fixes(project_key)
    features = generate_features(project_key)
    
    # Select modules updated this release
    modules_updated = random.sample(project_info['modules'], random.randint(2, 4))
    
    description = f"Release {project_name} {version} with {len(bug_fixes)} bug fixes and {len(features)} enhancements.\n\n"
    description += f"## Release Summary\n"
    description += f"This {release_type.lower()} release includes critical updates across {len(modules_updated)} core modules "
    description += f"with focus on stability, performance, and feature completeness.\n\n"
    
    description += f"## Modules Updated\n"
    for module in modules_updated:
        module_fixes = [f for f in bug_fixes if module.lower() in f.lower()][:3]
        module_features = [f for f in features if module.lower() in f.lower()][:2]
        
        description += f"### {module}\n"
        if module_fixes:
            for fix in module_fixes:
                description += f"- {fix}\n"
        if module_features:
            for feature in module_features:
                description += f"- {feature}\n"
        description += f"- Performance improvements and code optimization\n\n"
    
    description += f"## Key Improvements\n"
    for fix in bug_fixes[:5]:  # Top 5 fixes
        description += f"- {fix}\n"
    
    description += f"\n## New Features\n"
    for feature in features[:3]:  # Top 3 features  
        description += f"- {feature}\n"
    
    # Add technical details
    description += f"\n## Technical Details\n"
    description += f"- Automated test coverage: {random.randint(85, 98)}%\n"
    description += f"- Performance improvement: {random.randint(5, 25)}% faster execution\n"
    description += f"- Memory usage reduction: {random.randint(10, 30)}% optimization\n"
    description += f"- Compatibility maintained with previous {major_version(version)} series\n\n"
    
    description += f"## Quality Assurance\n"
    description += f"- {random.randint(500, 2000)} automated tests executed\n"
    description += f"- Cross-platform compatibility verified\n" 
    description += f"- Security scan completed with zero critical issues\n"
    description += f"- Performance regression testing passed\n\n"
    
    description += f"## Installation Notes\n"
    description += f"Standard upgrade process applies. Backup recommended before installation."
    
    return description

def major_version(version_str):
    """Extract major version from version string."""
    return version_str.split('.')[0]

def generate_pcr_tickets():
    """Generate all 2,860 PCR tickets."""
    output_file = '/Users/foohm/github/cuttlefish3/JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv'
    
    # CSV header matching original format
    header = ['id', 'created', 'description', 'key', 'priority', 'project', 'project_name', 
              'repositoryname', 'resolution', 'resolved', 'status', 'title', 'type', 
              'updated', 'votes', 'watchers', 'assignee_id', 'reporter_id']
    
    # Start date: 2014-01-06 (first Monday of 2014)
    start_date = datetime(2014, 1, 6)
    
    tickets = []
    ticket_id = 500000  # Start with high ID to avoid conflicts
    pcr_number = 1
    
    # Generate tickets for each project
    for project_key, project_info in PROJECTS.items():
        print(f"Generating {project_key} releases...")
        
        for week in range(572):  # 52 weeks * 11 years = 572 weeks
            # Calculate release date (every Monday)
            release_date = start_date + timedelta(weeks=week)
            
            # Determine release type
            rand = random.random()
            cumulative = 0
            release_type = 'Patch'  # default
            for rtype, prob in RELEASE_TYPES:
                cumulative += prob
                if rand <= cumulative:
                    release_type = rtype
                    break
            
            # Generate version
            version = generate_version(project_info['version_base'], week, release_type)
            
            # Generate ticket data
            created = release_date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            resolved = (release_date + timedelta(days=random.randint(1, 3))).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            updated = resolved
            
            description = generate_release_description(project_key, version, release_type, week)
            key = f"PCR-{pcr_number}"
            title = f"{project_info['name']} Release {version}"
            
            # Determine priority based on release type
            if release_type == 'Major':
                priority = 'Critical'
            elif release_type == 'Minor':
                priority = 'Major'
            else:
                priority = 'Minor'
            
            # Generate assignee and reporter IDs
            assignee_id = random.randint(*project_info['assignee_range'])
            reporter_id = random.randint(*project_info['reporter_range'])
            
            # Create ticket row - let CSV writer handle quoting automatically
            ticket = [
                ticket_id,
                created,
                description,
                key,
                priority,
                project_key,
                project_info["name"],
                project_info["repo"],
                "Fixed",
                resolved,
                "Closed",
                title,
                "Task",
                updated,
                random.randint(0, 50),
                random.randint(5, 100),
                assignee_id,
                reporter_id
            ]
            
            tickets.append(ticket)
            ticket_id += 1
            pcr_number += 1
    
    # Write to CSV file
    print(f"Writing {len(tickets)} tickets to {output_file}...")
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(tickets)
    
    print(f"Generated {len(tickets)} PCR tickets successfully!")
    print(f"File saved as: {output_file}")
    
    # Print summary statistics
    print(f"\nSummary:")
    print(f"- Total tickets: {len(tickets)}")
    print(f"- Date range: {start_date.strftime('%Y-%m-%d')} to {(start_date + timedelta(weeks=571)).strftime('%Y-%m-%d')}")
    print(f"- Projects: {', '.join(PROJECTS.keys())}")
    print(f"- Tickets per project: {len(tickets) // len(PROJECTS)}")

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    generate_pcr_tickets()