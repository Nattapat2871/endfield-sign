
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
import urllib.parse

# =========================================================
# 👇 ACCOUNT SETTINGS (Fill in your credentials here)
# =========================================================
# You must fill in the values inside the quotes below.
ACCOUNT_TOKEN = ""   # <--- ENTER YOUR ACCOUNT HERE 
ROLE_ID = ""         # <--- ENTER YOUR ROLE ID HERE 
# =========================================================

APP_CODE = "6eb76d4e13aa36e6"
BASE_URL = "https://zonai.skport.com"

def perform_oauth_flow(account_token):
    encoded_token = urllib.parse.quote(account_token, safe='')
    info_url = f"https://as.gryphline.com/user/info/v1/basic?token={encoded_token}"
    info_res = requests.get(info_url)
    info_data = info_res.json()
    if info_data.get("status") != 0:
        raise Exception(f"OAuth Step 1 Failed: {info_data.get('msg')}")

    grant_url = "https://as.gryphline.com/user/oauth2/v2/grant"
    grant_payload = {"token": account_token, "appCode": APP_CODE, "type": 0}
    grant_res = requests.post(grant_url, json=grant_payload)
    grant_data = grant_res.json()
    if grant_data.get("status") != 0 or not grant_data.get("data", {}).get("code"):
        raise Exception(f"OAuth Step 2 Failed: {grant_data.get('msg')}")
    auth_code = grant_data["data"]["code"]

    cred_url = f"{BASE_URL}/web/v1/user/auth/generate_cred_by_code"
    cred_headers = {"platform": "3", "content-type": "application/json"}
    cred_payload = {"code": auth_code, "kind": 1}
    cred_res = requests.post(cred_url, headers=cred_headers, json=cred_payload)
    cred_data = cred_res.json()
    if cred_data.get("code") != 0 or not cred_data.get("data", {}).get("cred"):
        raise Exception(f"OAuth Step 3 Failed: {cred_data.get('message')}")
    
    return cred_data["data"]["cred"], cred_data["data"]["token"]

def generate_sign(path, timestamp, salt):
    header_dict = {"platform": "3", "timestamp": str(timestamp), "dId": "", "vName": "1.0.0"}
    json_str = json.dumps(header_dict, separators=(',', ':'))
    s = f"{path}{timestamp}{json_str}"
    
    key = salt.encode('utf-8')
    msg = s.encode('utf-8')
    
    hmac_sha256 = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return hashlib.md5(hmac_sha256.encode('utf-8')).hexdigest()

def get_headers(path, timestamp, cred, salt, role_id):
    sign = generate_sign(path, timestamp, salt)
    return {
        "cred": cred,
        "sk-game-role": role_id,
        "platform": "3",
        "sk-language": "en",
        "timestamp": timestamp,
        "vname": "1.0.0",
        "sign": sign,
        "User-Agent": "Skport/0.7.0 (com.gryphline.skport; build:700089; Android 33; ) Okhttp/5.1.0",
        "content-type": "application/json",
        "accept": "application/json, text/plain, */*"
    }

def run_full_process():
    if not ACCOUNT_TOKEN or not ROLE_ID:
        print("❌ Error: Missing ACCOUNT_TOKEN or ROLE_ID.")
        return

    ts = str(int(time.time()))

    # =======================================================
    # --- 0. สร้าง cred และเตรียมข้อมูลการยืนยันตัวตน ---
    # =======================================================
    print("--- 0. Authentication Info ---")
    try:
        CRED, SALT = perform_oauth_flow(ACCOUNT_TOKEN)
        # ลองสร้าง Sign ตัวอย่างของการดึงโปรไฟล์มาแสดงผล
        SAMPLE_SIGN = generate_sign("/web/v2/user", ts, SALT)
        print(f"🔑 CRED: {CRED}")
        print(f"🔑 SIGN (Sample): {SAMPLE_SIGN}")
        print(f"🎯 SK_GAME_ROLE: {ROLE_ID}")
    except Exception as e:
        print(f"❌ Auth Failed: {e}")
        return

    # =======================================================
    # --- 1. โปรไฟล์ ---
    # =======================================================
    print("\n--- 1. User Profile ---")
    profile_path = "/web/v2/user"
    headers_profile = get_headers(profile_path, ts, CRED, SALT, ROLE_ID)
    
    try:
        res_profile = requests.get(f"{BASE_URL}{profile_path}", headers=headers_profile).json()
        if res_profile.get("code") == 0:
            basic_user = res_profile.get("data", {}).get("user", {}).get("basicUser", {})
            print(f"👤 Username: {basic_user.get('nickname', 'Unknown')}")
            print(f"🆔 UID (Skport): {basic_user.get('id', 'Unknown')}")
            print(f"🖼️ Avatar URL: {basic_user.get('avatar', 'No image')}")
        else:
            print(f"⚠️ Profile Error: {res_profile.get('message')}")
    except Exception as e:
        print(f"💥 Profile Fetch Error: {e}")

    # =======================================================
    # --- ดำเนินการเช็คอิน (Check-in Logic) ---
    # =======================================================
    checkin_path = "/web/v1/game/endfield/attendance"
    checkin_url = f"{BASE_URL}{checkin_path}"
    
    # 1. เช็คสถานะปฏิทิน (GET)
    ts_check = str(int(time.time()))
    headers_check = get_headers(checkin_path, ts_check, CRED, SALT, ROLE_ID)
    
    res_status = requests.get(checkin_url, headers=headers_check).json()
    if res_status.get("code") != 0:
        print(f"❌ Error fetching calendar: {res_status.get('message')}")
        return

    data = res_status.get("data", {})
    calendar = data.get("calendar", [])
    res_map = data.get("resourceInfoMap", {})
    total_days = len(calendar)
    
    already_claimed = data.get("hasToday", False)
    claimed_count = sum(1 for day in calendar if day.get('done'))

    checkin_result_msg = ""

    if already_claimed:
        checkin_result_msg = "✅ Already signed in today. (Skipping POST request)"
        today_idx = claimed_count - 1 # ดึงของรางวัลที่รับไปแล้ววันนี้
    else:
        # ยังไม่ได้รับ ทำการส่ง POST เพื่อเช็คอิน
        ts_post = str(int(time.time()))
        headers_post = get_headers(checkin_path, ts_post, CRED, SALT, ROLE_ID)
        res_post = requests.post(checkin_url, headers=headers_post).json()
        
        if res_post.get("code") == 0:
            checkin_result_msg = "✅ Success! Reward claimed."
            today_idx = claimed_count # ของรางวัลของวันนี้คือช่องถัดไป
            claimed_count += 1 # เพิ่มยอดเช็คอินสำเร็จ
        else:
            checkin_result_msg = f"❌ Claim Failed: {res_post.get('message')}"
            today_idx = claimed_count

    # ดึงข้อมูลของรางวัลประจำวัน
    today_award_name = "Unknown"
    today_award_count = 0
    today_award_icon = "No image"

    if 0 <= today_idx < total_days:
        award_id = calendar[today_idx].get("awardId")
        info = res_map.get(award_id, {})
        today_award_name = info.get("name", award_id)
        today_award_count = info.get("count", 1)
        today_award_icon = info.get("icon", "No image")

    # =======================================================
    # --- 2. ผลการเช็คอิน ---
    # =======================================================
    print("\n--- 2. Check-in Result ---")
    print(checkin_result_msg)

    # =======================================================
    # --- 3. ข้อมูลการเช็คอิน ---
    # =======================================================
    print("\n--- 3. Check-in Data ---")
    print(f"📅 Progress: Checked in {claimed_count} / {total_days} days")
    print(f"🎁 Today's Reward: {today_award_name} x{today_award_count}")
    print(f"🖼️ Item Icon URL: {today_award_icon}")

if __name__ == "__main__":
    run_full_process()
