import asyncio
import json
import argparse
from playwright.async_api import async_playwright

# This script implements Step 1 of the Reddit-to-ChatGPT SEO pipeline.
# It uses Playwright to navigate to a Reddit thread and execute in-browser
# fetch requests to Reddit's undocumented .json and morechildren.json endpoints,
# bypassing strict API limits by utilizing the browser's native guest session.

JS_EXTRACTOR = """
async () => {
    const threadId = window.location.pathname.split('/')[4];
    const url = window.location.pathname.replace(/\\/$/, '') + '.json?limit=500&raw_json=1&showmore=true';
    
    // Fetch initial thread
    const res = await fetch(url);
    const data = await res.json();
    
    const postData = data[0].data.children[0].data;
    const commentsData = data[1].data.children;
    
    let allComments = [];
    let moreIds = [];
    
    // Parse initial comments
    function parseComments(children) {
        for (const child of children) {
            if (child.kind === 'more' && child.data.children) {
                moreIds.push(...child.data.children);
            } else if (child.kind === 't1') {
                allComments.push({
                    id: child.data.name,
                    author: child.data.author,
                    text: child.data.body,
                    score: child.data.score,
                    depth: child.data.depth
                });
                if (child.data.replies && child.data.replies.data) {
                    parseComments(child.data.replies.data.children);
                }
            }
        }
    }
    parseComments(commentsData);
    
    // Fetch morechildren in batches of 100
    const BATCH_SIZE = 100;
    for (let i = 0; i < moreIds.length; i += BATCH_SIZE) {
        const batch = moreIds.slice(i, i + BATCH_SIZE);
        const params = new URLSearchParams({
            api_type: 'json',
            link_id: 't3_' + threadId,
            children: batch.join(','),
            raw_json: '1',
            limit_children: 'false'
        });
        
        const moreUrl = `https://www.reddit.com/api/morechildren.json?${params.toString()}`;
        const moreRes = await fetch(moreUrl);
        const moreData = await moreRes.json();
        
        if (moreData && moreData.json && moreData.json.data && moreData.json.data.things) {
            for (const thing of moreData.json.data.things) {
                if (thing.kind === 't1') {
                    allComments.push({
                        id: thing.data.name,
                        author: thing.data.author,
                        text: thing.data.body,
                        score: thing.data.score,
                        depth: thing.data.depth
                    });
                }
            }
        }
        
        // Sleep to avoid rate limiting
        await new Promise(r => setTimeout(r, 1000));
    }
    
    return {
        post: {
            title: postData.title,
            author: postData.author,
            score: postData.score,
            content: postData.selftext
        },
        comments: allComments
    };
}
"""

async def extract_thread(url: str):
    print(f"Starting extraction for: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Using a stealthy context
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print("Navigating to thread...")
        await page.goto(url, wait_until="domcontentloaded")
        
        print("Injecting morechildren extraction logic (this may take a moment for large threads)...")
        result = await page.evaluate(JS_EXTRACTOR)
        
        await browser.close()
        
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Reddit thread and all comments.")
    parser.add_argument("url", help="Reddit thread URL")
    parser.add_argument("--output", help="Output JSON file", default="thread_data.json")
    
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(extract_thread(args.url))
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully extracted post and {len(data['comments'])} comments.")
    print(f"Data saved to {args.output}")
