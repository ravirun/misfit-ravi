#!/usr/bin/env python3
"""
Calendar Alignment Function
Maps all day branches (4 years × 12 months × 4 weeks × 7 days) to real calendar dates
and updates README files with actual dates and deadlines
"""
from datetime import datetime, timedelta
import calendar
import subprocess
import re

MONTH_NAMES = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

MONTH_NAMES_FULL = {
    'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
    'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
    'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
}

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_calendar_date(year, month_str, week, day, week_start='first_day'):
    """
    Calculate the actual calendar date for a given year, month, week, and day.
    
    Args:
        year (int): Year (2026-2029)
        month_str (str): Month abbreviation ('jan', 'feb', etc.)
        week (int): Week number (1-4)
        day (int): Day number (1-7, where 1=Monday, 7=Sunday)
        week_start (str): 
            - 'first_day': Week 1 starts on the 1st of the month (regardless of weekday)
            - 'monday': Week 1 starts on the first Monday of the month
            - 'sunday': Week 1 starts on the first Sunday of the month
    
    Returns:
        datetime: The actual calendar date
    """
    month = MONTH_NAMES[month_str.lower()]
    
    # Get first day of the month
    first_day = datetime(year, month, 1)
    
    if week_start == 'first_day':
        # Week 1 starts on the 1st of the month, regardless of weekday
        # Calculate days from first day
        days_offset = (week - 1) * 7 + (day - 1)
        target_date = first_day + timedelta(days=days_offset)
        
        # Ensure we don't go into next month
        next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        if target_date >= next_month:
            # If we exceed the month, use the last day of the month
            last_day = (next_month - timedelta(days=1)).day
            target_date = datetime(year, month, last_day)
        
        return target_date
    
    elif week_start == 'monday':
        # Week 1 starts on the first Monday of the month
        # Find first Monday
        first_monday = first_day
        while first_monday.weekday() != 0:  # 0 = Monday
            first_monday += timedelta(days=1)
        
        # Calculate days from first Monday
        days_offset = (week - 1) * 7 + (day - 1)
        target_date = first_monday + timedelta(days=days_offset)
        
        # Ensure we don't go into next month
        next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        if target_date >= next_month:
            last_day = (next_month - timedelta(days=1)).day
            target_date = datetime(year, month, last_day)
        
        return target_date
    
    elif week_start == 'sunday':
        # Week 1 starts on the first Sunday of the month
        # Find first Sunday
        first_sunday = first_day
        while first_sunday.weekday() != 6:  # 6 = Sunday
            first_sunday += timedelta(days=1)
        
        # Calculate days from first Sunday
        days_offset = (week - 1) * 7 + (day - 1)
        target_date = first_sunday + timedelta(days=days_offset)
        
        # Ensure we don't go into next month
        next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        if target_date >= next_month:
            last_day = (next_month - timedelta(days=1)).day
            target_date = datetime(year, month, last_day)
        
        return target_date
    
    else:
        raise ValueError(f"Invalid week_start: {week_start}")

def get_date_for_branch(branch_name, week_start='first_day'):
    """
    Extract date information from branch name and return calendar date.
    
    Args:
        branch_name (str): Branch name like '2026-jan-week1-day1'
        week_start (str): 'first_day', 'monday', or 'sunday'
    
    Returns:
        dict: Contains date info and datetime object
    """
    parts = branch_name.split('-')
    if len(parts) != 4:
        raise ValueError(f"Invalid branch name format: {branch_name} (expected format: YYYY-mon-weekN-dayN)")
    
    year = int(parts[0])
    month_str = parts[1]
    week_str = parts[2]  # 'week1'
    day_str = parts[3]   # 'day1'
    
    week = int(week_str.replace('week', ''))
    day = int(day_str.replace('day', ''))
    
    date_obj = get_calendar_date(year, month_str, week, day, week_start)
    
    return {
        'year': year,
        'month': month_str,
        'month_name': MONTH_NAMES_FULL[month_str],
        'week': week,
        'day': day,
        'day_name': date_obj.strftime('%A'),  # Use actual day of week from date
        'date': date_obj,
        'date_str': date_obj.strftime('%Y-%m-%d'),
        'date_formatted': date_obj.strftime('%B %d, %Y'),
        'day_of_week': date_obj.strftime('%A'),
        'deadline': date_obj.replace(hour=23, minute=59, second=59),  # 11:59 PM
        'deadline_str': date_obj.replace(hour=23, minute=59, second=59).strftime('%Y-%m-%d %H:%M:%S'),
        'deadline_formatted': date_obj.replace(hour=23, minute=59, second=59).strftime('%B %d, %Y at 11:59 PM')
    }

def update_readme_with_calendar_date(branch_name, date_info):
    """
    Update README.md file with calendar date and deadline information.
    
    Args:
        branch_name (str): Branch name
        date_info (dict): Date information from get_date_for_branch()
    
    Returns:
        bool: True if successful, False otherwise
    """
    repo_path = '/Users/misfit.ravi/misfit-ravi'
    readme_path = f'{repo_path}/README.md'
    
    # Read current README
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading README: {e}")
        return False
    
    # Create date and deadline section
    date_section = f"""---

## 📅 Calendar Information

**Actual Date:** {date_info['date_formatted']} ({date_info['date_str']})  
**Day of Week:** {date_info['day_name']}  
**Week:** Week {date_info['week']} of {date_info['month_name']} {date_info['year']}  
**Deadline:** {date_info['deadline_formatted']} ({date_info['deadline_str']})

---

## ⏰ Branch Status

**Status:** {'🔴 CLOSED' if datetime.now() > date_info['deadline'] else '🟢 ACTIVE'}  
**Deadline:** {date_info['deadline_formatted']}  
**Time Remaining:** {get_time_remaining(date_info['deadline'])}  

> **Note:** This branch closes at 11:59 PM on {date_info['date_formatted']}. After the deadline, the branch remains visible and accessible but is marked as closed. Content can still be viewed and indexed by search engines.

---
"""
    
    # Check if date section already exists
    if '## 📅 Calendar Information' in content:
        # Update existing section
        pattern = r'---\s*\n## 📅 Calendar Information.*?## ⏰ Branch Status.*?---'
        replacement = date_section.strip()
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Insert after the header (after first line with #)
        lines = content.split('\n')
        insert_index = 1
        for i, line in enumerate(lines):
            if line.startswith('# '):
                insert_index = i + 1
                break
        
        # Insert date section
        lines.insert(insert_index, date_section.strip())
        content = '\n'.join(lines)
    
    # Update header if needed
    old_header_pattern = r'# Misfit Ravi - .*?Content Plan'
    new_header = f"# Misfit Ravi - {date_info['date_formatted']} ({date_info['day_name']}) Content Plan"
    content = re.sub(old_header_pattern, new_header, content)
    
    # Write updated README
    try:
        with open(readme_path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing README: {e}")
        return False

def get_time_remaining(deadline):
    """Calculate time remaining until deadline"""
    now = datetime.now()
    if now > deadline:
        return "Deadline passed"
    
    delta = deadline - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    else:
        return f"{minutes} minutes"

def update_all_day_branches_with_calendar(years=[2026, 2027, 2028, 2029], week_start='first_day'):
    """
    Update all day branches with calendar dates and deadlines.
    
    Args:
        years (list): List of years to process
        week_start (str): 'first_day', 'monday', or 'sunday'
    
    Returns:
        tuple: (success_count, fail_count)
    """
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    repo_path = '/Users/misfit.ravi/misfit-ravi'
    
    success_count = 0
    fail_count = 0
    
    print("=" * 80)
    print("UPDATING ALL DAY BRANCHES WITH CALENDAR DATES AND DEADLINES")
    print("=" * 80)
    print(f"Week start method: {week_start}")
    print()
    
    for year in years:
        print(f"Processing {year}...")
        for month in months:
            for week in range(1, 5):
                for day in range(1, 8):
                    branch_name = f"{year}-{month}-week{week}-day{day}"
                    
                    try:
                        # Get calendar date info
                        date_info = get_date_for_branch(branch_name, week_start)
                        
                        # Checkout branch
                        result = subprocess.run(['git', 'checkout', branch_name], 
                                              capture_output=True, text=True, cwd=repo_path)
                        if result.returncode != 0:
                            print(f"  ⚠️  Could not checkout {branch_name}")
                            fail_count += 1
                            continue
                        
                        # Update README
                        if update_readme_with_calendar_date(branch_name, date_info):
                            # Commit changes
                            subprocess.run(['git', 'add', 'README.md'], cwd=repo_path)
                            commit_msg = f"Add calendar date and deadline: {date_info['date_formatted']}"
                            subprocess.run(['git', 'commit', '-m', commit_msg], 
                                         capture_output=True, cwd=repo_path)
                            success_count += 1
                        else:
                            fail_count += 1
                        
                        if success_count % 50 == 0:
                            print(f"  Updated {success_count} branches...")
                    
                    except Exception as e:
                        print(f"  ❌ Error processing {branch_name}: {e}")
                        fail_count += 1
        
        print(f"  ✅ Completed {year}: {success_count} branches updated")
    
    print()
    print("=" * 80)
    print(f"SUMMARY:")
    print(f"  ✅ Updated: {success_count}/1344 day branches")
    print(f"  ❌ Failed: {fail_count}/1344 day branches")
    print("=" * 80)
    
    return success_count, fail_count

if __name__ == '__main__':
    # Use 'first_day' to start week 1 on the 1st of each month
    update_all_day_branches_with_calendar(week_start='first_day')
