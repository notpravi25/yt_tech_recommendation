"""
╔══════════════════════════════════════════════════════════╗
║          Daily Tech Video Recommender 🎬                 ║
║   Telegram-powered · Scheduled · AI/ML + Tech Topics     ║
╚══════════════════════════════════════════════════════════╝

SETUP INSTRUCTIONS (do this once before running):
──────────────────────────────────────────────────
1. Create a Telegram Bot:
   a. Open Telegram → search for @BotFather
   b. Send:  /newbot
   c. Choose a name  (e.g. "My Tech Recommender")
   d. Choose a username (e.g. "mytech_recommender_bot")
   e. BotFather gives you a TOKEN → paste it below as BOT_TOKEN

2. Get your Chat ID:
   a. Search your new bot on Telegram and send it any message
   b. Open this URL in your browser (replace YOUR_TOKEN):
      https://api.telegram.org/botYOUR_TOKEN/getUpdates
   c. Find  "chat":{"id": XXXXXXX}  → that number is your CHAT_ID

3. Paste both values in the CONFIG section below, then run!
"""

import random
import requests
import schedule
import time
from datetime import datetime
from youtube_search import YoutubeSearch


# ─────────────────────────────────────────────────────────
#  CONFIG — Fill these in before running
# ─────────────────────────────────────────────────────────
BOT_TOKEN = "8791304578:AAGqtXCCgX51cSstg1j83hi6cy5uIz9y3yI"   # e.g. "7412345678:AAFxyz..."
CHAT_ID   = "8219813869"     # e.g. "123456789"
SEND_TIME = "17:30"                     # 5:30 PM daily (24-hr format)


# ─────────────────────────────────────────────────────────
#  TOPICS — Core Tech + ML/AI + Trending (60 total)
# ─────────────────────────────────────────────────────────
TOPICS = {

    # ── How Things Work ───────────────────────────────────
    "Tech Fundamentals": [
        "how car engines work explained animation",
        "how electric vehicles work explained",
        "how jet engines work animation",
        "how nuclear reactors work animation",
        "how rockets work explained",
        "how submarines work explained",
        "how radar works explained",
        "how solar panels generate electricity explained",
        "how fiber optic internet cables work",
        "how satellites orbit earth explained",
        "how GPS navigation works explained",
        "how Wi-Fi works explained animation",
        "how a CPU processor works inside computer",
        "how lithium ion batteries work explained",
        "how electric motors work animation",
        "how planes fly aerodynamics explained",
        "how 5G networks work explained",
        "how quantum computers work explained simply",
        "how semiconductors and microchips are made",
        "how hard drives and SSDs work explained",
    ],

    # ── AI & Machine Learning ─────────────────────────────
    "AI & Machine Learning": [
        "how artificial intelligence works for beginners",
        "how neural networks work visually explained",
        "how large language models LLMs work explained",
        "how ChatGPT works under the hood explained",
        "how transformers work in AI explained",
        "how machine learning works step by step",
        "how deep learning works animation",
        "how computer vision works AI explained",
        "how reinforcement learning works explained",
        "how diffusion models AI image generation works",
        "how stable diffusion works explained",
        "what is RAG retrieval augmented generation explained",
        "how attention mechanism works in transformers",
        "how backpropagation works neural network explained",
        "what is fine tuning AI models explained",
        "how AI voice cloning works explained",
        "how AlphaGo and AlphaFold work DeepMind explained",
        "what is AGI artificial general intelligence explained",
        "how AI hallucinations happen explained",
        "how embeddings work in AI explained simply",
    ],

    # ── Trending Tech (2024-2026) ─────────────────────────
    "Trending Tech": [
        "how humanoid robots work Boston Dynamics explained",
        "how Neuralink brain chip works explained",
        "how SpaceX Starship works reusable rocket explained",
        "how Starlink satellite internet works explained",
        "how self-driving cars work AI tesla explained",
        "how solid state batteries work future EVs",
        "how nuclear fusion energy works explained 2024",
        "what is spatial computing Apple Vision Pro explained",
        "how quantum cryptography works explained",
        "how CRISPR gene editing works explained animation",
        "what is edge computing explained simply",
        "how blockchain technology works explained",
        "how augmented reality AR works explained",
        "what is digital twin technology explained",
        "how hydrogen fuel cells work explained",
        "how drone delivery systems work explained",
        "how smart grids work electricity future explained",
        "what is neuromorphic computing explained",
        "how exoskeletons work robotic suits explained",
        "how 3D printing works explained animation",
    ],
}

# Flatten all topics into one list
ALL_TOPICS = [topic for group in TOPICS.values() for topic in group]


# ─────────────────────────────────────────────────────────
#  Pick today's topic (same result all day, changes at midnight)
# ─────────────────────────────────────────────────────────
def pick_topic() -> str:
    seed = int(datetime.now().strftime("%Y%m%d"))
    random.seed(seed)
    return random.choice(ALL_TOPICS)


# ─────────────────────────────────────────────────────────
#  English language filter
#  Rejects titles that contain characters from Indian scripts
#  (Telugu, Hindi/Devanagari, Tamil, Kannada, Malayalam, etc.)
# ─────────────────────────────────────────────────────────
def is_english_title(title: str) -> bool:
    # Layer 1: reject titles containing non-Latin scripts
    non_english_ranges = [
        (0x0900, 0x097F),   # Devanagari  (Hindi, Marathi)
        (0x0C00, 0x0C7F),   # Telugu
        (0x0B80, 0x0BFF),   # Tamil
        (0x0C80, 0x0CFF),   # Kannada
        (0x0D00, 0x0D7F),   # Malayalam
        (0x0A80, 0x0AFF),   # Gujarati
        (0x0A00, 0x0A7F),   # Gurmukhi (Punjabi)
        (0x0980, 0x09FF),   # Bengali
        (0x4E00, 0x9FFF),   # Chinese
        (0x3040, 0x30FF),   # Japanese
        (0xAC00, 0xD7AF),   # Korean
        (0x0600, 0x06FF),   # Arabic
    ]
    for char in title:
        cp = ord(char)
        for start, end in non_english_ranges:
            if start <= cp <= end:
                return False

    # Layer 2: reject titles that mention non-English languages by keyword
    # (catches titles like "How AI Works in Tamil" written in English letters)
    non_english_keywords = [
        "in tamil", "in telugu", "in hindi", "in kannada",
        "in malayalam", "in marathi", "in bengali", "in urdu",
        "in gujarati", "in punjabi", "in odia", "in assamese",
        "tamil lo", "telugu lo", "hindi mein", "in chinese",
        "in japanese", "in korean", "in arabic",
    ]
    lower_title = title.lower()
    for kw in non_english_keywords:
        if kw in lower_title:
            return False

    return True


# ─────────────────────────────────────────────────────────
#  Search YouTube — returns exactly 1 English video
#  Fetches up to 8 candidates and picks the first English one
# ─────────────────────────────────────────────────────────
def search_youtube(query: str) -> dict | None:
    try:
        # Fetch extra candidates so we have room to skip non-English ones
        results = YoutubeSearch(query, max_results=8).to_dict()
    except Exception as err:
        print(f"  Search error: {err}")
        return None

    for item in results:
        title    = item.get("title", "")
        channel  = item.get("channel", "Unknown Channel")
        suffix   = item.get("url_suffix", "")
        duration = item.get("duration", "N/A")
        url      = f"https://www.youtube.com{suffix}" if suffix else "URL unavailable"

        if is_english_title(title):
            return {"title": title, "channel": channel,
                    "url": url, "duration": duration}

    return None   # no English video found in candidates


# ─────────────────────────────────────────────────────────
#  Clean topic for display (strip search-helper words)
# ─────────────────────────────────────────────────────────
def clean_topic(raw: str) -> str:
    strip_words = [
        " animation", " visually", " simply", " for beginners",
        " explained", " step by step", " under the hood",
    ]
    out = raw
    for w in strip_words:
        out = out.replace(w, "")
    return out.strip().title()


# ─────────────────────────────────────────────────────────
#  Build Telegram message (Markdown formatted)
# ─────────────────────────────────────────────────────────
def build_telegram_message(topic: str, videos: list) -> str:
    date_str = datetime.now().strftime("%A, %d %B %Y")
    topic_display = clean_topic(topic)

    lines = [
        "🎬 *Daily Tech Video Recommendation*",
        f"📅 {date_str}",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📌 *Today's Topic:*  _{topic_display}_",
        "",
    ]

    if not videos:
        lines.append("❌ No English video found today. Check your internet and try again.")
    else:
        v = videos
        lines.append(f"▶️ *{v['title']}*")
        lines.append(f"👤 {v['channel']}   ⏱ {v['duration']}")
        lines.append(f"🔗 {v['url']}")
        lines.append("")

    lines += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 _One video a day keeps ignorance away\\! 🚀_",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
#  Send Telegram notification
# ─────────────────────────────────────────────────────────
def send_telegram(message: str) -> bool:
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("  ⚠️  Telegram not configured. Fill in BOT_TOKEN and CHAT_ID above.")
        return False

    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}

    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("  ✅  Telegram message sent!")
            return True
        else:
            print(f"  ❌  Telegram error {r.status_code}: {r.text}")
            return False
    except Exception as err:
        print(f"  ❌  Failed to send Telegram message: {err}")
        return False


# ─────────────────────────────────────────────────────────
#  Print results to terminal
# ─────────────────────────────────────────────────────────
def print_results(topic: str, videos: list) -> None:
    now = datetime.now().strftime("%A, %d %B %Y  %H:%M")
    topic_display = clean_topic(topic)

    print()
    print("=" * 62)
    print("  🎬  Daily Tech Video Recommender")
    print(f"  📅  {now}")
    print("=" * 62)
    print(f"\n  📌  Topic: {topic_display}\n")

    if not videos:
        print("  ❌  No English video found. Check your internet connection.")
    else:
        v = videos
        print(f"  ▶  {v['title']}")
        print(f"     👤  {v['channel']}   ⏱ {v['duration']}")
        print(f"     🔗  {v['url']}")
        print()

    print("=" * 62)
    print()


# ─────────────────────────────────────────────────────────
#  Daily job — called by scheduler every day at SEND_TIME
# ─────────────────────────────────────────────────────────
def daily_job():
    print(f"\n  ⏳  Running at {datetime.now().strftime('%H:%M:%S')}...")
    topic   = pick_topic()
    video   = search_youtube(topic)
    message = build_telegram_message(topic, video)
    print_results(topic, video)
    send_telegram(message)


# ─────────────────────────────────────────────────────────
#  Start the scheduler
# ─────────────────────────────────────────────────────────
def start_scheduler():
    schedule.every().day.at(SEND_TIME).do(daily_job)

    print()
    print("=" * 62)
    print("  ⏰  Scheduler is running!")
    print(f"  📬  Telegram message will be sent daily at {SEND_TIME}.")
    print(f"  📚  {len(ALL_TOPICS)} topics loaded across {len(TOPICS)} categories.")
    print("  🛑  Press Ctrl+C to stop.")
    print("=" * 62)

    # Send once immediately on startup as a test
    print("\n  🔄  Sending today's recommendation right now as a preview...\n")
    daily_job()

    while True:
        schedule.run_pending()
        time.sleep(30)


# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    start_scheduler()