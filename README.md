# Arknights: Endfield - Unofficial Automation Tools

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

![Visitor Badge](https://api.visitorbadge.io/api/VisitorHit?user=Nattapat2871&repo=endfield.py&countColor=%237B1E7A)


A collection of unofficial Python scripts to help automate tasks for **Arknights: Endfield**. This repository includes tools for daily check-ins and fetching the latest gift codes from various community sources.

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

1.  **`endfield_checkin.py`**: A script to automate the daily login/check-in process to claim rewards via the game's API.
2.  **`endfield_code_fetcher.py`**: An asynchronous scraper that gathers active gift codes from multiple fan sites (e.g., endfield.gg, GamesRadar).

---

## ⚙️ Prerequisites

You need **Python 3.8+** installed. Install the required dependencies using `pip`:

```bash
pip install requests aiohttp beautifulsoup4 lxml
```

---

## 💻 How to get Credential (Endfield)

Follow these steps to connect the assistant to your account:

### Step 1: Log in to Portal
* Log in to the [SKPort Endfield Portal](https://game.skport.com/endfield/sign-in) with your account.

### Step 2: Open Developer Tools
* Press `F12` (or `Ctrl+Shift+I` / `Cmd+Option+I`) on your browser.
* Navigate to the **Application** tab.

### Step 3: Get ACCOUNT_TOKEN
1.  On the left sidebar, go to **Storage** -> **Cookies**.
2.  Select `https://game.skport.com`.
3.  **Refresh the page** (F5).
4.  Find the cookie named `ACCOUNT_TOKEN` and copy its **Value**.
5.  Paste it into the registration field.

### Step 4: Get SK-GAME-ROLE
1.  Switch to the **Network** tab in Developer Tools.
2.  **Refresh the page** again.
3.  In the filter/search box, type `attendance` or `zonai.skport.com`.
4.  Click on the request name (e.g., `attendance`).
5.  Look at the **Headers** section -> **Request Headers**.
6.  Find the key `sk-game-role` and copy its **Value**.
7.  Paste it into the registration field.

---

#### **Setup:**
Once you have the values from the steps above, open `endfield_checkin.py` and paste them into the configuration section:

```python
# 👇 ACCOUNT SETTINGS
ACCOUNT_TOKEN = ""   # <--- ENTER YOUR ACCOUNT HERE 
ROLE_ID = ""         # <--- ENTER YOUR ROLE ID HERE 
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
🖼️ Avatar URL: https://static.skport.com/image/common/20251031/46750c47729f845b4db6c404e12f771c.png

--- 2. Check-in Result ---
✅ Already signed in today. (Skipping POST request)

--- 3. Check-in Data ---
📅 Progress: Checked in 4 / 28 days
🎁 Today's Reward: Oroberyl x80
🖼️ Item Icon URL: https://static.skport.com/asset/endfield_attendance/8ed434a6cdb173c96ed0572115112f93.png
```

---

### 2. Gift Code Fetcher (`endfield_code_fetcher.py`)

This script scrapes various websites to find the latest promo codes.

#### **How to Run:**
```bash
python endfield_code_fetcher.py
```

#### **📜 Example Output:**
```text
(.venv) PS E:\devlopers_app\Skript\Project Focalor\tests> python endfield_code_fetcher.py
⌨️ Github:[https://github.com/Nattapat2871/endfield.py](https://github.com/Nattapat2871/endfield.py)
🚀 Starting Arknights: Endfield Code Fetcher...

📡 Fetching data from: endfield_gg...
   ✅ Found 4 codes
------------------------------
📡 Fetching data from: gamesradar...
   ✅ Found 1 codes
------------------------------
📡 Fetching data from: ldshop...
   ✅ Found 4 codes
------------------------------

📊 Summary (Total Unique Codes): 4
🎁 Code: ENDFIELDGIFT
   Rewards: Oroberyl x500
   Source: endfield.gg

🎁 Code: ENDFIELD4PC
   Rewards: T-Creds x13,000  Advanced Combat Record x2  Arms INSP Kit x2
   Source: endfield.gg

🎁 Code: ALLFIELD
   Rewards: Oroberyl x1,500  T-Creds x6,000  Elementary Combat Record x30  Arms Inspector x30  Protoprism x5  Protodisk x5  Mark of Perseverance x1
   Source: endfield.gg

🎁 Code: RETURNOFALL
   Rewards: Oroberyl x500  T-Creds x6,000  Elementary Combat Record x30  Arms Inspector x30  Protoprism x5  Protodisk x5
   Source: endfield.gg
```

---

## 📜 License

This project is licensed under the **MIT License**.

**Author:** [nattapat2871](https://github.com/nattapat2871)
