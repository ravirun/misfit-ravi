#!/usr/bin/env python3
"""
Cross-check function to verify all 2027 month branches have correct topics
"""
import subprocess
import re

# Expected topics for 2027
EXPECTED_TOPICS = {
    'jan': 'How the Internet Manufactures Identity',
    'feb': 'The Economics of Clout: Why Attention Is the New Currency',
    'mar': 'Satire of Modern Dating Culture',
    'apr': 'Why Society Rewards Loud Opinions Over Measured Ones',
    'may': 'The Illusion of "Hustle Culture Success"',
    'jun': 'The Comedy of Corporate Life',
    'jul': 'Why Everyone Wants to Be an Influencer (But No One Wants the Work)',
    'aug': 'The Rise of Algorithm Anxiety',
    'sep': 'The Business of Outrage Machines',
    'oct': 'Why We Fear Boredom (More Than Failure)',
    'nov': 'The Satire of Self-Help Addiction',
    'dec': 'Year 2: How Creating Content Changed My Brain'
}

MONTH_NAMES = {
    'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
    'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
    'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
}

def check_branch_topic(year, month):
    """Check if a branch has the correct topic"""
    branch = f"{year}-{month}"
    
    # Checkout branch
    result = subprocess.run(['git', 'checkout', branch], 
                          capture_output=True, text=True, cwd='/Users/misfit.ravi/misfit-ravi')
    if result.returncode != 0:
        return {'branch': branch, 'status': 'ERROR', 'message': f'Could not checkout: {result.stderr}'}
    
    # Read README.md
    try:
        with open('/Users/misfit.ravi/misfit-ravi/README.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return {'branch': branch, 'status': 'ERROR', 'message': 'README.md not found'}
    
    # Extract topic from README
    # Look for pattern: ### Topic Name
    topic_match = re.search(r'###\s+(.+?)(?:\n|$)', content)
    if not topic_match:
        return {'branch': branch, 'status': 'ERROR', 'message': 'Could not find topic in README'}
    
    actual_topic = topic_match.group(1).strip()
    expected_topic = EXPECTED_TOPICS[month]
    
    # Check if topic matches
    if actual_topic == expected_topic:
        return {'branch': branch, 'status': 'OK', 'topic': actual_topic}
    else:
        return {
            'branch': branch, 
            'status': 'MISMATCH', 
            'expected': expected_topic,
            'actual': actual_topic
        }

def cross_check_2027():
    """Cross-check all 2027 month branches"""
    print("=" * 80)
    print("CROSS-CHECKING 2027 MONTH BRANCHES")
    print("=" * 80)
    print()
    
    results = []
    for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
        result = check_branch_topic(2027, month)
        results.append(result)
    
    # Print results
    print(f"{'Month':<6} {'Branch':<12} {'Status':<12} {'Topic':<60}")
    print("-" * 100)
    
    all_correct = True
    for i, result in enumerate(results, 1):
        month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'][i-1]
        month_name = MONTH_NAMES[month]
        
        if result['status'] == 'OK':
            print(f"{i:<6} {result['branch']:<12} {'✅ OK':<12} {result['topic'][:55]:<60}")
        elif result['status'] == 'MISMATCH':
            all_correct = False
            print(f"{i:<6} {result['branch']:<12} {'❌ WRONG':<12} {result['actual'][:55]:<60}")
            print(f"{'':<6} {'':<12} {'Expected:':<12} {result['expected'][:55]:<60}")
        else:
            all_correct = False
            print(f"{i:<6} {result['branch']:<12} {'❌ ERROR':<12} {result.get('message', 'Unknown error'):<60}")
    
    print()
    print("=" * 80)
    
    # Summary
    correct_count = sum(1 for r in results if r['status'] == 'OK')
    mismatch_count = sum(1 for r in results if r['status'] == 'MISMATCH')
    error_count = sum(1 for r in results if r['status'] == 'ERROR')
    
    print(f"SUMMARY:")
    print(f"  ✅ Correct: {correct_count}/12")
    print(f"  ❌ Mismatches: {mismatch_count}/12")
    print(f"  ⚠️  Errors: {error_count}/12")
    print()
    
    if all_correct:
        print("🎉 All branches have correct topics!")
    else:
        print("⚠️  Some branches need fixing!")
        print()
        print("Branches that need fixing:")
        for result in results:
            if result['status'] == 'MISMATCH':
                print(f"  - {result['branch']}: Expected '{result['expected']}', got '{result['actual']}'")
            elif result['status'] == 'ERROR':
                print(f"  - {result['branch']}: {result.get('message', 'Unknown error')}")
    
    print("=" * 80)
    
    return all_correct

if __name__ == '__main__':
    cross_check_2027()

