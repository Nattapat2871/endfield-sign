
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

import requests
import json
import time
import hmac
import hashlib

# =========================================================
# 👇 ACCOUNT SETTINGS (Fill in your credentials here)
# =========================================================
# You must fill in the values inside the quotes below.
CRED = " "      # <--- ENTER YOUR CRED HERE (e.g., "q61gZI...")
ROLE_ID = " "   # <--- ENTER YOUR ROLE ID HERE (e.g., "3_4492...")
# =========================================================

def generate_sign(path, body, timestamp, cred):
    """
    Generates the cryptographic signature required by the API.
    Formula: MD5( HMAC-SHA256( path + body + timestamp + json_params, cred ) )
    
    Args:
        path (str): The API endpoint path.
        body (str): The request body (JSON string).
        timestamp (str): Current timestamp.
        cred (str): User credential key.
        
    Returns:
        str: The generated signature string.
    """
    c_dict = {
        "platform": "3",
        "timestamp": str(timestamp),
        "dId": "",
    }
    # Important: separators must be exact to match server expectation
    json_str = json.dumps(c_dict, separators=(',', ':'))
    s = f"{path}{body}{timestamp}{json_str}"
    
    key = cred.encode('utf-8')
    msg = s.encode('utf-8')
    
    hmac_sha256 = hmac.new(key, msg, hashlib.sha256).hexdigest()
    final_sign = hashlib.md5(hmac_sha256.encode('utf-8')).hexdigest()
    return final_sign

def get_headers(path, body, timestamp, cred, role_id):
    """
    Constructs the HTTP headers for the request, including the calculated signature.
    
    Args:
        path (str): API path.
        body (str): Request body.
        timestamp (str): Timestamp.
        cred (str): User credential.
        role_id (str): The game role ID.

    Returns:
        dict: A dictionary of HTTP headers.
    """
    sign = generate_sign(path, body, timestamp, cred)
    return {
        "authority": "zonai.skport.com",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://game.skport.com",
        "referer": "https://game.skport.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "cred": cred,
        "sign": sign,
        "timestamp": timestamp,
        "platform": "3",
        "vname": "1.0.0",
        "sk-game-role": role_id,
        "sk-language": "en"
    }

def run_full_process():
    """
    Main execution function.
    1. Fetches user profile to verify identity.
    2. Sends a check-in request to claim rewards.
    3. Retrieves and summarizes the calendar status.
    """
    
    # Check if user forgot to fill in credentials
    if not CRED or not ROLE_ID:
        print("❌ Error: Please open the script and fill in CRED and ROLE_ID variables first.")
        return

    base_url = "https://zonai.skport.com"
    ts = str(int(time.time()))

    print(f"⌨️ Github:https://github.com/Nattapat2871/endfield.py")
    print(f"🚀 Starting Arknights: Endfield Check-in System")
    print(f"👤 Target Role ID: {ROLE_ID}")
    print("-" * 40)

    # -------------------------------------------------------
    # [STEP 1] Fetch User Profile
    # -------------------------------------------------------
    print(f"🔍 1. Fetching user profile...")
    profile_path = "/web/v2/user"
    profile_url = f"{base_url}{profile_path}"
    
    headers_profile = get_headers(profile_path, "", ts, CRED, ROLE_ID)
    
    try:
        response = requests.get(profile_url, headers=headers_profile)
        data = response.json()
        
        if data.get("code") == 0:
            basic_user = data.get("data", {}).get("user", {}).get("basicUser", {})
            nickname = basic_user.get("nickname", "Unknown")
            avatar_url = basic_user.get("avatar", "")
            user_id = basic_user.get("id", "Unknown")
            
            print(f"   👤 Nickname: {nickname}")
            print(f"   🆔 User ID: {user_id}")
            print(f"   🖼️ Avatar URL: {avatar_url}")
        else:
            print(f"   ⚠️ Failed to fetch profile: {data.get('message')}")
            
    except Exception as e:
        print(f"   💥 Profile Error: {e}")

    print("-" * 40)
    time.sleep(1)

    # -------------------------------------------------------
    # [STEP 2] Claim Daily Reward (POST)
    # -------------------------------------------------------
    print(f"🔄 2. Sending check-in request...")
    
    checkin_path = "/web/v1/game/endfield/attendance"
    checkin_url = f"{base_url}{checkin_path}"
    
    payload_str = json.dumps({}, separators=(',', ':'))
    headers_post = get_headers(checkin_path, payload_str, ts, CRED, ROLE_ID)
    
    try:
        response = requests.post(checkin_url, headers=headers_post, data=payload_str)
        data = response.json()
        code = data.get("code")

        if code == 0:
            print(f"   ✅ Success! Reward claimed.")
            
            awards = data.get("data", {}).get("awardIds", [])
            # Get resource map for item names
            res_map = data.get("data", {}).get("resourceInfoMap", {})
            
            if awards:
                print(f"   🎁 Rewards received: {len(awards)} items")
                for item in awards:
                    item_id = item.get('id')
                    # Find name and info from map
                    info = res_map.get(item_id, {})
                    name = info.get("name", item_id)
                    count = info.get("count", 1)
                    print(f"      - {name} x{count}")
        
        elif code == 10001:
            print(f"   ✅ Already checked in today. (No action needed)")
        
        else:
            print(f"   ❌ Error: {data.get('message')} (Code: {code})")

    except Exception as e:
        print(f"   💥 Connection Error (POST): {e}")

    print("-" * 40)
    time.sleep(1) 

    # -------------------------------------------------------
    # [STEP 3] Check Calendar Status (GET)
    # -------------------------------------------------------
    print(f"📅 3. Summarizing calendar status...")
    
    ts_get = str(int(time.time()))
    headers_get = get_headers(checkin_path, "", ts_get, CRED, ROLE_ID)
    
    try:
        response = requests.get(checkin_url, headers=headers_get)
        data = response.json()
        
        if data.get("code") == 0:
            calendar = data.get("data", {}).get("calendar", [])
            # Get resource map (Important!)
            res_map = data.get("data", {}).get("resourceInfoMap", {})
            
            claimed_count = sum(1 for day in calendar if day.get('done'))
            total_days = len(calendar)
            
            print(f"   📊 Progress: Claimed {claimed_count} / {total_days} days")
            print("   [Recent 3 Days Status]")
            
            for idx, day in enumerate(calendar[:3]):
                status = "✅ Claimed" if day.get('done') else "⬜ Pending"
                award_id = day.get('awardId')
                
                # Get item info
                info = res_map.get(award_id, {})
                item_name = info.get("name", award_id)
                item_count = info.get("count", "?")
                item_icon = info.get("icon", "")
                
                print(f"      Day {idx+1}: {item_name} x{item_count} -> {status}")
                if item_icon:
                    print(f"            🖼️ Icon: {item_icon}")
        else:
            print(f"   ❌ Failed to fetch calendar: {data.get('message')}")

    except Exception as e:
        print(f"   💥 Connection Error (GET): {e}")

    print("-" * 40)
    print("✨ Process Completed.")

if __name__ == "__main__":
    run_full_process()
