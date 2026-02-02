# Arknights: Endfield - Unofficial Automation Tools

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A collection of unofficial Python scripts to help automate tasks for **Arknights: Endfield**. This repository includes tools for daily check-ins and fetching the latest gift codes from various community sources.

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

#### **Setup:**
1.  Open `endfield_checkin.py`.
2.  Locate the **Configuration Section** at the top of the file.
3.  Fill in your `CRED` and `ROLE_ID`.
    * *Note: You can find these values by inspecting network traffic (F12) on the official check-in page.*

```python
# 👇 ACCOUNT SETTINGS (Fill in your credentials here)
CRED = "YOUR_CRED_HERE"      # <--- Enter your credential key
ROLE_ID = "YOUR_ROLE_ID"     # <--- Enter your role ID
```

#### **How to Run:**
```bash
python endfield_checkin.py
```

**Features:**
* ✅ Auto-generates required cryptographic signatures.
* ✅ Claims daily rewards if not already claimed.
* ✅ Displays received items and current calendar progress.

---

### 2. Gift Code Fetcher (`endfield_code_fetcher.py`)

This script scrapes various websites to find the latest promo codes.

#### **How to Run:**
```bash
python endfield_code_fetcher.py
```

**Features:**
* ✅ Asynchronous fetching (fast execution).
* ✅ Scrapes from multiple sources (`endfield.gg`, `gamesradar`, `ldshop`).
* ✅ Dedupes codes automatically.
* ✅ Sanitizes codes (removes spaces, converts to uppercase).

---

## 📜 License

This project is licensed under the **MIT License**.

**Author:** [nattapat2871](https://github.com/nattapat2871)
