import requests
import json
import time
import hmac
import hashlib

# =========================================================
# 👇 CONFIGURATION (Enter your credentials here)
# =========================================================
# ⚠️ DO NOT COMMIT YOUR ACTUAL CREDENTIALS TO GITHUB
CRED = ""       # <--- Paste your 'cred' value here
ROLE_ID = ""    # <--- Paste your 'sk-game-role' value here
# =========================================================

def generate_sign(path, body, timestamp, cred):
    """
    Calculate Sign: MD5( HMAC-SHA256( path + body + timestamp + json, cred ) )
    """
    c_dict = {
        "platform": "3",
        "timestamp": str(timestamp),
        "dId": "",
    }
    json_str = json.dumps(c_dict, separators=(',', ':'))
    s = f"{path}{body}{timestamp}{json_str}"
    
    key = cred.encode('utf-8')
    msg = s.encode('utf-8')
    
    hmac_sha256 = hmac.new(key, msg, hashlib.sha256).hexdigest()
    final_sign = hashlib.md5(hmac_sha256.encode('utf-8')).hexdigest()
    return final_sign

def get_headers(path, body, timestamp, cred, role_id):
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
        "sk-language": "th_TH"
    }

def run_full_process():
    if not CRED or not ROLE_ID:
        print("❌ Error: Please configure CRED and ROLE_ID in the script first.")
        return

    base_url = "https://zonai.skport.com"
    ts = str(int(time.time()))

    print(f"🚀 Starting System: Arknights: Endfield Check-in")
    print(f"👤 Target Role ID: {ROLE_ID}")
    print("-" * 40)

    # -------------------------------------------------------
    # [STEP 1] Fetch Profile
    # -------------------------------------------------------
    print(f"🔍 1. Fetching User Profile...")
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
            # print(f"   🖼️ Avatar: {avatar_url}")
        else:
            print(f"   ⚠️ Cannot fetch profile: {data.get('message')}")
            
    except Exception as e:
        print(f"   💥 Profile Error: {e}")

    print("-" * 40)
    time.sleep(1)

    # -------------------------------------------------------
    # [STEP 2] Check-in (POST)
    # -------------------------------------------------------
    print(f"🔄 2. Sending Check-in Request...")
    
    checkin_path = "/web/v1/game/endfield/attendance"
    checkin_url = f"{base_url}{checkin_path}"
    
    payload_str = json.dumps({}, separators=(',', ':'))
    headers_post = get_headers(checkin_path, payload_str, ts, CRED, ROLE_ID)
    
    try:
        response = requests.post(checkin_url, headers=headers_post, data=payload_str)
        data = response.json()
        code = data.get("code")

        if code == 0:
            print(f"   ✅ Success! Check-in completed.")
            
            awards = data.get("data", {}).get("awardIds", [])
            res_map = data.get("data", {}).get("resourceInfoMap", {})
            
            if awards:
                print(f"   🎁 Rewards received: {len(awards)} items")
                for item in awards:
                    item_id = item.get('id')
                    info = res_map.get(item_id, {})
                    name = info.get("name", item_id)
                    count = info.get("count", 1)
                    print(f"      - {name} x{count}")
        
        elif code == 10001:
            print(f"   ✅ Already checked in today.")
        
        else:
            print(f"   ❌ Error: {data.get('message')} (Code: {code})")

    except Exception as e:
        print(f"   💥 Connection Error (POST): {e}")

    print("-" * 40)
    time.sleep(1) 

    # -------------------------------------------------------
    # [STEP 3] Get Calendar Status (GET)
    # -------------------------------------------------------
    print(f"📅 3. Checking Calendar Status...")
    
    ts_get = str(int(time.time()))
    headers_get = get_headers(checkin_path, "", ts_get, CRED, ROLE_ID)
    
    try:
        response = requests.get(checkin_url, headers=headers_get)
        data = response.json()
        
        if data.get("code") == 0:
            calendar = data.get("data", {}).get("calendar", [])
            res_map = data.get("data", {}).get("resourceInfoMap", {})
            
            claimed_count = sum(1 for day in calendar if day.get('done'))
            total_days = len(calendar)
            
            print(f"   📊 Progress: {claimed_count} / {total_days} Days")
            print("   [Latest 3 Days Status]")
            
            for idx, day in enumerate(calendar[:3]):
                status = "✅ Claimed" if day.get('done') else "⬜ Pending"
                award_id = day.get('awardId')
                
                info = res_map.get(award_id, {})
                item_name = info.get("name", award_id)
                item_count = info.get("count", "?")
                
                print(f"      Day {idx+1}: {item_name} x{item_count} -> {status}")
        else:
            print(f"   ❌ Cannot fetch calendar: {data.get('message')}")

    except Exception as e:
        print(f"   💥 Connection Error (GET): {e}")

    print("-" * 40)
    print("✨ Finished")

if __name__ == "__main__":
    run_full_process()
