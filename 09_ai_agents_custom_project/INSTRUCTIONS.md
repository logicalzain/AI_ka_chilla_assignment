# 🤖 Social Media AI Agents — Complete Guide

> **Read this fully before running any agent.**
> This guide covers setup, usage, dangers, limits, and best practices for all 4 agents.

---

## 📁 Project Structure

```
ai_agents/
├── INSTRUCTIONS.md                    ← You are here
├── requirements.txt                   ← All Python dependencies
│
├── instagram_agent/
│   └── instagram_agent.ipynb          ← Instagram AI Agent
│
├── linkedin_agent/
│   └── linkedin_agent.ipynb           ← LinkedIn AI Agent
│
├── ticktock_agent/
│   └── tiktok_agent.ipynb             ← TikTok AI Agent
│
└── watsapp_agent/
    └── whatsapp_agent.ipynb           ← WhatsApp AI Agent
```

---

## ⚙️ Setup & Installation

### Step 1 — Create a Python Environment (Recommended)

```bash
# Using conda (recommended)
conda create -n social_agents python=3.11
conda activate social_agents

# OR using venv
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux
```

### Step 2 — Install All Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Install Playwright (needed for TikTok)

```bash
playwright install chromium
```

### Step 4 — Install Google Chrome

All Selenium-based agents (LinkedIn, TikTok, WhatsApp) require **Google Chrome** to be installed on your machine.  
Download: https://www.google.com/chrome/

### Step 5 — Open the Notebook

Open any `.ipynb` file in VS Code or Jupyter Lab, then run cells **from top to bottom** in order.

---

## 🔐 Credentials — Where to Put Them

### Instagram Agent

In **Cell 2**, the notebook will ask interactively:
```
Instagram username: your_username
Instagram password: ••••••••
```
- Your session is saved to `session_YOUR_USERNAME.json` in the same folder.
- ✅ You only need to log in once per session file.
- ⚠️ Never share or commit `session_*.json` files — they give full account access.

---

### LinkedIn Agent

In **Cell 2**, the notebook will ask interactively:
```
LinkedIn email:    your@email.com
LinkedIn password: ••••••••
```
- Cookies are saved to `li_cookies_YOUR_EMAIL.pkl`.
- ✅ Reused on next run automatically.
- ⚠️ Never share `.pkl` cookie files.

---

### TikTok Agent

In **Cell 2**, the notebook will ask interactively:
```
TikTok username (or email): your@email.com
TikTok password: ••••••••
```
- Cookies saved to `tiktok_cookies_YOUR_EMAIL.pkl`.
- ⚠️ TikTok may show a **CAPTCHA** on first login. A browser window opens — solve it manually, then press Enter in the notebook.
- ✅ After solving once, cookies are saved and CAPTCHA won't appear again (usually).

---

### WhatsApp Agent

In **Cell 2**, **no username/password needed** — WhatsApp uses QR code login:
1. A Chrome browser opens automatically.
2. Open WhatsApp on your phone → ⋮ Menu → Linked Devices → Link a Device.
3. Scan the QR code shown in the browser.
4. ✅ Session saved permanently in `whatsapp_session/` folder. Never scan again.

> **Do NOT delete the `whatsapp_session/` folder** or you'll need to re-scan.

---

## 🔧 How to Use Each Agent

### Common Pattern (All Agents)

1. Run **Cell 1** — loads imports and the human behavior engine
2. Run **Cell 2** — logs in (enter credentials when prompted)
3. Run any feature cell you need (they are independent after login)
4. Uncomment the example lines at the bottom of each cell to use them

### Example — Instagram: Like Posts from a Hashtag

Go to **Cell 5** (Like & Unlike Posts), uncomment and run:
```python
like_posts_by_hashtag("photography", count=5)
```

### Example — Instagram: Upload a Photo

Go to **Cell 3** (Upload Photo), uncomment and run:
```python
m = upload_photo("photo.jpg", caption="Good morning! 🌞\n\n#morning #vibes")
```

### Example — WhatsApp: Send a Scheduled Message

Go to **Cell 11** (Scheduler), uncomment and run:
```python
schedule_message("Mom", "Good morning! ☀️", hour=8, minute=0)
run_scheduler()
```
> Keep the notebook running — the scheduler runs in a background thread.

---

## ✅ Pros — What These Agents Do Well

| Feature | Detail |
|---|---|
| **Session Persistence** | Login once, run forever (cookies/session files) |
| **Human-like Delays** | Random waits (1.5s–25s) between every action |
| **Typing Simulation** | Character-by-character typing at real human speed |
| **Skip Probability** | Doesn't like every post — mimics real browsing |
| **Video Watch Simulation** | Watches for a random duration before interacting |
| **Scheduler** | Run posts at specific times automatically |
| **Auto-Reply Bot** | WhatsApp keyword-based auto-replies |
| **Analytics** | View likes, comments, views, follower counts |
| **Bulk Actions** | Follow users from hashtags, bulk DMs with delays |
| **Modular Design** | Each cell is independent — run only what you need |
| **Undetected Chrome** | Uses `undetected-chromedriver` to hide automation |

---

## ❌ Cons — Limitations to Know

| Limitation | Detail |
|---|---|
| **Requires Chrome** | LinkedIn, TikTok, WhatsApp need Google Chrome installed |
| **Not Fully Headless** | Running fully headless (no visible browser) is easily detected |
| **CAPTCHA** | TikTok and LinkedIn may show CAPTCHAs — must solve manually |
| **UI Changes Break Code** | CSS selectors may break when platforms update their UI |
| **Rate Limits** | Too many actions too fast will trigger temporary bans |
| **2FA** | Two-factor authentication requires manual intervention |
| **Video Upload Slow** | Large video uploads can take minutes — don't close the notebook |
| **WhatsApp Business** | Works only with personal WhatsApp, not WhatsApp Business API |
| **TikTok DMs** | TikTok restricts DMs to mutual followers — may get blocked |
| **IP-based Limits** | Same IP doing too much = flag. Use residential internet, not VPN |

---

## ⚠️ Dangers & Risks — Read Carefully

### 🔴 Account Ban Risk

Every social media platform **prohibits automation** in their Terms of Service.  
Using these agents carries a risk of:
- Temporary action blocks (likes/comments disabled for hours/days)
- Permanent account suspension
- Phone number ban (WhatsApp)

**Mitigation:**
- Keep action counts **low** (3–10 per session, not hundreds)
- Run agents **once or twice per day**, not continuously
- Use `long_delay()` between actions
- Do not run agents on brand-new or unverified accounts

---

### 🔴 Credential Security

- Your username and password are entered interactively — they are **never stored in the notebook**.
- Session files (`.json`, `.pkl`, folders) **contain your login tokens** — these are as sensitive as your password.

**Rules:**
- ✅ Add these to `.gitignore` before using Git:
  ```
  session_*.json
  *_cookies*.pkl
  whatsapp_session/
  tiktok_cookies*.pkl
  ```
- ❌ Never upload session files to GitHub, Google Drive, or share them.
- ❌ Never run these agents on a shared/public computer.

---

### 🔴 Legal Risks

- Scraping and automation may violate platform Terms of Service.
- In some countries, unauthorized scraping is illegal under computer misuse laws.
- Sending unsolicited bulk messages (spam) may violate anti-spam laws (CAN-SPAM, GDPR).
- **Use these tools only for your own accounts and legitimate content creation.**

---

### 🟡 WhatsApp Specific Warnings

- WhatsApp actively detects automation. Sending too many messages too fast leads to a **permanent phone number ban**.
- Minimum recommended delay between bulk messages: **60–180 seconds**.
- Do NOT send the same message to 50+ people in one session.
- Do NOT use `send_bulk_messages()` for marketing/spam — only for personal use.

---

### 🟡 TikTok Specific Warnings

- TikTok uses advanced bot detection (device fingerprinting, behavior analysis).
- Always keep the browser window **visible** (not minimized) during automation.
- If CAPTCHA appears frequently, your IP may be flagged — wait 24 hours.
- Do not upload more than **1–3 videos per day** via automation.

---

### 🟡 Instagram Specific Warnings

- Instagram's action limits (per hour/day):
  - Likes: ~300/day max
  - Comments: ~100/day max
  - Follows: ~150/day max
  - DMs: ~50/day max
- The agents are set far below these limits but **do not increase the counts manually**.
- If you see "Action Blocked" in the app, stop the agent for 24–48 hours.

---

### 🟡 LinkedIn Specific Warnings

- LinkedIn limits connection requests to **~100/week** for regular accounts.
- Excessive scraping of LinkedIn profiles can trigger **LinkedIn Restricted Mode**.
- Do not send the same message template to hundreds of people — it will be flagged as spam.

---

## 🛡️ Best Practices to Stay Safe

1. **Run agents during your normal active hours** — don't run at 3AM if you normally sleep then.
2. **Vary your actions** — don't run the same function every day at the exact same time.
3. **Start slow** — first week: max 5 likes/day. Gradually increase over weeks.
4. **Keep a real presence** — occasionally log in normally (as a human) and browse.
5. **Monitor your accounts** — check for warnings, appeals, or suspicious login alerts.
6. **Use your home internet** — avoid VPNs, data centers, or cloud server IPs.
7. **One account per machine** — don't run multiple accounts from the same browser profile.
8. **Don't run 24/7** — simulate normal usage (1–3 sessions per day, 15–45 min each).

---

## 🔢 Recommended Action Limits (Per Day)

| Action | Instagram | LinkedIn | TikTok | WhatsApp |
|---|---|---|---|---|
| Likes | 20–50 | 15–30 | 20–50 | N/A |
| Comments | 5–15 | 5–10 | 5–10 | N/A |
| Follows | 10–20 | 5–10 | 10–20 | N/A |
| DMs/Messages | 5–10 | 5–10 | 3–5 | 10–20 |
| Posts/Uploads | 1–2 | 1–2 | 1–2 | Unlimited (be reasonable) |
| Story Views | 20–50 | N/A | N/A | N/A |

---

## 🔄 Updating the Agents

If a platform updates its UI and the agent breaks:
1. Open browser DevTools (F12) on the platform
2. Find the new CSS selector for the broken element
3. Update the CSS selector string in the corresponding cell
4. The `wait(driver, "CSS_SELECTOR")` calls are where selectors live

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `LoginRequired` | Instagram session expired | Delete `session_*.json`, re-run Cell 2 |
| `TimeoutException` | Element not found in time | Platform UI changed, update CSS selector |
| `SessionNotCreatedException` | Chrome version mismatch | Update Chrome or run `pip install --upgrade undetected-chromedriver` |
| `CAPTCHA detected` | Bot detection triggered | Solve manually in browser, wait 24h before retrying |
| `Action Blocked` | Instagram rate limit hit | Stop agent, wait 24–48 hours |
| `ModuleNotFoundError` | Package not installed | Run `pip install -r requirements.txt` |
| `FileNotFoundError` | Wrong file path for upload | Always use absolute paths for media files |
| QR code keeps refreshing | WhatsApp Web timeout | Re-run Cell 2, scan faster |

---

## 📌 Quick Reference — Agent Cell Map

### Instagram (`instagram_agent.ipynb`)
| Cell | Feature |
|---|---|
| 1 | Imports & human engine |
| 2 | Login |
| 3 | Upload Photo |
| 4 | Upload Video / Reel |
| 5 | Like Posts by Hashtag |
| 6 | Comment & Reply |
| 7 | Follow / Unfollow |
| 8 | Watch Stories |
| 9 | Send DMs |
| 10 | Post Analytics |
| 11 | Search Hashtags |
| 12 | Scheduler |
| 13 | Daily Routine (one-click) |

### LinkedIn (`linkedin_agent.ipynb`)
| Cell | Feature |
|---|---|
| 1 | Imports & human engine |
| 2 | Login |
| 3 | Text Post |
| 4 | Media Post (image/video) |
| 5 | Like Feed Posts |
| 6 | Comment & Reply |
| 7 | Connection Requests |
| 8 | Send DMs |
| 9 | Search People & Jobs |
| 10 | Post Analytics |
| 11 | Scheduler |
| 12 | Close Browser |

### TikTok (`tiktok_agent.ipynb`)
| Cell | Feature |
|---|---|
| 1 | Imports & human engine |
| 2 | Login |
| 3 | Upload Video |
| 4 | Browse FYP & Like |
| 5 | Comment & Reply |
| 6 | Follow / Unfollow |
| 7 | Analytics |
| 8 | Search Hashtag |
| 9 | Send DMs |
| 10 | Scheduler |
| 11 | Daily Routine (one-click) |
| 12 | Close Browser |

### WhatsApp (`whatsapp_agent.ipynb`)
| Cell | Feature |
|---|---|
| 1 | Imports & human engine |
| 2 | QR Login |
| 3 | Open Chat |
| 4 | Send Text Message |
| 5 | Send Media (image/video/file) |
| 6 | Read Unread Messages |
| 7 | React to Messages |
| 8 | Reply to Message |
| 9 | Group Messages & Bulk Send |
| 10 | Auto-Reply Bot |
| 11 | Scheduler |
| 12 | Search Contacts |
| 13 | Close Browser |

---

## ⚖️ Disclaimer

These agents are built for **personal content creator use only** — managing your own accounts, scheduling your own posts, and engaging with your community.

**Do NOT use these agents for:**
- Spam or mass unsolicited messaging
- Fake engagement (buying followers, fake likes)
- Scraping user data for commercial purposes
- Harassing or targeting other users
- Any activity that violates local laws

The developer takes no responsibility for account bans, legal issues, or any consequences arising from misuse of these tools.
