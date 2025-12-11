# Calendar Alignment System

## Overview

All day branches (1,344 total) have been aligned with real calendar dates and include deadline timers. Each branch closes at 11:59 PM on its assigned date but remains visible and accessible for search engines.

---

## How It Works

### Date Calculation

- **Method:** Week 1 starts on the 1st day of each month (regardless of weekday)
- **Formula:** `Date = First day of month + (Week - 1) × 7 + (Day - 1)`
- **Example:** `2026-jan-week1-day1` = January 1, 2026 (or first available day)

### Deadline System

- **Deadline:** 11:59 PM IST (Mumbai Time, UTC+5:30) on the assigned calendar date
- **Timezone:** All deadlines use Indian Standard Time (IST) / Mumbai time
- **Status:** 
  - 🟢 **ACTIVE** - Before deadline (Mumbai time)
  - 🔴 **CLOSED** - After deadline (Mumbai time)
- **Visibility:** Branches remain visible and accessible after deadline
- **Search Engine:** All branches remain indexed by Google and other search engines

---

## README Structure

Each day branch README now includes:

```markdown
## 📅 Calendar Information

**Actual Date:** January 1, 2026 (2026-01-01)
**Day of Week:** Thursday
**Week:** Week 1 of January 2026
**Deadline:** January 1, 2026 at 11:59 PM (2026-01-01 23:59:59)

## ⏰ Branch Status

**Status:** 🟢 ACTIVE / 🔴 CLOSED
**Deadline:** January 1, 2026 at 11:59 PM
**Time Remaining:** X days, X hours, X minutes

> **Note:** This branch closes at 11:59 PM on [date]. After the deadline, 
> the branch remains visible and accessible but is marked as closed. 
> Content can still be viewed and indexed by search engines.
```

---

## Automation

### GitHub Actions Workflow

A GitHub Actions workflow (`.github/workflows/branch_deadline_checker.yml`) runs hourly to:

1. Check all day branches for deadline status
2. Update branch status (ACTIVE → CLOSED) when deadline passes
3. Keep branches visible and accessible
4. Maintain search engine indexing

### Manual Update Script

Run `update_calendar_dates.py` to:
- Update all branches with calendar dates
- Add deadline information
- Refresh status based on current time

```bash
python3 update_calendar_dates.py
```

---

## Branch Naming Convention

Format: `YYYY-MMM-weekN-dayN`

- **YYYY:** Year (2026-2029)
- **MMM:** Month abbreviation (jan, feb, mar, etc.)
- **weekN:** Week number (1-4)
- **dayN:** Day number (1-7, Monday-Sunday)

Example: `2026-jan-week1-day1` = January 1, 2026 (or first day of January 2026)

---

## Statistics

- **Total Day Branches:** 1,344
- **Years Covered:** 4 (2026-2029)
- **Months Per Year:** 12
- **Weeks Per Month:** 4
- **Days Per Week:** 7
- **All Branches Updated:** ✅ 100%

---

## Calendar Mapping Examples

### 2026 (Nano Creator)
- `2026-jan-week1-day1` → January 1, 2026
- `2026-jan-week1-day7` → January 7, 2026
- `2026-dec-week4-day7` → December 28, 2026

### 2027 (Micro Creator)
- `2027-jan-week1-day1` → January 1, 2027
- `2027-jun-week2-day3` → June 10, 2027

### 2028 (Macro Creator)
- `2028-jan-week1-day1` → January 1, 2028
- `2028-dec-week4-day7` → December 28, 2028

### 2029 (Mega Creator)
- `2029-jan-week1-day1` → January 1, 2029
- `2029-dec-week4-day7` → December 28, 2029

---

## Features

✅ **Real Calendar Dates** - Each branch mapped to actual calendar date  
✅ **Deadline Timers** - Automatic closure at 11:59 PM  
✅ **Status Tracking** - Visual indicators (🟢 ACTIVE / 🔴 CLOSED)  
✅ **Search Engine Friendly** - All branches remain indexed  
✅ **Automated Updates** - GitHub Actions checks hourly  
✅ **Time Remaining** - Dynamic countdown until deadline  
✅ **Always Visible** - Branches never deleted, only marked closed  

---

## Usage

### Check a Branch's Deadline

```bash
git checkout 2026-jan-week1-day1
cat README.md | grep -A 5 "Branch Status"
```

### Update All Branches

```bash
python3 update_calendar_dates.py
git push origin --all
```

### View Calendar Mapping

```python
from calendar_alignment import get_date_for_branch

date_info = get_date_for_branch('2026-jan-week1-day1')
print(f"Date: {date_info['date_formatted']}")
print(f"Deadline: {date_info['deadline_formatted']}")
```

---

## Notes

- Branches are **never deleted** - they remain visible forever
- Status changes from ACTIVE to CLOSED automatically
- Search engines can index all branches regardless of status
- Content remains accessible even after deadline
- Deadline is informational - no actual branch protection is applied
- GitHub Actions workflow updates status hourly

---

*Last Updated: $(date)*
