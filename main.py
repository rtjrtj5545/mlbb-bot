"""
MLBB Auto-Update Telegram Bot — Cambodia Edition 🇰🇭
-----------------------------------------------------
Watches MLBB Cambodia YouTube + MPL Cambodia YouTube, translates new posts
into Khmer, and forwards them to your Telegram channel with your
www.nanatopup.com link attached.
"""

import os
import json
import time
import logging
import hashlib
import html
import re
from pathlib import Path

import requests
import feedparser
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------- CONFIG ----------
BOT_TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID    = os.getenv("TELEGRAM_CHANNEL_ID", "")
PROMO_LINK    = os.getenv("PROMO_LINK", "https://www.nanatopup.com")
PROMO_NAME    = os.getenv("PROMO_NAME", "NANA TOPUP")
POLL_MINUTES  = int(os.getenv("POLL_MINUTES", "15"))
SEEN_FILE     = Path("seen.json")
LOG_FILE      = Path("bot.log")

IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
SINGLE_RUN = os.getenv("SINGLE_RUN", "1" if IS_GITHUB_ACTIONS else "0") == "1"

# 🇰🇭 Cambodia-only sources
SOURCES = [
    # 1. MLBB Cambodia YouTube — @mobilelegendsbangbangcambodia
    {
        "name": "MLBB Cambodia YouTube 🇰🇭",
        "type": "rss",
        "url":  "https://www.youtube.com/feeds/videos.xml?channel_id=UC_AO5MJxx4tBCh5nlMkYoEg",
    },
    # 2. MPL Cambodia YouTube — @MPLCambodia_Official
    {
        "name": "MPL Cambodia YouTube 🏆",
        "type": "rss",
        "url":  "https://www.youtube.com/feeds/videos.xml?channel_id=UCuB5vb6-ZONbfYUIAXr6EsA",
    },
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"),
              logging.StreamHandler()],
)
log = logging.getLogger("mlbb-bot")


# ---------- SEEN STORAGE ----------
# Stored as an ordered list in JSON. Oldest first, newest last.
# Trimming is deterministic (always drops oldest, never randomly).
def load_seen() -> list:
    if SEEN_FILE.exists():
        try:
            data = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return list(data)
        except Exception:
            pass
    return []


def save_seen(seen_list: list) -> None:
    trimmed = seen_list[-2000:]
    SEEN_FILE.write_text(
        json.dumps(trimmed, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def make_id(item: dict) -> str:
    """Prefer the feed's stable entry id (e.g. yt:video:VIDEOID) over hashing
    title+url — that way fixed typos in a title don't cause re-posts."""
    fid = item.get("feed_id") or ""
    if fid:
        return fid
    raw = f"{item.get('url','')}|{item.get('title','')}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


# ---------- FETCHERS ----------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0 Safari/537.36"
}


def fetch_rss(src: dict) -> list:
    items = []
    feed = feedparser.parse(src["url"])
    for entry in feed.entries[:10]:
        media = None
        if "media_thumbnail" in entry and entry.media_thumbnail:
            media = entry.media_thumbnail[0].get("url")
        elif "media_content" in entry and entry.media_content:
            media = entry.media_content[0].get("url")
        items.append({
            "title":   entry.get("title", "").strip(),
            "url":     entry.get("link", "").strip(),
            "summary": BeautifulSoup(entry.get("summary", ""), "html.parser")
                       .get_text(" ", strip=True)[:400],
            "image":   media,
            "source":  src["name"],
            "feed_id": entry.get("id", "").strip(),   # YouTube → yt:video:XXXX
        })
    return items


def fetch_html(src: dict) -> list:
    """Kept for future use if you want to add a non-RSS source again."""
    items = []
    try:
        r = requests.get(src["url"], headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        log.warning(f"{src['name']} fetch failed: {e}")
        return items

    soup = BeautifulSoup(r.text, "html.parser")
    nodes = soup.select(src["item_selector"])[:15]
    base = re.match(r"https?://[^/]+", src["url"]).group(0)
    for n in nodes:
        title = n.get_text(" ", strip=True)
        href  = n.get("href", "") if n.name == "a" else ""
        if not title or len(title) < 5:
            continue
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = base + href
        img = n.find("img") or (n.parent.find("img") if n.parent else None)
        img_url = None
        if img and img.get("src"):
            img_url = img["src"]
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif img_url.startswith("/"):
                img_url = base + img_url
        items.append({
            "title":   title[:200],
            "url":     href or src["url"],
            "summary": "",
            "image":   img_url,
            "source":  src["name"],
            "feed_id": "",
        })
    return items


def gather_all() -> list:
    out = []
    for src in SOURCES:
        try:
            if src["type"] == "rss":
                items = fetch_rss(src)
            elif src["type"] == "html":
                items = fetch_html(src)
            else:
                items = []
            log.info(f"  → {src['name']}: {len(items)} items")
            out += items
        except Exception as e:
            log.exception(f"Source {src['name']} error: {e}")
    return out


# ---------- TRANSLATION ----------
def translate_khmer(text: str) -> str:
    if not text:
        return ""
    try:
        chunks, buf = [], ""
        for sent in re.split(r"(?<=[.!?])\s+", text):
            if len(buf) + len(sent) < 4500:
                buf += " " + sent
            else:
                chunks.append(buf.strip())
                buf = sent
        if buf:
            chunks.append(buf.strip())
        translated = [GoogleTranslator(source="auto", target="km").translate(c) for c in chunks]
        result = " ".join(t for t in translated if t).strip()
        # If we got back exactly what we sent, the translator is probably rate-limited.
        if result and result.lower() == text.lower():
            log.warning("Translation returned identical text — likely rate-limited.")
        return result or text
    except Exception as e:
        log.warning(f"Translation failed: {e}")
        return text


# ---------- TELEGRAM ----------
def tg_api(method: str) -> str:
    return f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"


def build_caption(item: dict, khmer_title: str, khmer_summary: str) -> str:
    # All text that goes inside HTML must be escaped — otherwise a stray '<'
    # or '&' from the translator/source will make Telegram reject the message.
    title_safe       = html.escape(khmer_title or item["title"])
    summary_safe     = html.escape(khmer_summary) if khmer_summary else ""
    source_safe      = html.escape(item["source"])
    url_safe         = html.escape(item["url"], quote=True)
    promo_link_safe  = html.escape(PROMO_LINK, quote=True)
    promo_name_safe  = html.escape(PROMO_NAME)

    parts = [f"🎮 <b>{title_safe}</b>", ""]
    if summary_safe:
        parts += [summary_safe[:600], ""]
    parts += [
        f"🔗 ប្រភព / Source: {source_safe}",
        f"📰 <a href=\"{url_safe}\">អានបន្ថែម / Read more</a>",
        "",
        f"💎 បញ្ចូលពេជ្រ MLBB តម្លៃថោក 👉 <a href=\"{promo_link_safe}\">{promo_name_safe}</a>",
        f"🌐 {PROMO_LINK}",
    ]
    return "\n".join(parts)


def send_telegram(item: dict, caption: str) -> bool:
    if not BOT_TOKEN or not CHANNEL_ID:
        log.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID")
        return False

    image = item.get("image")
    payload = {
        "chat_id": CHANNEL_ID,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    try:
        if image:
            payload["photo"]   = image
            payload["caption"] = caption[:1024]
            r = requests.post(tg_api("sendPhoto"), data=payload, timeout=30)
        else:
            payload["text"] = caption[:4096]
            r = requests.post(tg_api("sendMessage"), data=payload, timeout=30)

        if r.status_code == 200 and r.json().get("ok"):
            return True
        log.warning(f"Telegram error {r.status_code}: {r.text[:300]}")

        # Fallback: if photo upload failed, try the same caption as a text message.
        if image:
            payload.pop("photo", None)
            payload.pop("caption", None)
            payload["text"] = caption[:4096]
            r = requests.post(tg_api("sendMessage"), data=payload, timeout=30)
            return r.status_code == 200 and r.json().get("ok", False)
        return False
    except Exception as e:
        log.exception(f"Telegram send failed: {e}")
        return False


# ---------- CYCLE ----------
def run_cycle():
    seen_list = load_seen()
    seen_set  = set(seen_list)
    items = gather_all()
    log.info(f"Fetched {len(items)} items total from {len(SOURCES)} sources")

    if not seen_list:
        log.info("Empty seen list — seeding without posting")
        for it in items:
            uid = make_id(it)
            if uid not in seen_set:
                seen_set.add(uid)
                seen_list.append(uid)
        save_seen(seen_list)
        log.info(f"Seeded {len(seen_list)} items. Next run will post NEW updates.")
        return

    new_count = 0
    for it in items:
        uid = make_id(it)
        if uid in seen_set:
            continue

        log.info(f"NEW: [{it['source']}] {it['title'][:80]}")

        khmer_title   = translate_khmer(it["title"])
        khmer_summary = translate_khmer(it["summary"]) if it["summary"] else ""
        caption = build_caption(it, khmer_title, khmer_summary)

        if send_telegram(it, caption):
            seen_set.add(uid)
            seen_list.append(uid)
            new_count += 1
            save_seen(seen_list)
            time.sleep(3)
        else:
            log.warning("Send failed, will retry next cycle")

    log.info(f"Posted {new_count} new updates")


def main():
    log.info("=== MLBB Auto-Update Bot — Cambodia Edition 🇰🇭 ===")
    log.info(f"Mode: {'SINGLE RUN' if SINGLE_RUN else 'LOOP every %d min' % POLL_MINUTES}")
    log.info(f"Channel: {CHANNEL_ID}")
    log.info(f"Promo: {PROMO_LINK}")
    log.info(f"Watching {len(SOURCES)} sources")

    if SINGLE_RUN:
        run_cycle()
        log.info("Done.")
        return

    while True:
        try:
            run_cycle()
        except Exception as e:
            log.exception(f"Cycle error: {e}")
        log.info(f"Sleeping {POLL_MINUTES} min…")
        time.sleep(POLL_MINUTES * 60)


if __name__ == "__main__":
    main()
