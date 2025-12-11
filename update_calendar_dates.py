#!/usr/bin/env python3
"""
Update all day branch READMEs with actual calendar dates and deadlines
"""
from datetime import datetime, timedelta
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
    Uses 'first_day' method: Week 1 starts on the 1st of the month.
    """
    month = MONTH_NAMES[month_str.lower()]
    first_day = datetime(year, month, 1)
    
    # Calculate days from first day
    days_offset = (week - 1) * 7 + (day - 1)
    target_date = first_day + timedelta(days=days_offset)
    
    # Ensure we don't go into next month
    next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    if target_date >= next_month:
        last_day = (next_month - timedelta(days=1)).day
        target_date = datetime(year, month, last_day)
    
    return target_date

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

def update_readme_with_calendar(branch_name, date_info):
    """Update README.md with calendar date and deadline"""
    repo_path = '/Users/misfit.ravi/misfit-ravi'
    readme_path = f'{repo_path}/README.md'
    
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return False
    
    # Create calendar section
    is_past_deadline = datetime.now() > date_info['deadline']
    status_emoji = '🔴' if is_past_deadline else '🟢'
    status_text = 'CLOSED' if is_past_deadline else 'ACTIVE'
    
    calendar_section = f"""
---

## 📅 Calendar Information

**Actual Date:** {date_info['date_formatted']} ({date_info['date_str']})  
**Day of Week:** {date_info['day_name']}  
**Week:** Week {date_info['week']} of {date_info['month_name']} {date_info['year']}  
**Deadline:** {date_info['deadline_formatted']} ({date_info['deadline_str']})

---

## ⏰ Branch Status

**Status:** {status_emoji} {status_text}  
**Deadline:** {date_info['deadline_formatted']}  
**Time Remaining:** {get_time_remaining(date_info['deadline'])}  

> **Note:** This branch closes at 11:59 PM IST (Mumbai Time) on {date_info['date_formatted']}. After the deadline, the branch remains visible and accessible but is marked as closed. Content can still be viewed and indexed by search engines.

---
"""
    
    # Remove existing calendar/deadline sections if present
    content = re.sub(r'---\s*\n## 📅 Calendar Information.*?## ⏰ Branch Status.*?---', '', content, flags=re.DOTALL)
    content = re.sub(r'\*\*Actual Date:\*\*.*?\n', '', content)
    content = re.sub(r'\*\*Day of Week:\*\*.*?\n', '', content)
    content = re.sub(r'\*\*Week Number:\*\*.*?\n', '', content)
    content = re.sub(r'\*\*Month:\*\*.*?\n', '', content)
    
    # Insert after header (find first # line)
    lines = content.split('\n')
    insert_index = 1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            insert_index = i + 1
            # Skip any existing date info lines
            while insert_index < len(lines) and (
                lines[insert_index].startswith('**Actual Date:') or
                lines[insert_index].startswith('**Day of Week:') or
                lines[insert_index].startswith('**Week Number:') or
                lines[insert_index].startswith('**Month:') or
                lines[insert_index].strip() == ''
            ):
                insert_index += 1
            break
    
    lines.insert(insert_index, calendar_section.strip())
    content = '\n'.join(lines)
    
    # Update header to include date
    old_header_pattern = r'# Misfit Ravi - .*?Content Plan'
    new_header = f"# Misfit Ravi - {date_info['date_formatted']} ({date_info['day_name']}) Content Plan"
    content = re.sub(old_header_pattern, new_header, content)
    
    try:
        with open(readme_path, 'w') as f:
            f.write(content)
        return True
    except:
        return False

def update_all_branches():
    """Update all day branches with calendar dates"""
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    repo_path = '/Users/misfit.ravi/misfit-ravi'
    years = [2026, 2027, 2028, 2029]
    
    success = 0
    failed = 0
    
    print("=" * 80)
    print("UPDATING ALL DAY BRANCHES WITH CALENDAR DATES AND DEADLINES")
    print("=" * 80)
    print()
    
    for year in years:
        print(f"Processing {year}...")
        for month in months:
            for week in range(1, 5):
                for day in range(1, 8):
                    branch_name = f"{year}-{month}-week{week}-day{day}"
                    
                    try:
                        # Calculate date
                        date_obj = get_calendar_date(year, month, week, day)
                        deadline = date_obj.replace(hour=23, minute=59, second=59)
                        
                        date_info = {
                            'year': year,
                            'month': month,
                            'month_name': MONTH_NAMES_FULL[month],
                            'week': week,
                            'day': day,
                            'day_name': date_obj.strftime('%A'),
                            'date': date_obj,
                            'date_str': date_obj.strftime('%Y-%m-%d'),
                            'date_formatted': date_obj.strftime('%B %d, %Y'),
                            'deadline': deadline,
                            'deadline_str': deadline.strftime('%Y-%m-%d %H:%M:%S'),
                            'deadline_formatted': deadline.strftime('%B %d, %Y at 11:59 PM')
                        }
                        
                        # Checkout branch
                        result = subprocess.run(['git', 'checkout', branch_name], 
                                              capture_output=True, text=True, cwd=repo_path)
                        if result.returncode != 0:
                            failed += 1
                            continue
                        
                        # Update README
                        if update_readme_with_calendar(branch_name, date_info):
                            subprocess.run(['git', 'add', 'README.md'], cwd=repo_path)
                            commit_msg = f"Add calendar date and deadline: {date_info['date_formatted']}"
                            subprocess.run(['git', 'commit', '-m', commit_msg], 
                                         capture_output=True, cwd=repo_path)
                            success += 1
                        else:
                            failed += 1
                        
                        if success % 50 == 0:
                            print(f"  Updated {success} branches...")
                    
                    except Exception as e:
                        print(f"  ❌ Error: {branch_name}: {e}")
                        failed += 1
        
        print(f"  ✅ {year}: {success} updated")
    
    print()
    print("=" * 80)
    print(f"SUMMARY: ✅ {success}/1344 | ❌ {failed}/1344")
    print("=" * 80)
    
    return success, failed

if __name__ == '__main__':
    update_all_branches()
