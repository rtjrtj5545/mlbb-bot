# 🆓 Deploy MLBB Bot — 100% FREE FOREVER

**Cost:** $0 — forever. No credit card. No expiration.
**Time:** ~20 minutes once
**How it works:** GitHub runs your bot script automatically every 30 minutes on their free servers.

---

## 📋 What you need

- A free **GitHub account** → [github.com/signup](https://github.com/signup)
- Your **Telegram bot token** (from @BotFather)
- Your **Telegram channel** created, bot added as **admin** with "Post Messages" permission

That's it. No credit card. No payment.

---

# 🎯 STEP 1 — Create your Telegram bot (5 min)

Skip this if you already did it.

1. Open Telegram → search **@BotFather** → start chat
2. Send `/newbot`
3. Choose a name: `NANA MLBB News Bot`
4. Choose a username (must end in `bot`): `nanatopup_mlbb_bot`
5. **Copy the token** BotFather gives you. Looks like:
   `8123456789:AAEexampleTokenStringHere123abcXYZ`
   ⚠️ **Save this somewhere — you'll need it in Step 4.**

6. Create your channel in Telegram (if you don't have one):
   - Tap the pencil icon → **New Channel**
   - Public channel: pick a username like `@nanatopup_mlbb`
   - Or private channel — works too

7. Add your bot to the channel:
   - Open your channel → **Manage** → **Administrators** → **Add Admin**
   - Search your bot name → add it
   - ✅ Enable **"Post Messages"** permission
   - Save

---

# 🎯 STEP 2 — Put code on GitHub (5 min)

### 2.1 — Create a new repo

1. Go to **[github.com/new](https://github.com/new)**
2. **Repository name:** `mlbb-bot`
3. ✅ Set to **Public** ← IMPORTANT! Public = unlimited free runs.
   (Private only gets 2000 min/month free. Public = unlimited.)

   👉 *Don't worry — your secret tokens are NOT in the code. They go in GitHub Secrets, which stays hidden even in a public repo.*

4. ✅ Check **"Add a README file"**
5. Click **Create repository**

### 2.2 — Upload your bot files

1. On the new repo page, click **Add file** → **Upload files**
2. Open your `mlbb-bot` folder on your computer
3. Drag these files into the browser uploader:
   - ✅ `main.py`
   - ✅ `requirements.txt`
   - ✅ `Dockerfile`
   - ✅ `seen.json`
   - ✅ `.gitignore`
   - ✅ `README.md`
   - ❌ **NEVER upload `.env`** (it has your secret token)
4. For the `.github/workflows/poll.yml` file:
   - Click **Add file** → **Create new file**
   - In the filename field type: `.github/workflows/poll.yml` (typing `/` creates folders)
   - Paste the contents of your local `poll.yml`
   - Click **Commit changes**

Alternative (easier): drag the **entire `.github` folder** from your file manager into the GitHub uploader — it preserves the folder structure.

5. Once everything is uploaded → **Commit changes**

✅ Your code is on GitHub.

---

# 🎯 STEP 3 — Add your secrets (3 min)

This is where your bot token goes — safely hidden, never visible in the code.

1. In your GitHub repo, click **Settings** (top right)
2. Left sidebar → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these **4 secrets** one by one:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather (the long string) |
| `TELEGRAM_CHANNEL_ID` | `@your_channel_name` (with @) or `-100123456789` for private |
| `PROMO_LINK` | `https://www.nanatopup.com` |
| `PROMO_NAME` | `NANA TOPUP` |

Each one: click **New repository secret** → fill in **Name** and **Secret** value → **Add secret**.

✅ Secrets are now stored safely.

---

# 🎯 STEP 4 — Enable & test the workflow (2 min)

1. In your repo, click the **Actions** tab (top of repo page)
2. You may see a yellow banner: **"Workflows aren't being run on this repository"** → click **"I understand my workflows, go ahead and enable them"**
3. On the left, you should see **"MLBB Poll"** workflow → click it
4. Click **"Run workflow"** (dropdown on the right) → **Run workflow** (green button)
5. Wait 30 seconds → refresh the page

You'll see a new run appear. Click it to watch live logs:
```
=== MLBB Auto-Update Bot ===
Mode: SINGLE RUN
Channel: @nanatopup_mlbb
Fetched 23 items from 3 sources
Empty seen list — seeding without posting
Seeded 23 items. Next run will post NEW updates.
Done.
```

✅ The first run **seeds silently** (so you don't get 23 old news posts at once).
✅ The **next run** — and every run after — will only post genuinely NEW updates.

---

# 🎯 STEP 5 — That's it! It runs forever.

Your bot now runs automatically every 30 minutes on GitHub's free servers.

When MLBB posts something new:
1. Within ~30 minutes, the bot detects it
2. Translates to Khmer 🇰🇭
3. Posts to your channel with the photo + your nanatopup.com link
4. Stores it in `seen.json` so it never posts twice
5. Repeat — forever — at $0 cost

You can close your laptop. Turn off your phone. The bot keeps running on GitHub.

---

# 📊 How to monitor

### Check it's running
- Repo → **Actions** tab → see green checkmarks for every run
- ✅ Green = success
- ❌ Red = error — click the run to see what went wrong

### See what it posted
- Open your Telegram channel — that's the proof

### Adjust polling frequency
- Edit `.github/workflows/poll.yml` on GitHub (click the pencil icon)
- Change `'*/30 * * * *'` to:
  - `'*/15 * * * *'` → every 15 min (faster, more free minutes used)
  - `'*/60 * * * *'` → every hour (slower, fewer minutes used)
  - `'0 */2 * * *'` → every 2 hours
- Commit the change — takes effect immediately

---

# 💰 Free tier reality

| Setup | Free minutes/month | Your bot uses |
|---|---|---|
| **Public repo** (recommended) | ♾️ **Unlimited** | ~1,440 min/month at 30-min interval |
| Private repo | 2,000 min/month | Need ≥30 min interval to fit |

With a public repo: **literally unlimited free runs forever.** GitHub gives this away.

---

# 🇰🇭 ការណែនាំខ្លីៗជាខ្មែរ

1. **បង្កើត GitHub account** ដោយឥតគិតថ្លៃ
2. **បង្កើត repo "mlbb-bot"** → ជ្រើស **Public** (សំខាន់! ដើម្បីដំណើរការដោយឥតគិតថ្លៃគ្មានដែនកំណត់)
3. **Upload files** ទាំងអស់ លើកលែងតែ `.env`
4. **Settings → Secrets → Actions** → បន្ថែម tokens 4
5. **Actions tab → Run workflow** → ដំណើរការដំបូងបង្អស់ស្ងាត់ៗ (មិនផ្ញើទេ)
6. **រួចហើយ!** Bot នឹងពិនិត្យរៀងរាល់ 30 នាទី — ហើយផ្ញើព័ត៌មានថ្មីភ្លាមៗ

**តម្លៃ: $0 រហូត។ មិនត្រូវការកាត។**

---

# 🆘 Common problems

| Problem | Fix |
|---------|-----|
| **"Workflow not running"** | Check Actions tab — workflows may need to be enabled once after first push |
| **Red ❌ — "Bad Request: chat not found"** | `TELEGRAM_CHANNEL_ID` wrong. For public channels use `@name` with the @. For private channels use the `-100...` ID. |
| **Red ❌ — "Unauthorized"** | `TELEGRAM_BOT_TOKEN` is wrong. Regenerate via @BotFather and update the secret. |
| **Red ❌ — "Forbidden: bot is not a member of the chat"** | Bot was not added as admin to the channel. Add it as admin with Post Messages permission. |
| **Green ✅ but no posts in channel** | First run **seeds silently** — wait for MLBB to actually post something new, OR delete `seen.json` from the repo and re-run (will post recent items) |
| **Cron looks delayed** | Normal — GitHub free cron can be delayed by 5–15 min under load. Not a bug. |
| **Translation comes back in English** | Google Translate temporarily rate-limited the runner's IP. Will work next run. |

---

# 🔄 How to update the bot later

Want to add a new source? Change the format? Add Khmer text?

1. Open the file in your GitHub repo (e.g. `main.py`)
2. Click the **pencil icon** (top right) to edit in browser
3. Make your changes
4. Scroll down → **Commit changes**
5. Next scheduled run uses the new code automatically

Or test it manually: **Actions** tab → **Run workflow**.

---

# 🚫 Want to STOP the bot?

- Repo → **Actions** tab → **MLBB Poll** workflow → **"…"** menu → **Disable workflow**
- Or just delete the repo

No cancellation, no billing, nothing to worry about. It just stops.

---

Made for **nanatopup.com** 💎 — your MLBB Diamond top-up shop in Cambodia 🇰🇭
