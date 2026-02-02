
# ========================================================================================

# Project: Arknights: Endfield Auto Check-in Script
# Author: nattapat2871
# Github: https://github.com/Nattapat2871/endfield.py
# License: MIT License

# DISCLAIMER:
# This software is provided "as is", without warranty of any kind, express or implied.
# This is an UNOFFICIAL script and is NOT affiliated with, endorsed by, or connected to 
# the game developers or publishers.

# USE AT YOUR OWN RISK.
# The author (nattapat2871) is NOT responsible for any consequences that may arise 
# from using this script, including but not limited to account bans, suspensions, 
# or data loss.

# ========================================================================================

import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def sanitize_code(code: str) -> str:
    """
    # PRINCIPLE: 
    # Normalizes the code string to ensure consistency.
    # It removes any text inside parentheses (e.g., "(Global Only)") 
    # and converts the string to uppercase.
    """
    if not code:
        return ""
    # Remove content within parentheses and extra whitespace
    clean_code = re.sub(r"\(.*\)", "", code)
    return clean_code.strip().upper()

# =========================================================
# PARSERS (Logic for specific websites)
# =========================================================

def parse_endfield_gg(content: str) -> list[dict[str, str]]:
    """
    # PRINCIPLE: 
    # Parses HTML from 'endfield.gg'.
    # This site uses a specific <table> layout.
    # The function iterates through table rows (<tr>), looks for the code 
    # in the first column (<td>), and rewards in the second column.
    """
    codes = []
    soup = BeautifulSoup(content, "lxml")
    
    # Locate the table with the specific class
    table = soup.find("table", class_="has-fixed-layout")
    if not table or not table.tbody:
        return []
    
    for tr in table.tbody.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2:
            # Code is usually in a <strong> tag or just text in the first column
            code_tag = tds[0].find("strong")
            code = code_tag.get_text(strip=True) if code_tag else tds[0].get_text(strip=True)
            
            # Extract rewards and remove bullet points characters
            rewards = tds[1].get_text(separator=" ", strip=True).replace("•", "").strip()
            
            if code and rewards:
                codes.append({
                    "code": sanitize_code(code),
                    "rewards": rewards,
                    "source": "endfield.gg"
                })
    return codes

def parse_gamesradar(content: str) -> list[dict[str, str]]:
    """
    # PRINCIPLE: 
    # Parses HTML from 'gamesradar.com'.
    # This site lists codes in an unordered list (<ul>).
    # The function looks for <li> items where the code is highlighted in <strong> tags,
    # then extracts the remaining text as the reward description.
    """
    codes = []
    soup = BeautifulSoup(content, "lxml")
    
    # Search for list items containing codes
    for li in soup.find_all("li"):
        strong_tag = li.find("strong")
        if not strong_tag:
            continue
            
        code_text = strong_tag.get_text(strip=True)
        # Filter out false positives (too short or non-alphanumeric)
        if len(code_text) < 5 or not code_text.replace(" ", "").isalnum():
            continue
            
        # Remove the code from the text to get the reward part
        reward_text = li.get_text(strip=True).replace(code_text, "", 1)
        # Clean up leading punctuation (colons, dashes)
        rewards = re.sub(r"^[\s:–-]*", "", reward_text).strip()
        
        if code_text and rewards:
            codes.append({
                "code": sanitize_code(code_text),
                "rewards": rewards,
                "source": "gamesradar.com"
            })
    return codes

def parse_ldshop(content: str) -> list[dict[str, str]]:
    """
    # PRINCIPLE: 
    # Parses HTML from 'ldshop.gg'.
    # This site typically wraps the code inside a colored <span> tag within an <li>.
    # The logic is similar to GamesRadar but targets <span> instead of <strong>.
    """
    codes = []
    soup = BeautifulSoup(content, "lxml")
    
    # Loop through list items
    for li in soup.find_all("li"):
        span_tag = li.find("span")
        if not span_tag:
            continue
            
        code_text = span_tag.get_text(strip=True)
        if len(code_text) < 5:
            continue
            
        reward_text = li.get_text(strip=True).replace(code_text, "", 1)
        rewards = re.sub(r"^[\s:–-]*", "", reward_text).strip()
        
        if code_text and rewards:
            codes.append({
                "code": sanitize_code(code_text),
                "rewards": rewards,
                "source": "ldshop.gg"
            })
    return codes

# =========================================================
# MAIN EXECUTION
# =========================================================

async def test_fetch():
    """
    # PRINCIPLE:
    # Orchestrates the asynchronous fetching process.
    # 1. Defines source URLs and their corresponding parser functions.
    # 2. Creates an aiohttp session to make requests.
    # 3. Iterates through sources, fetches HTML, and parses it.
    # 4. Aggregates results into a dictionary to automatically handle duplicates.
    """
    
    # Map sources to (URL, Parser Function)
    sources = {
        "endfield_gg": ("https://endfield.gg/arknights-endfield-codes/", parse_endfield_gg),
        "gamesradar": ("https://www.gamesradar.com/games/rpg/arknights-endfield-codes/", parse_gamesradar),
        "ldshop": ("https://www.ldshop.gg/blog/arknights-endfield-gp/arknights-endfield-codes.html", parse_ldshop)
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    all_results = {}
    
    print(f"⌨️ Github:https://github.com/Nattapat2871/endfield.py")
    print("🚀 Starting Arknights: Endfield Code Fetcher...\n")

    async with aiohttp.ClientSession(headers=headers) as session:
        for name, (url, parser) in sources.items():
            try:
                print(f"📡 Fetching data from: {name}...")
                async with session.get(url, timeout=15) as response:
                    if response.status == 200:
                        content = await response.text()
                        found_codes = parser(content)
                        print(f"   ✅ Found {len(found_codes)} codes")
                        
                        for item in found_codes:
                            code = item["code"]
                            # Deduplication: If code exists, keep the first one found (or update logic if needed)
                            if code not in all_results:
                                all_results[code] = item
                    else:
                        print(f"   ❌ HTTP Error {response.status} for {name}")
            except Exception as e:
                print(f"   ❌ Exception occurred with {name}: {e}")
            print("-" * 30)

    print(f"\n📊 Summary (Total Unique Codes): {len(all_results)}")
    for code, data in all_results.items():
        print(f"🎁 Code: {code}")
        print(f"   Rewards: {data['rewards']}")
        print(f"   Source: {data['source']}")
        print()

if __name__ == "__main__":
    asyncio.run(test_fetch())
