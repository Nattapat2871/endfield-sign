
// ========================================================================================
// Project: Arknights: Endfield Auto Check-in Script
// Author: nattapat2871
// Github: https://github.com/Nattapat2871/endfield-sign
// ========================================================================================



// =========================================================
// 👇 ACCOUNT SETTINGS
// =========================================================
const ACCOUNT_LIST = [
  {
    "name": "Main Account",
    "token": "",  // Enter your ACCOUNT_TOKEN here
    "roleId": "" // Enter your SK_GAME_ROLE here
  },

   // If you want to add multiple accounts, you can keep increasing this amount.
   // { 
     // "name": "Sub Account",         
     // "token": "",  
     // "roleId": "" 
   // }
];

// If you don't want to use Discord, you can leave it as "YOUR_DISCORD_WEBHOOK_URL_HERE" or "".
const DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"; 
// =========================================================

//     ---- This is all that needs to be fixed. ----

















/**  this script made by Nattapat2871    **/
/**  After this line is the script code. Please DO NOT modify. **/
/**  This script is .gs and works only in Google app script.  (https://script.google.com)  */

const APP_CODE = "6eb76d4e13aa36e6";
const BASE_URL = "https://zonai.skport.com";


// เช็คว่าผู้ใช้ตั้งค่า Discord ไว้หรือไม่
function isDiscordEnabled() {
  return DISCORD_WEBHOOK_URL && DISCORD_WEBHOOK_URL.indexOf("http") === 0 && DISCORD_WEBHOOK_URL !== "YOUR_DISCORD_WEBHOOK_URL_HERE";
}

// ฟังก์ชันหลักที่ใช้ในการรันสคริปต์
function runFullProcess() {
  if (ACCOUNT_LIST.length === 0) {
    Logger.log("❌ Error: Missing ACCOUNT_LIST.");
    return;
  }

  Logger.log("🚀 Starting check-in for " + ACCOUNT_LIST.length + " accounts...");
  if (!isDiscordEnabled()) {
    Logger.log("ℹ️ Discord notification is DISABLED. Only logging to console.");
  }

  // วนลูปเพื่อเช็คอินทีละไอดี
  for (let i = 0; i < ACCOUNT_LIST.length; i++) {
    const account = ACCOUNT_LIST[i];
    Logger.log("--- Processing Account: " + account.name + " ---");

    const ts = Math.floor(Date.now() / 1000).toString();

    // =======================================================
    // --- 0. สร้าง cred และเตรียมข้อมูลการยืนยันตัวตน ---
    // =======================================================
    let cred, salt;
    try {
      const authData = performOauthFlow(account.token);
      cred = authData.cred;
      salt = authData.salt;
    } catch (e) {
      Logger.log("❌ Auth Failed for " + account.name + ": " + e.message);
      sendToDiscord("❌ Auth Failed", e.message, 16711680, account.name); 
      continue; // ข้ามไปทำไอดีถัดไปทันที
    }

    // =======================================================
    // --- 1. ดึงข้อมูลโปรไฟล์ ---
    // =======================================================
    const profilePath = "/web/v2/user";
    const headersProfile = getHeaders(profilePath, ts, cred, salt, account.roleId);
    
    let username = "Unknown", uid = "Unknown", avatarUrl = "";
    try {
      const resProfile = UrlFetchApp.fetch(BASE_URL + profilePath, {
        method: "get",
        headers: headersProfile,
        muteHttpExceptions: true
      });
      const profileData = JSON.parse(resProfile.getContentText());
      if (profileData.code === 0) {
        const basicUser = profileData.data.user.basicUser;
        username = basicUser.nickname || "Unknown";
        uid = basicUser.id || "Unknown";
        avatarUrl = basicUser.avatar || "";
      }
    } catch (e) {
      Logger.log("💥 Profile Fetch Error: " + e.message);
    }

    // =======================================================
    // --- ดำเนินการเช็คอิน (Check-in Logic) ---
    // =======================================================
    const checkinPath = "/web/v1/game/endfield/attendance";
    const checkinUrl = BASE_URL + checkinPath;
    
    const tsCheck = Math.floor(Date.now() / 1000).toString();
    const headersCheck = getHeaders(checkinPath, tsCheck, cred, salt, account.roleId);
    
    const resStatus = UrlFetchApp.fetch(checkinUrl, {
      method: "get",
      headers: headersCheck,
      muteHttpExceptions: true
    });
    
    const statusData = JSON.parse(resStatus.getContentText());
    if (statusData.code !== 0) {
      Logger.log("❌ Error fetching calendar for " + account.name);
      sendToDiscord("❌ Error Fetching Calendar", statusData.message, 16711680, account.name, avatarUrl);
      continue; 
    }

    const data = statusData.data || {};
    const calendar = data.calendar || [];
    const resMap = data.resourceInfoMap || {};
    const totalDays = calendar.length;
    
    const alreadyClaimed = data.hasToday || false;
    let claimedCount = calendar.filter(day => day.done).length;

    let checkinResultMsg = "";
    let todayIdx;
    let isSuccess = false;

    if (alreadyClaimed) {
      checkinResultMsg = "✅ Already signed in today.";
      todayIdx = claimedCount - 1;
      isSuccess = true;
    } else {
      const tsPost = Math.floor(Date.now() / 1000).toString();
      const headersPost = getHeaders(checkinPath, tsPost, cred, salt, account.roleId);
      
      const resPost = UrlFetchApp.fetch(checkinUrl, {
        method: "post",
        headers: headersPost,
        muteHttpExceptions: true
      });
      
      const postData = JSON.parse(resPost.getContentText());
      if (postData.code === 0) {
        checkinResultMsg = "🎉 Success! Reward claimed.";
        todayIdx = claimedCount;
        claimedCount += 1;
        isSuccess = true;
      } else {
        checkinResultMsg = "❌ Claim Failed: " + postData.message;
        todayIdx = claimedCount;
      }
    }

    let todayAwardName = "Unknown";
    let todayAwardCount = 0;
    let todayAwardIcon = "";

    if (todayIdx >= 0 && todayIdx < totalDays) {
      const awardId = calendar[todayIdx].awardId;
      const info = resMap[awardId] || {};
      todayAwardName = info.name || awardId;
      todayAwardCount = info.count || 1;
      todayAwardIcon = info.icon || "";
    }

    Logger.log("Result: " + checkinResultMsg + " | " + todayAwardName + " x" + todayAwardCount);

    // =======================================================
    // --- ส่งข้อมูลไปยัง Discord ---
    // =======================================================
    if (isDiscordEnabled()) {
      const embedColor = isSuccess ? 3066993 : 16711680;
      
      const discordPayload = {
        "username": "Endfield Bot",
        "avatar_url": "https://static.skport.com/image/common/20251031/46750c47729f845b4db6c404e12f771c.png",
        "embeds": [{
          "author": {
            "name": account.name, 
            "icon_url": avatarUrl
          },
          "title": "Arknights: Endfield Check-in",
          "description": checkinResultMsg,
          "color": embedColor,
          "fields": [
            { "name": "👤 Username", "value": username + " (UID: " + uid + ")", "inline": false },
            { "name": "📅 Progress", "value": claimedCount + " / " + totalDays + " days", "inline": true },
            { "name": "🎁 Today's Reward", "value": todayAwardName + " x" + todayAwardCount, "inline": true }
          ],
          "thumbnail": {
            "url": todayAwardIcon
          },
          "timestamp": new Date().toISOString(),
          "footer": {
            "text": "Skport Auto Check-in"
          }
        }]
      };

      try {
        UrlFetchApp.fetch(DISCORD_WEBHOOK_URL, {
          method: "post",
          contentType: "application/json",
          payload: JSON.stringify(discordPayload)
        });
      } catch (e) {
        Logger.log("⚠️ Failed to send to Discord: " + e.message);
      }
    }

    Logger.log("✅ Done for " + account.name + "! Progress: " + claimedCount + "/" + totalDays);

    // ⏳ หน่วงเวลา 1.5 วินาที ก่อนจะเริ่มเช็คอินไอดีถัดไป
    if (i < ACCOUNT_LIST.length - 1) {
      Utilities.sleep(1500); 
    }
  }
}


// =========================================================
// Helper Functions
// =========================================================

function performOauthFlow(accountToken) {
  const encodedToken = encodeURIComponent(accountToken);
  
  // Step 1: Info
  const infoUrl = "https://as.gryphline.com/user/info/v1/basic?token=" + encodedToken;
  const infoRes = UrlFetchApp.fetch(infoUrl, { muteHttpExceptions: true });
  const infoData = JSON.parse(infoRes.getContentText());
  if (infoData.status !== 0) throw new Error("OAuth Step 1 Failed: " + infoData.msg);

  // Step 2: Grant
  const grantUrl = "https://as.gryphline.com/user/oauth2/v2/grant";
  const grantRes = UrlFetchApp.fetch(grantUrl, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ "token": accountToken, "appCode": APP_CODE, "type": 0 }),
    muteHttpExceptions: true
  });
  const grantData = JSON.parse(grantRes.getContentText());
  if (grantData.status !== 0 || !grantData.data || !grantData.data.code) {
    throw new Error("OAuth Step 2 Failed: " + grantData.msg);
  }
  const authCode = grantData.data.code;

  // Step 3: Generate Cred
  const credUrl = BASE_URL + "/web/v1/user/auth/generate_cred_by_code";
  const credRes = UrlFetchApp.fetch(credUrl, {
    method: "post",
    headers: { "platform": "3", "content-type": "application/json" },
    payload: JSON.stringify({ "code": authCode, "kind": 1 }),
    muteHttpExceptions: true
  });
  const credData = JSON.parse(credRes.getContentText());
  if (credData.code !== 0 || !credData.data || !credData.data.cred) {
    throw new Error("OAuth Step 3 Failed: " + credData.message);
  }
  
  return { cred: credData.data.cred, salt: credData.data.token };
}

function generateSign(path, timestamp, salt) {
  const headerDict = { "platform": "3", "timestamp": timestamp, "dId": "", "vName": "1.0.0" };
  const jsonStr = JSON.stringify(headerDict).replace(/\s/g, ""); 
  const s = path + timestamp + jsonStr;
  
  // HMAC-SHA256
  const hmacBytes = Utilities.computeHmacSha256Signature(s, salt);
  const hmacHex = bytesToHex(hmacBytes);
  
  // MD5
  const md5Bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, hmacHex);
  return bytesToHex(md5Bytes);
}

function getHeaders(path, timestamp, cred, salt, roleId) {
  const sign = generateSign(path, timestamp, salt);
  return {
    "cred": cred,
    "sk-game-role": roleId,
    "platform": "3",
    "sk-language": "en",
    "timestamp": timestamp,
    "vname": "1.0.0",
    "sign": sign,
    "User-Agent": "Skport/0.7.0 (com.gryphline.skport; build:700089; Android 33; ) Okhttp/5.1.0",
    "content-type": "application/json",
    "accept": "application/json, text/plain, */*"
  };
}

function bytesToHex(bytes) {
  return bytes.map(function(byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join('');
}

function sendToDiscord(title, description, color, accountName, iconUrl) {
  if (!isDiscordEnabled()) return;
  const payload = {
    "username": "Endfield Bot",
    "avatar_url": BOT_AVATAR_URL,
    "embeds": [{
      "author": {
        "name": accountName || "Unknown Account",
        "icon_url": iconUrl || "https://i.imgur.com/example_icon.png"
      },
      "title": title,
      "description": description,
      "color": color || 16711680,
      "timestamp": new Date().toISOString() 
    }]
  };
  UrlFetchApp.fetch(DISCORD_WEBHOOK_URL, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
}
