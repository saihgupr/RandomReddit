<h1>RandomReddit Chrome Extension</h1>

<p>RandomReddit is a Chrome Extension that opens random subreddits from the list maintained at r/ListOfSubreddits. In a normal window, it opens a random SFW subreddit. In an Incognito window, it opens a random NSFW subreddit.</p>

<h2>Optional Usage</h2>

<p>Run the python script:</p>
<pre><code class="language-bash">python random_reddit.py</code></pre>

<p>The script will:</p>
<ol>
    <li>Check for cached subreddit list</li>
    <li>If cache is expired or missing, fetch from r/ListOfSubreddits wiki</li>
    <li>Select a random subreddit</li>
    <li>Open in your browser (if available) or default browser</li>
    <li>Display the opened subreddit in the console</li>
</ol>

<h2>How It Works</h2>

<ul>
    <li><strong>Subreddit List</strong>: Fetches from https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits using regex to extract subreddit names</li>
    <li><strong>Caching</strong>: Stores subreddit list in <code>subreddits_cache.json</code> for 24 hours</li>
    <li><strong>Browser Management</strong>:
        <ul>
            <li>On macOS with your Browswer: Uses AppleScript to check current tab URL
                <ul>
                    <li>If on Reddit: Reuses current tab</li>
                    <li>If not on Reddit: Creates new tab</li>
                </ul>
            </li>
            <li>Fallback: Uses <code>webbrowser</code> module for default browser</li>
        </ul>
    </li>
    <li><strong>Error Handling</strong>: Includes fallback subreddit list and browser fallback</li>
</ul>

<h2>Notes</h2>

<ul>
    <li>The script requires an internet connection for initial subreddit list fetch</li>
    <li>The subreddit list from r/ListOfSubreddits may include NSFW or inactive subreddits (no filtering applied)</li>
    <li>Cache file (<code>subreddits_cache.json</code>) is created in the script's directory</li>
</ul>

<h2>License</h2>

<p>MIT License - see <a href="LICENSE">LICENSE</a> file for details</p>

<h2>Issues</h2>

<p>Report bugs or feature requests in the <a href="https://github.com/yourusername/RandomReddit/issues">Issues</a> section.</p>
