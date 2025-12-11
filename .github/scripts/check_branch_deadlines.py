#!/usr/bin/env python3
"""
GitHub Actions script to check branch deadlines and update status
Runs hourly to check if branches have passed their deadlines
"""
from datetime import datetime
import re
import subprocess
import json

def extract_deadline_from_readme(readme_content):
    """Extract deadline from README content"""
    # Look for deadline pattern
    deadline_pattern = r'Deadline:\s*([A-Za-z]+ \d{1,2}, \d{4} at 11:59 PM)'
    match = re.search(deadline_pattern, readme_content)
    
    if match:
        deadline_str = match.group(1)
        try:
            # Parse the deadline
            deadline = datetime.strptime(deadline_str, '%B %d, %Y at 11:59 PM')
            return deadline
        except:
            pass
    
    return None

def check_branch_deadline(branch_name):
    """Check if a branch has passed its deadline"""
    try:
        # Checkout branch
        result = subprocess.run(['git', 'checkout', branch_name], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return None
        
        # Read README
        try:
            with open('README.md', 'r') as f:
                content = f.read()
        except:
            return None
        
        deadline = extract_deadline_from_readme(content)
        if not deadline:
            return None
        
        now = datetime.now()
        is_past = now > deadline
        
        return {
            'branch': branch_name,
            'deadline': deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'is_past': is_past,
            'status': 'CLOSED' if is_past else 'ACTIVE'
        }
    
    except Exception as e:
        print(f"Error checking {branch_name}: {e}")
        return None

def update_branch_status(branch_name, is_past):
    """Update branch README status if needed"""
    try:
        result = subprocess.run(['git', 'checkout', branch_name], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return False
        
        with open('README.md', 'r') as f:
            content = f.read()
        
        # Check current status
        current_status = '🟢 ACTIVE' if '🟢 ACTIVE' in content else '🔴 CLOSED'
        expected_status = '🔴 CLOSED' if is_past else '🟢 ACTIVE'
        
        if current_status != expected_status:
            # Update status
            if is_past:
                content = content.replace('🟢 ACTIVE', '🔴 CLOSED')
            else:
                content = content.replace('🔴 CLOSED', '🟢 ACTIVE')
            
            with open('README.md', 'w') as f:
                f.write(content)
            
            subprocess.run(['git', 'add', 'README.md'])
            subprocess.run(['git', 'commit', '-m', f'Update branch status: {expected_status}'])
            return True
    
    except Exception as e:
        print(f"Error updating {branch_name}: {e}")
    
    return False

def main():
    """Main function to check all day branches"""
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    years = [2026, 2027, 2028, 2029]
    
    results = {
        'active': [],
        'closed': [],
        'errors': []
    }
    
    print("Checking branch deadlines...")
    
    for year in years:
        for month in months:
            for week in range(1, 5):
                for day in range(1, 8):
                    branch_name = f"{year}-{month}-week{week}-day{day}"
                    status = check_branch_deadline(branch_name)
                    
                    if status:
                        if status['is_past']:
                            results['closed'].append(status)
                            # Update status if needed
                            update_branch_status(branch_name, True)
                        else:
                            results['active'].append(status)
                    else:
                        results['errors'].append(branch_name)
    
    print(f"\nSummary:")
    print(f"  Active branches: {len(results['active'])}")
    print(f"  Closed branches: {len(results['closed'])}")
    print(f"  Errors: {len(results['errors'])}")
    
    # Write summary to file
    with open('deadline_summary.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
