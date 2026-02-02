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

## 🚀 Usage Guide

### 1. Daily Check-in (`endfield_checkin.py`)

This script communicates directly with the game servers to perform the daily check-in.

#### **💻 How to get Credentials (Endfield)**
Follow these steps to connect the script to your account:

1.  Log in to [SKPort Endfield Portal](https://game.skport.com/endfield/sign-in).
2.  Open Developer Tools (Press `F12`) -> Go to the **Network** tab.
3.  Refresh the page and find a request named `zonai.skport.com` or `attendance`.
4.  In **Request Headers**, find the `cred` and `sk-game-role` values.

#### **Setup:**
Once you have the values from the steps above, open `endfield_checkin.py` and paste them into the configuration section:

```python
# 👇 ACCOUNT SETTINGS
CRED = "YOUR_COPIED_CRED_VALUE"          # <--- Paste 'cred' here
ROLE_ID = "YOUR_COPIED_SK_GAME_ROLE"     # <--- Paste 'sk-game-role' here
```

#### **How to Run:**
```bash
python endfield_checkin.py
```

#### **📜 Example Output:**
```text
(.venv) PS E:\devlopers_app\Skript\Project Focalor\tests> python endfield_checkin.py
⌨️ Github: [https://github.com/Nattapat2871/endfield.py](https://github.com/Nattapat2871/endfield.py)
🚀 Starting Arknights: Endfield Check-in System
👤 Target Role ID: 3_4492964822_2
----------------------------------------
🔍 1. Fetching user profile...
   👤 Nickname: Nattapat2871
   🆔 User ID: 7305348574810
   🖼️ Avatar URL: [https://static.skport.com/image/common/20251031/46750c47729f845b4db6c404e12f771c.png](https://static.skport.com/image/common/20251031/46750c47729f845b4db6c404e12f771c.png)
----------------------------------------
🔄 2. Sending check-in request...
   ✅ Already checked in today. (No action needed)
----------------------------------------
📅 3. Summarizing calendar status...
   📊 Progress: Claimed 2 / 28 days
   [Recent 3 Days Status]
      Day 1: Intermediate Combat Record x2 -> ✅ Claimed
            🖼️ Icon: [https://static.skport.com/asset/endfield_attendance/921A397E2765462C009B939E0CD92606.png](https://static.skport.com/asset/endfield_attendance/921A397E2765462C009B939E0CD92606.png)
      Day 2: Arms INSP Kit x2 -> ✅ Claimed
            🖼️ Icon: [https://static.skport.com/asset/endfield_attendance/0dea0bc0fd87138df322e8a254a6999f.png](https://static.skport.com/asset/endfield_attendance/0dea0bc0fd87138df322e8a254a6999f.png)
      Day 3: Talosian Credit Notes|T-Creds x2000 -> ⬜ Pending
            🖼️ Icon: [https://static.skport.com/asset/endfield_attendance/2a58a0e85f39092433842ccd62324785.png](https://static.skport.com/asset/endfield_attendance/2a58a0e85f39092433842ccd62324785.png)
----------------------------------------
✨ Process Completed.
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
