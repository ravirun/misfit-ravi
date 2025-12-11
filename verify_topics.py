#!/usr/bin/env python3
"""
Cross-check script to verify all month branches have the correct content topics
"""
import subprocess
import re
import sys

# Expected topics for 2026
EXPECTED_2026_TOPICS = {
    1: "Why Modern Life Makes No Sense (But We Pretend It Does)",
    2: "The Satire of Productivity Culture",
    3: "Social Media: The World's Greatest Unpaid Internship",
    4: "How Everyone Thinks They're \"Different\" (But We're All the Same)",
    5: "Why Adults Are Just Children With Wi-Fi",
    6: "The Psychology Behind Overthinking Everything",
    7: "The Rise of Fake Experts (Including Me)",
    8: "Why We Love Outrage More Than Solutions",
    9: "The Myth of \"Finding Yourself\"",
    10: "Why Our Attention Span Is Now Shorter Than a Goldfish",
    11: "The Silent Comedy of Human Behavior",
    12: "What I Learned Trying to Be a Creator for 12 Months"
}

# Month abbreviations
MONTHS = {
    1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
    7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
}

def get_current_branch():
    """Get the current git branch"""
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                          capture_output=True, text=True)
    return result.stdout.strip()

def checkout_branch(branch_name):
    """Checkout a git branch"""
    result = subprocess.run(['git', 'checkout', branch_name], 
                          capture_output=True, text=True)
    return result.returncode == 0

def read_readme():
    """Read the README.md file"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def extract_topic(readme_content):
    """Extract the content topic from README"""
    if not readme_content:
        return None
    
    # Look for the topic after "## Content Topic" and "###"
    pattern = r'## Content Topic\s*\n\s*###\s*(.+?)\s*\n'
    match = re.search(pattern, readme_content, re.MULTILINE)
    
    if match:
        return match.group(1).strip()
    
    # Alternative pattern: look for "###" followed by topic
    pattern2 = r'###\s+(.+?)\s*\n'
    matches = re.findall(pattern2, readme_content)
    # Usually the first ### after Content Topic is the topic
    for i, line in enumerate(readme_content.split('\n')):
        if 'Content Topic' in line:
            # Look for next ###
            for j in range(i+1, min(i+10, len(readme_content.split('\n')))):
                next_line = readme_content.split('\n')[j]
                if next_line.strip().startswith('###'):
                    topic = next_line.replace('###', '').strip()
                    return topic
    
    return None

def normalize_topic(topic):
    """Normalize topic for comparison (remove extra spaces, handle quotes)"""
    if not topic:
        return ""
    # Remove extra whitespace
    topic = ' '.join(topic.split())
    # Normalize quotes
    topic = topic.replace('"', '"').replace('"', '"')
    topic = topic.replace('"', '"').replace('"', '"')
    return topic.strip()

def verify_year(year, expected_topics):
    """Verify all month branches for a given year"""
    print(f"\n{'='*70}")
    print(f"Verifying {year} Month Branches")
    print(f"{'='*70}\n")
    
    original_branch = get_current_branch()
    results = []
    all_correct = True
    
    for month_num, month_abbr in MONTHS.items():
        branch_name = f"{year}-{month_abbr}"
        expected_topic = expected_topics.get(month_num, "NOT FOUND")
        
        print(f"Checking {branch_name}...", end=" ")
        
        # Checkout branch
        if not checkout_branch(branch_name):
            print(f"❌ FAILED - Cannot checkout branch")
            results.append((branch_name, month_num, None, expected_topic, False, "Cannot checkout"))
            all_correct = False
            continue
        
        # Read README
        readme_content = read_readme()
        if not readme_content:
            print(f"❌ FAILED - README.md not found")
            results.append((branch_name, month_num, None, expected_topic, False, "README not found"))
            all_correct = False
            continue
        
        # Extract topic
        actual_topic = extract_topic(readme_content)
        if not actual_topic:
            print(f"❌ FAILED - Cannot extract topic")
            results.append((branch_name, month_num, None, expected_topic, False, "Cannot extract topic"))
            all_correct = False
            continue
        
        # Normalize and compare
        normalized_actual = normalize_topic(actual_topic)
        normalized_expected = normalize_topic(expected_topic)
        
        if normalized_actual == normalized_expected:
            print(f"✅ CORRECT")
            results.append((branch_name, month_num, actual_topic, expected_topic, True, None))
        else:
            print(f"❌ MISMATCH")
            print(f"   Expected: {expected_topic}")
            print(f"   Actual:   {actual_topic}")
            results.append((branch_name, month_num, actual_topic, expected_topic, False, "Topic mismatch"))
            all_correct = False
    
    # Return to original branch
    checkout_branch(original_branch)
    
    return results, all_correct

def print_summary(results, year):
    """Print summary of verification results"""
    print(f"\n{'='*70}")
    print(f"Summary for {year}")
    print(f"{'='*70}\n")
    
    correct_count = sum(1 for _, _, _, _, is_correct, _ in results if is_correct)
    total_count = len(results)
    
    print(f"Total branches checked: {total_count}")
    print(f"✅ Correct: {correct_count}")
    print(f"❌ Incorrect: {total_count - correct_count}\n")
    
    if correct_count < total_count:
        print("Issues found:")
        print("-" * 70)
        for branch_name, month_num, actual, expected, is_correct, error in results:
            if not is_correct:
                month_name = MONTHS[month_num].upper()
                print(f"\n{month_name} ({branch_name}):")
                print(f"  Expected: {expected}")
                if actual:
                    print(f"  Actual:   {actual}")
                if error:
                    print(f"  Error:    {error}")
        print()

if __name__ == "__main__":
    print("=" * 70)
    print("Content Topic Verification Script")
    print("=" * 70)
    
    # Verify 2026
    results_2026, all_correct_2026 = verify_year(2026, EXPECTED_2026_TOPICS)
    print_summary(results_2026, 2026)
    
    # Exit with appropriate code
    if all_correct_2026:
        print("✅ All 2026 branches have correct topics!")
        sys.exit(0)
    else:
        print("❌ Some branches have incorrect topics. Please review above.")
        sys.exit(1)
