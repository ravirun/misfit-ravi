#!/usr/bin/env python3
"""
Update README files for all week branches with weekly topics
"""
import subprocess
import re

# Weekly topics organized by year and month
WEEKLY_TOPICS = {
    2026: {
        'jan': {
            'week1': 'The Illogic of Daily Routines (Why humans love self-imposed nonsense)',
            'week2': 'Why Modern Work Culture Is Basically Performance Art',
            'week3': 'The Paradox of Having Everything Yet Feeling Lost',
            'week4': 'How Society Normalizes Absurdity (A comedic breakdown)'
        },
        'feb': {
            'week1': 'Why "To-Do Lists" Are Now Therapy Sessions',
            'week2': 'The Myth of the Perfect Morning Routine',
            'week3': 'Productivity Gurus vs Reality',
            'week4': 'Why Rest Feels Illegal in 2026'
        },
        'mar': {
            'week1': 'Creating Content for Free: The New Corporate Ladder',
            'week2': 'Why We Treat Algorithms Like Gods',
            'week3': 'Influencer Culture: Glamorous or Digital Labor?',
            'week4': 'Posting for Validation: A Global Hobby'
        },
        'apr': {
            'week1': 'The Identity Crisis of the Internet Generation',
            'week2': 'Why Individuality Has Become a Copy-Paste Template',
            'week3': 'Stereotypes We Pretend We Don\'t Fit (But Do)',
            'week4': 'Everyone\'s Main Character Syndrome Explained'
        },
        'may': {
            'week1': 'Why Adulthood Is Just Pretending You Know Things',
            'week2': 'How Adults Throw Tantrums… Professionally',
            'week3': 'The Comedy of "Being Responsible"',
            'week4': 'Why Our Inner Child Runs Most Decisions'
        },
        'jun': {
            'week1': 'How to Overthink the Smallest Possible Problem',
            'week2': 'The Spiral of Imaginary Scenarios',
            'week3': 'Why Anxiety Loves Modern Life',
            'week4': 'The Overthinker\'s Guide to Ruining a Good Day'
        },
        'jul': {
            'week1': 'How Everyone Becomes an Expert After One YouTube Video',
            'week2': 'The Epidemic of Certainty Without Knowledge',
            'week3': 'Why Social Media Rewards Confidence Over Competence',
            'week4': 'My Confession: I\'m Learning as I Go (Satirically)'
        },
        'aug': {
            'week1': 'Outrage as Entertainment',
            'week2': 'Why Calm Discussions Never Go Viral',
            'week3': 'How Algorithms Profit From Your Anger',
            'week4': 'The Comedy of Arguing With Strangers Online'
        },
        'sep': {
            'week1': 'Why Finding Yourself Is a Lifetime Side-Quest',
            'week2': 'The Self-Discovery Industrial Complex',
            'week3': 'Why You Don\'t Need to "Fix Your Life" to Exist',
            'week4': 'Satire of People Who Reinvent Themselves Monthly'
        },
        'oct': {
            'week1': 'The 8-Second Brain: How We Got Here',
            'week2': 'Multitasking: The Lie We Tell Ourselves',
            'week3': 'The Scrolling Addiction We Pretend Not to Have',
            'week4': 'Why Boredom Is Now a Luxury'
        },
        'nov': {
            'week1': 'The Funny Things Humans Do Without Realizing',
            'week2': 'Social Norms That Make No Logical Sense',
            'week3': 'Why We Crave Validation From People We Don\'t Know',
            'week4': 'The Awkwardness of Being Human (A Satirical Mirror)'
        },
        'dec': {
            'week1': 'What I Thought Creating Would Be vs Reality',
            'week2': 'How Posting Every Week Changed My Identity',
            'week3': 'Lessons From My Best & Worst Performing Videos',
            'week4': 'A Satirical but Honest Review of My First Year'
        }
    },
    2027: {
        'jan': {
            'week1': 'The Algorithmic Identity Crisis: Who Are You Without the Feed?',
            'week2': 'Why People Perform Versions of Themselves Online',
            'week3': 'How Aesthetic Trends Replace Real Personality',
            'week4': 'The Digital Masks We Wear (Satirical Breakdown)'
        },
        'feb': {
            'week1': 'How Clout Became More Valuable Than Credentials',
            'week2': 'The Hidden Economy: Likes, Followers, Social Credit',
            'week3': 'Why People Chase Virality Like a Lottery Ticket',
            'week4': 'The Attention Marketplace: Winners, Losers, and Exploiters'
        },
        'mar': {
            'week1': 'Dating Apps: The Gamification of Human Emotion',
            'week2': 'Why "Situationships" Are Just Confusion With Branding',
            'week3': 'The Illusion of Infinite Options',
            'week4': 'Why Modern Romance Feels Like Customer Service'
        },
        'apr': {
            'week1': 'Outrage > Logic: How We Reward Noise, Not Nuance',
            'week2': 'The Performative Expert: Confidence Without Competence',
            'week3': 'Why Nuanced Takes Don\'t Go Viral',
            'week4': 'The Entertainment Value of Bad Opinions'
        },
        'may': {
            'week1': 'Why Hustle Culture Sells the Dream (Not the Reality)',
            'week2': 'Productivity As a Personality Disorder',
            'week3': 'The Myth of the Self-Made Creator',
            'week4': 'The Satire of "Rise and Grind" Culture'
        },
        'jun': {
            'week1': 'Corporate Jargon: Saying Nothing With Big Words',
            'week2': 'Meetings That Could Have Been a Message',
            'week3': 'The Psychology of Acting Busy',
            'week4': 'Why Promotions Don\'t Equal Purpose'
        },
        'jul': {
            'week1': 'The Fantasy vs Reality of Creator Life',
            'week2': 'The Invisible Labor Behind "Effortless" Content',
            'week3': 'Why Everyone Wants Fame Without Responsibility',
            'week4': 'The Entitlement of Overnight Success Culture'
        },
        'aug': {
            'week1': 'Why We Care So Much About Numbers That Don\'t Exist in Real Life',
            'week2': 'The Fear of Being Ignored by the Algorithm',
            'week3': 'Posting Anxiety: The New Social Disorder',
            'week4': 'Are We Serving the Algorithm or Is It Serving Us?'
        },
        'sep': {
            'week1': 'How Outrage Became a Billion-Dollar Industry',
            'week2': 'Why Anger Travels Faster Than Truth',
            'week3': 'The Psychology of Consuming Controversy',
            'week4': 'How Media Companies Profit From Division'
        },
        'oct': {
            'week1': 'The Death of Stillness in a Hyperstimulated World',
            'week2': 'Why We Constantly Need Entertainment',
            'week3': 'The Art of Doing Nothing (And Why It Feels Illegal)',
            'week4': 'Boredom as a Superpower in the Attention Age'
        },
        'nov': {
            'week1': 'Why People Consume Self-Help Instead of Helping Themselves',
            'week2': 'The Endless Cycle of "Fixing" Yourself',
            'week3': 'Motivation Content: Fast Food for the Mind',
            'week4': 'The Comedy Behind "New Year, New Me" Culture'
        },
        'dec': {
            'week1': 'How Constant Creation Reshaped My Identity',
            'week2': 'What I Learned From Growing 10k → 100k',
            'week3': 'My Most Surprising Discoveries About the Audience',
            'week4': 'The Psychological Cost (and Reward) of Year 2'
        }
    },
    2028: {
        'jan': {
            'week1': 'A Timeline of Human Mistakes (From Fire to TikTok)',
            'week2': 'Why Humans Outsmart Themselves More Than Nature Does',
            'week3': 'How Our Biggest Innovations Started as Dumb Ideas',
            'week4': 'The Evolution of Foolishness: Are We Getting Smarter or Just Louder?'
        },
        'feb': {
            'week1': 'The Hypocrisy of "Do What You Love" Culture',
            'week2': 'How Society Worships Success While Ignoring the System',
            'week3': 'Why We Demand Honesty but Reward Performance',
            'week4': 'The Comedy of Saying One Thing and Doing Another'
        },
        'mar': {
            'week1': 'How Platforms Monetize Your Mind',
            'week2': 'Why Attention Is More Valuable Than Money',
            'week3': 'The Trap of Constant Notifications',
            'week4': 'How We All Became Workers in the Attention Factory'
        },
        'apr': {
            'week1': 'Why Politics Resembles a Netflix Series',
            'week2': 'The Performance Art of Public Debates',
            'week3': 'How Politicians Market Themselves Like Influencers',
            'week4': 'Why Every Side Thinks They\'re the Main Character'
        },
        'may': {
            'week1': 'The Hype Cycle: How Tech News Became Pop Culture',
            'week2': 'Why We Celebrate Ideas More Than Outcomes',
            'week3': 'The Theater of Product Launches',
            'week4': 'Innovation as Spectacle: Are We Innovating or Performing?'
        },
        'jun': {
            'week1': 'The Patterns of Human Mistakes Through History',
            'week2': 'How Technology Amplifies Human Flaws',
            'week3': 'Why Our Worst Decisions Come From Good Intentions',
            'week4': 'A Satirical Forecast of 2050'
        },
        'jul': {
            'week1': 'The Psychology Behind Viral Behavior',
            'week2': 'Why Outrage Spreads Faster Than Joy',
            'week3': 'The Anatomy of a "Perfect" Viral Clip',
            'week4': 'Why Virality Feels Random (But Isn\'t)'
        },
        'aug': {
            'week1': 'The Human Biases AI Will Inherit',
            'week2': 'Why Automation Won\'t Fix Human Nature',
            'week3': 'The Comedy of Humans Trying to Outsmart Machines',
            'week4': 'AI in 2050: Smarter Tools, Same Dumb Decisions'
        },
        'sep': {
            'week1': 'How Online Status Is Manufactured',
            'week2': 'Why Followers Equal Social Power',
            'week3': 'The Invisible Ranking System of Digital Life',
            'week4': 'The Satire of Clout-Based Social Classes'
        },
        'oct': {
            'week1': 'Why We Buy Things We Don\'t Need',
            'week2': 'The Psychology of Retail Therapy',
            'week3': 'How Advertising Manipulates Identity',
            'week4': 'The Humor in Chasing Material Happiness'
        },
        'nov': {
            'week1': 'The Silliest Trends of the Decade',
            'week2': 'Cultural Obsessions That Won\'t Age Well',
            'week3': 'How the 2020s Will Look in Textbooks',
            'week4': 'A Satirical Time Capsule of Our Era'
        },
        'dec': {
            'week1': 'My Biggest Creative Wins of the Year',
            'week2': 'My Funniest Miscalculations About the Internet',
            'week3': 'What Surprised Me as a 100k–1M Creator',
            'week4': 'Honest Lessons From 3 Years of Creating'
        }
    },
    2029: {
        'jan': {
            'week1': 'Why Humans Are Obsessed With Power (Even in Group Chats)',
            'week2': 'The Illusion of Control: Why Power Is Mostly Performance',
            'week3': 'How People Change When They Get Power (and Why It\'s Predictable)',
            'week4': 'The Comedy of Power Struggles in Everyday Life'
        },
        'feb': {
            'week1': 'Why Humans Never Learn From History',
            'week2': 'The Patterns Behind Repeating the Same Mistakes',
            'week3': 'How Good Intentions Create Bad Outcomes',
            'week4': 'A Satirical Guide to Avoiding Mistakes (That We\'ll Ignore Anyway)'
        },
        'mar': {
            'week1': 'Why Media Doesn\'t Show Reality — It Manufactures It',
            'week2': 'How Narratives Are Engineered to Influence Behavior',
            'week3': 'Why Humans Believe Anything With Enough Repetition',
            'week4': 'The Satire of Trusting Screens More Than People'
        },
        'apr': {
            'week1': 'What the Next 50 Years Might Look Like (If Humans Stay the Same)',
            'week2': 'Why Future Problems Will Look Suspiciously Familiar',
            'week3': 'A Comedic Map of Future Social Norms',
            'week4': 'How Humor Helps Us Survive What\'s Coming'
        },
        'may': {
            'week1': 'The Psychology Behind Blind Loyalty',
            'week2': 'How Charisma Beats Competence Every Time',
            'week3': 'Why Followers Project Their Dreams Onto Leaders',
            'week4': 'A Satirical Portrait of the "Perfect" Modern Leader'
        },
        'jun': {
            'week1': 'Why Comedy Exists in Every Culture',
            'week2': 'The Science of Why Pain = Funny (Sometimes)',
            'week3': 'Humor as a Coping Mechanism for Human Chaos',
            'week4': 'Why Difficult Truths Are More Acceptable When Funny'
        },
        'jul': {
            'week1': 'How Fame Became a Business Model',
            'week2': 'Why Attention Is More Monetizable Than Talent',
            'week3': 'The Financial Lifecycle of a Celebrity',
            'week4': 'The Comedy of Chasing Fame for Money'
        },
        'aug': {
            'week1': 'The Warning Signs of a Declining Society',
            'week2': 'How Societies Self-Destruct in Slow Motion',
            'week3': 'Why Collapse Always Looks Obvious in Retrospect',
            'week4': 'A Satirical Toolkit for "Avoiding Collapse"'
        },
        'sep': {
            'week1': 'Every Tech Innovation Ever: Two Steps Forward, One Disaster Back',
            'week2': 'Why Humans Outsource Thinking to Machines',
            'week3': 'The Unintended Consequences of "Progress"',
            'week4': 'A Comedic Prediction of the Problems Tech Will Create Next'
        },
        'oct': {
            'week1': 'Why Humans Haven\'t Evolved Emotionally Since the Stone Age',
            'week2': 'Our Funniest Cognitive Biases',
            'week3': 'How Evolution Built Us for Survival, Not Happiness',
            'week4': 'A Satirical Look at How We Might Evolve Next'
        },
        'nov': {
            'week1': 'Trends We Love Today That Will Be Embarrassing Later',
            'week2': 'The Problems We Left for Future Humans to Fix',
            'week3': 'What History Class Might Teach About the 2020s–2030s',
            'week4': 'A Satirical Letter to the Future Generation'
        },
        'dec': {
            'week1': 'Part 1: The Cultural Forecasts I Made — And What Actually Happened',
            'week2': 'Part 2: The Science Behind Predicting Behavior Through Comedy',
            'week3': 'Part 3: How Humor Helped People Understand the World',
            'week4': 'Part 4: The Final Reflection — Four Years of Watching Humanity'
        }
    }
}

CREATOR_LEVELS = {
    2026: 'Nano Creator (1k–10k followers)',
    2027: 'Micro Creator (10k–100k followers)',
    2028: 'Macro Creator (100k–1M followers)',
    2029: 'Mega Creator (1M+ followers)'
}

MONTH_NAMES = {
    'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
    'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
    'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
}

WEEK_NUMBERS = {
    'week1': 'Week 1', 'week2': 'Week 2', 'week3': 'Week 3', 'week4': 'Week 4'
}

def create_week_readme(year, month, week, topic, creator_level):
    """Create README content for a week branch"""
    month_name = MONTH_NAMES[month]
    week_name = WEEK_NUMBERS[week]
    
    phase = {
        2026: 'Nano Creator Phase',
        2027: 'Micro Creator Phase',
        2028: 'Macro Creator Phase',
        2029: 'Mega Creator Phase'
    }[year]
    
    format_desc = {
        2026: 'Medium-form video (3-10 minutes)',
        2027: 'Medium-form video (3-10 minutes)',
        2028: 'Long-form video (10-30+ minutes)',
        2029: 'Premium long-form or documentary-style (30+ minutes)'
    }[year]
    
    style_desc = {
        2026: 'Personal, scrappy, authentic',
        2027: 'Personal, scrappy, authentic',
        2028: 'High-production, cinematic',
        2029: 'High-production, cinematic, documentary-level'
    }[year]
    
    content = f"""# Misfit Ravi - {month_name} {year}, {week_name} Content Plan

**{creator_level}**

---

## Weekly Content Topic

### {topic}

---

## Topic Overview

An evergreen satirical exploration designed for {creator_level.lower()}, focusing on {topic.lower()}.

---

## Content Strategy

### Key Themes

- Evergreen satirical commentary
- Cultural observations
- Human behavior patterns
- Timeless insights

### Satirical Angle

- Smart humor that makes people think
- Self-aware commentary
- Relatable observations
- Evergreen themes that won't date

### Content Format

- **Primary:** {format_desc}
- **Secondary:** Short-form clips for social media
- **Style:** {style_desc}
- **Tone:** Witty, observational, insightful

---

## Key Points to Cover

1. **Core Theme**
   - Exploring {topic.lower()}
   - Finding the satirical angle
   - Making it relatable and timeless

2. **The Satire**
   - Pointing out universal truths
   - Finding humor in patterns
   - Making people think while laughing

3. **Evergreen Elements**
   - Content that ages well
   - Timeless observations
   - Rewatchable value

---

## Evergreen Elements

✅ **Timeless Topic:** {topic.split('(')[0].strip() if '(' in topic else topic} is always relevant  
✅ **Universal Appeal:** Everyone can relate to this  
✅ **Satirical Edge:** Smart humor that makes people think  
✅ **Rewatchable:** Content that ages well  

---

*Building something timeless, one video at a time.*  
*{week_name}, {month_name} {year} - {phase}*
"""
    return content

def update_all_week_readmes():
    """Update README files for all week branches"""
    total = 0
    updated = 0
    failed = 0
    
    print("=" * 80)
    print("UPDATING ALL WEEK BRANCH README FILES")
    print("=" * 80)
    print()
    
    for year in [2026, 2027, 2028, 2029]:
        print(f"Processing {year}...")
        for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            for week in ['week1', 'week2', 'week3', 'week4']:
                total += 1
                branch = f"{year}-{month}-{week}"
                topic = WEEKLY_TOPICS[year][month][week]
                creator_level = CREATOR_LEVELS[year]
                
                # Checkout branch
                result = subprocess.run(['git', 'checkout', branch], 
                                      capture_output=True, text=True, cwd='/Users/misfit.ravi/misfit-ravi')
                if result.returncode != 0:
                    print(f"  ❌ Could not checkout {branch}")
                    failed += 1
                    continue
                
                # Create README content
                readme_content = create_week_readme(year, month, week, topic, creator_level)
                
                # Write README
                with open('/Users/misfit.ravi/misfit-ravi/README.md', 'w') as f:
                    f.write(readme_content)
                
                # Commit
                week_name = WEEK_NUMBERS[week]
                month_name = MONTH_NAMES[month]
                subprocess.run(['git', 'add', 'README.md'], cwd='/Users/misfit.ravi/misfit-ravi')
                commit_msg = f"Add {week_name} {month_name} {year} content plan"
                result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                      capture_output=True, text=True, cwd='/Users/misfit.ravi/misfit-ravi')
                
                if result.returncode == 0:
                    updated += 1
                    if updated % 20 == 0:
                        print(f"  Updated {updated} branches...")
                else:
                    if 'nothing to commit' not in result.stdout and 'nothing to commit' not in result.stderr:
                        print(f"  ⚠️  {branch}: {result.stderr[:50]}")
    
    print()
    print("=" * 80)
    print(f"SUMMARY:")
    print(f"  ✅ Updated: {updated}/{total} branches")
    print(f"  ❌ Failed: {failed}/{total} branches")
    print("=" * 80)
    
    return updated, failed

if __name__ == '__main__':
    update_all_week_readmes()
