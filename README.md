<h1>RandomReddit</h1>

<p>RandomReddit is a Python script that opens random subreddits from the list maintained at r/ListOfSubreddits. It features smart tab management for Arc browser on macOS (opening in current tab if already on Reddit, new tab otherwise), caching of subreddit lists, and fallback support for default browsers.</p>

<h2>Features</h2>

<ul>
    <li>Fetches subreddit list from r/ListOfSubreddits wiki page</li>
    <li>Caches subreddit list locally for 24 hours to reduce API calls</li>
    <li>Smart tab management for Arc browser (macOS):
        <ul>
            <li>Uses current tab if already on Reddit</li>
            <li>Creates new tab if current tab is not on Reddit</li>
        </ul>
    </li>
    <li>Fallback to default browser if Arc is unavailable</li>
    <li>Opens top posts (all time) for selected subreddit</li>
    <li>Includes a fallback list of popular subreddits if wiki fetch fails</li>
</ul>

<h2>Requirements</h2>

<ul>
    <li>Python 3.6+</li>
    <li>macOS (for Arc browser support)</li>
    <li>Arc browser (optional, for smart tab management)</li>
    <li>Standard Python libraries:
        <ul>
            <li><code>random</code></li>
            <li><code>webbrowser</code></li>
            <li><code>requests</code></li>
            <li><code>time</code></li>
            <li><code>json</code></li>
            <li><code>os</code></li>
            <li><code>subprocess</code></li>
            <li><code>datetime</code></li>
            <li><code>re</code></li>
        </ul>
    </li>
</ul>

<p>No external dependencies required!</p>

<h2>Installation</h2>

<ol>
    <li>Clone the repository:
        <pre><code class="language-bash">git clone https://github.com/yourusername/RandomReddit.git
cd RandomReddit</code></pre>
    </li>
    <li>Ensure you have Python 3.6 or later installed:
        <pre><code class="language-bash">python --version</code></pre>
    </li>
    <li>(Optional) For Arc browser support, ensure Arc is installed on your macOS system.</li>
</ol>

<h2>Usage</h2>

<p>Run the script:</p>
<pre><code class="language-bash">python random_reddit.py</code></pre>

<p>The script will:</p>
<ol>
    <li>Check for cached subreddit list</li>
    <li>If cache is expired or missing, fetch from r/ListOfSubreddits wiki</li>
    <li>Select a random subreddit</li>
    <li>Open in Arc browser (if available) or default browser</li>
    <li>Display the opened subreddit in the console</li>
</ol>

<h2>How It Works</h2>

<ul>
    <li><strong>Subreddit List</strong>: Fetches from https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits using regex to extract subreddit names</li>
    <li><strong>Caching</strong>: Stores subreddit list in <code>subreddits_cache.json</code> for 24 hours</li>
    <li><strong>Browser Management</strong>:
        <ul>
            <li>On macOS with Arc: Uses AppleScript to check current tab URL
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
    <li>Arc browser support is macOS-only; other systems use default browser</li>
    <li>The subreddit list from r/ListOfSubreddits may include NSFW or inactive subreddits (no filtering applied)</li>
    <li>Cache file (<code>subreddits_cache.json</code>) is created in the script's directory</li>
</ul>

<h2>Contributing</h2>

<ol>
    <li>Fork the repository</li>
    <li>Create a feature branch:
        <pre><code class="language-bash">git checkout -b feature/new-feature</code></pre>
    </li>
    <li>Commit changes:
        <pre><code class="language-bash">git commit -m 'Add new feature'</code></pre>
    </li>
    <li>Push to the branch:
        <pre><code class="language-bash">git push origin feature/new-feature</code></pre>
    </li>
    <li>Open a Pull Request</li>
</ol>

<h2>License</h2>

<p>MIT License - see <a href="LICENSE">LICENSE</a> file for details</p>

<h2>Acknowledgments</h2>

<ul>
    <li>Subreddit list provided by r/ListOfSubreddits community</li>
    <li>AppleScript integration for Arc browser support</li>
    <li>Standard Python libraries for cross-platform compatibility</li>
</ul>

<h2>Issues</h2>

<p>Report bugs or feature requests in the <a href="https://github.com/yourusername/RandomReddit/issues">Issues</a> section.</p>
