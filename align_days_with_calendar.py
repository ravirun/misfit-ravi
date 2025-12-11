#!/usr/bin/env python3
"""
Align all day branches with actual calendar dates
Maps 4 years × 12 months × 4 weeks × 7 days to real calendar dates
"""
import subprocess
from datetime import datetime, timedelta
import calendar

def get_first_monday_of_month(year, month):
    """Get the first Monday of a given month"""
    first_day = datetime(year, month, 1)
    # Find the first Monday
    days_until_monday = (7 - first_day.weekday()) % 7
    if days_until_monday == 0 and first_day.weekday() != 0:
        days_until_monday = 7
    first_monday = first_day + timedelta(days=days_until_monday)
    return first_monday

def get_actual_dates_for_month(year, month):
    """Get actual calendar dates for a month, starting from first Monday"""
    first_monday = get_first_monday_of_month(year, month)
    dates = []
    current_date = first_monday
    
    # Generate 28 days (4 weeks × 7 days)
    for week in range(4):
        week_dates = []
        for day in range(7):
            week_dates.append(current_date)
            current_date += timedelta(days=1)
        dates.append(week_dates)
    
    return dates

def update_day_branch_with_date(year, month_abbr, week_num, day_num, actual_date):
    """Update a day branch's README with actual calendar date"""
    month_names = {
        'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
        'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
        'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
    }
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    branch_name = f"{year}-{month_abbr}-week{week_num}-day{day_num}"
    
    # Checkout branch
    result = subprocess.run(['git', 'checkout', branch_name], 
                          capture_output=True, text=True, cwd='/Users/misfit.ravi/misfit-ravi')
    if result.returncode != 0:
        return False
    
    # Read current README
    try:
        with open('/Users/misfit.ravi/misfit-ravi/README.md', 'r') as f:
            content = f.read()
    except:
        return False
    
    # Update the header with actual date
    month_name = month_names[month_abbr]
    day_name = day_names[day_num - 1]
    date_str = actual_date.strftime('%B %d, %Y')
    date_short = actual_date.strftime('%Y-%m-%d')
    
    # Update header line
    old_header = f"# Misfit Ravi - {month_name} {year}, Week {week_num}, {day_name} Content Plan"
    new_header = f"# Misfit Ravi - {date_str} ({day_name}) Content Plan"
    
    if old_header in content:
        content = content.replace(old_header, new_header)
    else:
        # Try alternative format
        alt_header = f"# Misfit Ravi - {month_name} {year}, Week {week_num}, {day_name}"
        if alt_header in content:
            content = content.replace(alt_header, new_header)
    
    # Add date information after the header
    date_section = f"\n**Actual Date:** {date_str} ({date_short})  \n**Day of Week:** {day_name}  \n**Week Number:** {week_num}  \n**Month:** {month_name} {year}\n"
    
    # Insert after the header (after first line)
    lines = content.split('\n')
    if len(lines) > 1:
        lines.insert(1, date_section.strip())
        content = '\n'.join(lines)
    
    # Update footer with actual date
    old_footer = f"*{day_name}, Week {week_num}, {month_name} {year} -"
    new_footer = f"*{date_str} ({day_name}) -"
    content = content.replace(old_footer, new_footer)
    
    # Write updated README
    with open('/Users/misfit.ravi/misfit-ravi/README.md', 'w') as f:
        f.write(content)
    
    # Commit changes
    subprocess.run(['git', 'add', 'README.md'], cwd='/Users/misfit.ravi/misfit-ravi')
    commit_msg = f"Add actual calendar date {date_short} to {branch_name}"
    subprocess.run(['git', 'commit', '-m', commit_msg], 
                 capture_output=True, cwd='/Users/misfit.ravi/misfit-ravi')
    
    return True

def align_all_days_with_calendar():
    """Align all day branches with actual calendar dates"""
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month_numbers = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    years = [2026, 2027, 2028, 2029]
    
    total_updated = 0
    total_failed = 0
    
    print("=" * 80)
    print("ALIGNING DAY BRANCHES WITH ACTUAL CALENDAR DATES")
    print("=" * 80)
    print()
    
    for year in years:
        print(f"Processing {year}...")
        for month_abbr in months:
            month_num = month_numbers[month_abbr]
            
            # Get actual dates for this month
            actual_dates = get_actual_dates_for_month(year, month_num)
            
            for week_idx in range(4):
                week_num = week_idx + 1
                for day_idx in range(7):
                    day_num = day_idx + 1
                    actual_date = actual_dates[week_idx][day_idx]
                    
                    if update_day_branch_with_date(year, month_abbr, week_num, day_num, actual_date):
                        total_updated += 1
                    else:
                        total_failed += 1
                    
                    if total_updated % 50 == 0:
                        print(f"  Updated {total_updated} branches...")
        
        print(f"  ✅ Completed {year}: {total_updated} branches updated")
    
    print()
    print("=" * 80)
    print(f"SUMMARY:")
    print(f"  ✅ Updated: {total_updated}/1344 day branches")
    print(f"  ❌ Failed: {total_failed}/1344 day branches")
    print("=" * 80)
    
    return total_updated, total_failed

if __name__ == '__main__':
    align_all_days_with_calendar()
