# Arknights: Endfield - Unofficial Automation Tools

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-GAS-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

![Visitor Badge](https://api.visitorbadge.io/api/VisitorHit?user=Nattapat2871&repo=endfield-sign&countColor=%237B1E7A)

A collection of unofficial scripts to help automate tasks for **Arknights: Endfield**. This repository includes tools for daily check-ins (both Cloud and Local versions) and fetching the latest gift codes from various community sources.

---

### ✨ Looking for an easier way? Try **Project Focalor**!

The features in this repository are **fully integrated** into **Project Focalor**, a powerful Discord bot assistant for HoYoVerse and Endfield games.

**Why use Project Focalor?**
* **🤖 Fully Automated:** No need to run scripts manually on your PC.
* **✅ More Stable:** Runs 24/7 with improved stability and error handling.
* **🛡️ Safe & Secure:** Manage your accounts safely.
* **🎁 All-in-One:** Auto Daily Check-in & Auto Redeem Codes—never miss a reward again!

👉 **[Get Project Focalor Now](https://project-focalor.nattapat2871.me)**

---

> [!WARNING]
> **DISCLAIMER:** This project is an **UNOFFICIAL** fan-made tool. It is not affiliated with, endorsed by, or connected to the game developers or publishers. **Use at your own risk.** The author is not responsible for any account bans or restrictions resulting from the use of these scripts.

## 📂 Included Tools

1. **`endfield_checkin.gs`** (🔥 Recommended): A Google Apps Script to automate check-ins on the cloud 24/7 for free. **Now supports Auto-Detect Characters & Multi-Server!**
2. **`endfield_checkin.py`**: A local Python script to automate the daily login/check-in process to claim rewards via the game's API.
3. **`endfield_code_fetcher.py`**: An asynchronous scraper that gathers active gift codes from multiple fan sites (e.g., endfield.gg, GamesRadar).

---

## ⚙️ Prerequisites (For Python users)

You need **Python 3.8+** installed. Install the required dependencies using `pip`:

```bash
pip install requests aiohttp beautifulsoup4 lxml
```

---

## 💻 How to get Credential (Endfield)

Follow these steps to connect the assistant to your account.

### Step 1: Log in to Portal
* Log in to the [SKPort Endfield Portal](https://game.skport.com/endfield/sign-in) with your account.

### Step 2: Open Developer Tools
* Press `F12` (or `Ctrl+Shift+I` / `Cmd+Option+I`) on your browser.
* Navigate to the **Application** tab.

### Step 3: Get ACCOUNT_TOKEN (Required for both GS & Python)
1. On the left sidebar, go to **Storage** -> **Cookies**.
2. Select `https://game.skport.com`.
3. **Refresh the page** (F5).
4. Find the cookie named `ACCOUNT_TOKEN` and copy its **Value**.

### Step 4: Get SK-GAME-ROLE (Required for Python / Optional for GS)
> **Note for Google Apps Script users:** You can **SKIP** this step! The GS script now automatically detects your Role ID.

1. Switch to the **Network** tab in Developer Tools.
2. **Refresh the page** again.
3. In the filter/search box, type `attendance` or `zonai.skport.com`.
4. Click on the request name (e.g., `attendance`).
5. Look at the **Headers** section -> **Request Headers**.
6. Find the key `sk-game-role` and copy its **Value**.

---

## 🚀 1. Auto Check-in (Google Apps Script - ☁️ Cloud & Free)

This is the recommended method. It runs automatically on Google's servers without needing your PC to be on.

**✨ Features:**
- **Auto-Detect Roles:** Automatically finds all characters in your account (Asia, USA, TW, etc.).
- **Multi-Server Support:** Checks in for *every* character found, not just the main one.
- **Zero Config:** Just paste your Token, no need to find Role IDs manually.
- **Discord Notify:** Sends beautiful notifications with dynamic timestamps.

### 🛠️ Setup Guide
1. Go to [Google Apps Script](https://script.google.com/) and create a **New Project**.
2. Copy the entire code from `endfield_checkin.gs` and paste it into the editor.
3. **Configuration:**
   - Paste your `ACCOUNT_TOKEN` into the `ACCOUNT_LIST`.
   - (Optional) Paste your `DISCORD_WEBHOOK_URL`.
   - **No need to fill `roleId`**, the script will handle it automatically!
4. Click the **Save** icon (💾) or press `Ctrl + S`.
5. Select `runFullProcess` from the top dropdown menu and click **▶ Run** to test it once. (Grant necessary permissions if prompted).

### ⏰ How to set up Trigger (Run Automatically)
1. On the left sidebar, click the **Triggers** icon (⏰).
2. Click **+ Add Trigger** at the bottom right.
3. Set up the trigger as follows:
   - Choose which function to run: `runFullProcess`
   - Select event source: `Time-driven`
   - Select type of time based trigger: `Day timer`
   - Select time of day: `3am to 4am` (or any time you prefer)
4. Click **Save**. Done! The script will now check-in for you every day.

### 📸 Discord Output Example
<p align="center">
  <img width="458" height="530" alt="image" src="https://github.com/user-attachments/assets/98eb7619-79e8-4c12-9c27-5f454eb74081" />
</p>

```text
Arknights: Endfield Check-in
🎉 Success! Reward claimed.

👤 Username: Nattapat2871 (UID: 7305348574810)
📅 Progress: 4 / 28 days
🎁 Today's Reward: Oroberyl x80

Skport Auto Check-in • Today at 3:17 AM
```

---

## 🐍 2. Auto Check-in (Python - Local PC)

If you prefer running the script locally on your PC.

#### **Setup:**
Once you have the values from the steps above, open `endfield_checkin.py` and paste them into the configuration section:

```python
# 👇 ACCOUNT SETTINGS
ACCOUNT_TOKEN = ""   # <--- ENTER YOUR ACCOUNT_TOKEN HERE 
ROLE_ID = ""         # <--- ENTER YOUR ROLE_ID (SK-GAME-ROLE) HERE 
```

#### **How to Run:**
```bash
python endfield_checkin.py
```

#### **📜 Example Output:**
```text
(.venv) PS E:\devlopers_app\Skript\Project Focalor\tests> py test_endfield.py 
--- 0. Authentication Info ---
🔑 CRED: ****************
🔑 SIGN (Sample): ************
🎯 SK_GAME_ROLE: *********

--- 1. User Profile ---
👤 Username: Nattapat2871
🆔 UID (Skport): 7305348574810
🖼️ Avatar URL: [https://static.skport.com/image](https://static.skport.com/image)...

--- 2. Check-in Result ---
✅ Already signed in today. (Skipping POST request)

--- 3. Check-in Data ---
📅 Progress: Checked in 4 / 28 days
🎁 Today's Reward: Oroberyl x80
```

---

## 🎁 3. Gift Code Fetcher (`endfield_code_fetcher.py`)

This script scrapes various websites to find the latest promo codes.

#### **How to Run:**
```bash
python endfield_code_fetcher.py
```

#### **📜 Example Output:**
```text
(.venv) PS E:\devlopers_app\Skript\Project Focalor\tests> python endfield_code_fetcher.py
⌨️ Github: [https://github.com/Nattapat2871/endfield.py](https://github.com/Nattapat2871/endfield.py)
🚀 Starting Arknights: Endfield Code Fetcher...

📡 Fetching data from: endfield_gg...
   ✅ Found 4 codes
------------------------------
...
📊 Summary (Total Unique Codes): 4
🎁 Code: ENDFIELDGIFT
   Rewards: Oroberyl x500
   Source: endfield.gg
```

---

## 📜 License

This project is licensed under the **MIT License**.

**Author:** [nattapat2871](https://github.com/nattapat2871)
