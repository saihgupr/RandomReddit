import random
import webbrowser
import requests
import time
import json
import os
import subprocess
from datetime import datetime, timedelta
import re

# Cache file path
CACHE_FILE = "subreddits_cache.json"
# Cache expiration time (24 hours)
CACHE_EXPIRY_HOURS = 24

def load_cached_subreddits():
    """
    Load subreddits from cache file if it exists and isn't expired
    Returns tuple: (subreddits list, cache timestamp) or (None, None) if invalid
    """
    if not os.path.exists(CACHE_FILE):
        return None, None

    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
        
        # Check if cache has required fields
        if 'subreddits' not in cache_data or 'timestamp' not in cache_data:
            return None, None

        # Check if cache is expired
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() > cache_time + timedelta(hours=CACHE_EXPIRY_HOURS):
            return None, None

        return cache_data['subreddits'], cache_time

    except (json.JSONDecodeError, ValueError):
        return None, None

def save_to_cache(subreddits):
    """
    Save subreddits list to cache file with timestamp
    """
    cache_data = {
        'subreddits': subreddits,
        'timestamp': datetime.now().isoformat()
    }
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except Exception as e:
        print(f"Error saving cache: {str(e)}")

def get_subreddits_from_wiki():
    """
    Fetch subreddit list from r/ListOfSubreddits wiki page
    Returns a list of subreddit names
    """
    # Try to load from cache first
    cached_subreddits, cache_time = load_cached_subreddits()
    
    if cached_subreddits:
        print(f"Using cached subreddits (cached at {cache_time})")
        return cached_subreddits

    wiki_url = "https://www.reddit.com/r/ListOfSubreddits/wiki/nsfw.json"
    headers = {
        'User-Agent': 'RandomSubredditOpener/1.0 (by /u/yourusername)'
    }

    try:
        print("Fetching subreddit list from wiki...")
        response = requests.get(wiki_url, headers=headers)
        
        if response.status_code == 200:
            wiki_data = response.json()
            wiki_content = wiki_data['data']['content_md']
            
            # Extract subreddit names using regex
            # Looking for patterns like /r/subredditname or r/subredditname
            subreddit_pattern = r'(?:/r/|r/)(\w+)'
            subreddits = re.findall(subreddit_pattern, wiki_content)
            
            # Remove duplicates and sort
            subreddits = sorted(list(set(subreddits)))
            
            # Filter out any invalid subreddit names
            subreddits = [s for s in subreddits if len(s) > 1 and s.isalnum()]
            
            if subreddits:
                save_to_cache(subreddits)
                return subreddits
            else:
                print("No subreddits found in wiki content")
                return None
                
        else:
            print(f"Error fetching wiki page: {response.status_code}")
            return None
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def open_url_in_arc(url):
    """
    Open URL in Arc browser:
    - If current tab is on Reddit, use that tab
    - If current tab is not on Reddit, create a new tab
    """
    applescript = f'''
    tell application "Arc"
        activate
        set currentURL to URL of active tab of front window
        if currentURL contains "reddit.com" then
            -- Current tab is already on Reddit, use it
            tell active tab of front window
                set URL to "{url}"
            end tell
        else
            -- Current tab is not on Reddit, create a new tab
            tell front window
                make new tab with properties {{URL:"{url}"}}
            end tell
        end if
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except Exception as e:
        print(f"Error opening URL in Arc: {str(e)}")
        return False
        
def open_random_subreddit():
    """
    Open a random subreddit from the fetched/cached list
    """
    subreddits = get_subreddits_from_wiki()
    
    if not subreddits:
        print("Could not fetch subreddits. Using fallback list.")
        subreddits = [
            "AskReddit", "pics", "funny", "gaming", "aww",
            "Music", "movies", "news", "worldnews", "todayilearned"
        ]
    
    random_subreddit = random.choice(subreddits)
    url = f"https://www.reddit.com/r/{random_subreddit}/top/?t=all"
    
    # Try to open in Arc using AppleScript
    if open_url_in_arc(url):
        print(f"Opened r/{random_subreddit} top posts (all time) in Arc")
    else:
        print("Failed to open in Arc, falling back to default browser")
        # Fallback to default browser if AppleScript fails
        webbrowser.open(url, new=0, autoraise=True)
        print(f"Opened r/{random_subreddit} top posts (all time) in default browser")

if __name__ == "__main__":
    open_random_subreddit()