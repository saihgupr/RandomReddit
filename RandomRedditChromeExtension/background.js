const CACHE_EXPIRY_HOURS = 24;

async function getSubreddits(isIncognito) {
  const cacheKey = isIncognito ? 'nsfw_subreddits' : 'sfw_subreddits';
  const timestampKey = isIncognito ? 'nsfw_timestamp' : 'sfw_timestamp';

  const cachedData = await chrome.storage.local.get([cacheKey, timestampKey]);
  if (cachedData[cacheKey] && cachedData[timestampKey]) {
    const cacheTime = new Date(cachedData[timestampKey]);
    if (new Date() - cacheTime < CACHE_EXPIRY_HOURS * 60 * 60 * 1000) {
      console.log(`Using cached ${isIncognito ? 'NSFW' : 'SFW'} subreddits`);
      return cachedData[cacheKey];
    }
  }

  console.log(`Fetching ${isIncognito ? 'NSFW' : 'SFW'} subreddit list from wiki...`);
  const wikiPage = isIncognito ? 'nsfw' : 'listofsubreddits';
  const url = `https://www.reddit.com/r/ListOfSubreddits/wiki/${wikiPage}.json`;

  try {
    const response = await fetch(url);
    const wikiData = await response.json();
    const wikiContent = wikiData.data.content_md;
    const subredditPattern = /(?:\/r\/|r\/)(\w+)/g;
    let subreddits = wikiContent.match(subredditPattern).map(s => s.replace(/\/?r\//, ''));
    subreddits = [...new Set(subreddits)].sort();
    subreddits = subreddits.filter(s => s.length > 1 && /^[a-zA-Z0-9_]+$/.test(s));

    await chrome.storage.local.set({ 
      [cacheKey]: subreddits, 
      [timestampKey]: new Date().toISOString() 
    });
    return subreddits;
  } catch (error) {
    console.error(`Error fetching ${isIncognito ? 'NSFW' : 'SFW'} subreddits:`, error);
    return isIncognito ? ['askredditafterdark'] : ['AskReddit']; // Fallback
  }
}

chrome.action.onClicked.addListener(async (tab) => {
  const isIncognito = tab.incognito;
  const subreddits = await getSubreddits(isIncognito);
  
  if (subreddits && subreddits.length > 0) {
    const randomSubreddit = subreddits[Math.floor(Math.random() * subreddits.length)];
    const domain = isIncognito ? 'old.reddit.com' : 'www.reddit.com';
    const url = `https://${domain}/r/${randomSubreddit}/top/?t=all`;

    // Query for all reddit tabs and then filter them by incognito status
    chrome.tabs.query({ url: '*://*.reddit.com/*' }, (allRedditTabs) => {
      const appropriateTabs = allRedditTabs.filter(t => t.incognito === isIncognito);
      
      if (appropriateTabs.length > 0) {
        // If a matching tab exists, update it
        chrome.tabs.update(appropriateTabs[0].id, { url: url, active: true });
      } else {
        // Otherwise, create a new tab. It will open in the correct window (normal or incognito).
        chrome.tabs.create({ url: url });
      }
    });
  } else {
    console.error("Could not get a list of subreddits.");
  }
});