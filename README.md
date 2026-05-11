# MLBB Auto-Update Telegram Bot 🎮

Auto-monitors Mobile Legends: Bang Bang news sources, translates updates into **Khmer (ខ្មែរ)**, and posts to your Telegram channel with a photo/video + your **www.nanatopup.com** link in every caption.

---

## 🇰🇭 ការណែនាំជាភាសាខ្មែរ

ឧបករណ៍នេះនឹង៖
- ឃ្លាំមើល MLBB News, YouTube, និង Wiki ដោយស្វ័យប្រវត្តិ
- រាល់ពេលមានព័ត៌មានថ្មី — បកប្រែជាខ្មែរ
- ផ្ញើទៅ Telegram Channel របស់អ្នកជាមួយរូបភាព និងតំណ **www.nanatopup.com**

---

## ✅ What it does

| Step | Action |
|------|--------|
| 1 | Polls MLBB official news, YouTube channel, and fan wiki every 15 min |
| 2 | Detects items it hasn't seen before |
| 3 | Translates title + summary into Khmer using Google Translate |
| 4 | Sends to your Telegram channel as a **photo + caption** (or text if no image) |
| 5 | Adds `www.nanatopup.com` promo link to every post |

---

## 📦 Setup (one-time)

### 1. Install Python 3.10+

```bash
python --version   # must be 3.10 or newer
```

### 2. Download & install dependencies

```bash
cd mlbb-bot
pip install -r requirements.txt
```

### 3. Create your Telegram bot

1. Open Telegram → search **@BotFather**
2. Send `/newbot` → follow prompts → copy the **bot token**
3. Create your channel (or use existing one)
4. Add the bot to your channel as **Administrator** with "Post Messages" permission
5. Get your channel ID:
   - Public channel: just use `@yourchannelname`
   - Private channel: forward any message from the channel to **@userinfobot** and copy the `-100xxxxxxxxxx` ID

### 4. Configure

```bash
cp .env.example .env
nano .env
```

Fill in:
```env
TELEGRAM_BOT_TOKEN=8123456789:AAFexampleTokenFromBotFather
TELEGRAM_CHANNEL_ID=@nanatopup_mlbb_news
PROMO_LINK=https://www.nanatopup.com
PROMO_NAME=NANA TOPUP
POLL_MINUTES=15
```

### 5. Run

```bash
python main.py
```

The first run will only **seed** existing news (so you don't get spammed with 50 old posts). From the next cycle onward, only **NEW** updates will be sent.

---

## 🚀 Run 24/7 (production)

### Option A — Linux server with systemd

Create `/etc/systemd/system/mlbb-bot.service`:

```ini
[Unit]
Description=MLBB Auto Update Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/mlbb-bot
ExecStart=/usr/bin/python3 /home/ubuntu/mlbb-bot/main.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now mlbb-bot
sudo systemctl status mlbb-bot
journalctl -u mlbb-bot -f          # live logs
```

### Option B — Free hosting (Railway / Render / Fly.io)

1. Push project to a GitHub repo
2. On Railway.app → New Project → Deploy from GitHub
3. Add env vars from `.env` in the dashboard
4. Set start command: `python main.py`
5. Deploy ✅ — runs forever

### Option C — Run on your PC

Use Windows Task Scheduler or just keep a terminal open:
```bash
python main.py
```

---

## 🔧 Customize

### Add more sources
Edit `SOURCES` in `main.py`. Supported types:
- **rss** — any RSS/Atom feed (YouTube channels, blogs)
- **html** — any webpage, with a CSS selector for items

YouTube channel RSS format:
```
https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxxxxx
```

### Change post format
Edit `build_caption()` in `main.py` — change emojis, layout, language mix, etc.

### Change translation target
In `translate_khmer()`, change `target="km"` to any language code (e.g. `"th"` for Thai).

---

## 📝 Files

```
mlbb-bot/
├── main.py              # the bot
├── requirements.txt     # Python dependencies
├── .env.example         # config template (copy to .env)
├── .env                 # YOUR secrets (do not share)
├── seen.json            # auto-created — tracks posted items
├── bot.log              # auto-created — runtime logs
└── README.md            # this file
```

---

## ⚠️ Notes

- **Facebook & Instagram** can't be reliably auto-scraped (they actively block bots). For those, the most reliable path is Meta's Graph API with a Page Access Token — possible but requires app review. The official MLBB site + YouTube + Wiki cover ~95% of real news.
- **Google Translate** via `deep-translator` is free but rate-limited. For high-volume use, get a paid Google Cloud Translate API key.
- The bot stores posted items in `seen.json` — don't delete it unless you want re-posts.
- Telegram caption limit is 1024 chars for photos. Longer items send as text-only.

---

## 🆘 Troubleshooting

| Problem | Fix |
|--------|------|
| "Chat not found" | Bot isn't in the channel, or channel ID wrong |
| "Forbidden: bot is not a member" | Add bot as admin in your channel |
| No new posts ever | First run seeds existing items — wait for an actual new update, or delete `seen.json` to repost everything |
| Translation in English | Google Translate temporarily blocked your IP — wait or use a paid key |
| Photos missing | Source page changed layout — adjust the `item_selector` in SOURCES |

---

Made for nanatopup.com 💎
