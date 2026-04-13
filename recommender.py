"""
╔══════════════════════════════════════════════════════════╗
║          Daily Tech Video Recommender 🎬                 ║
║   Telegram-powered · GitHub Actions · AI/ML + Tech       ║
╚══════════════════════════════════════════════════════════╝

BOT_TOKEN and CHAT_ID are injected automatically by GitHub
Actions via repository secrets — never hardcoded here.
"""

import os
import random
import requests
from datetime import datetime
from youtube_search import YoutubeSearch


# ─────────────────────────────────────────────────────────
#  CONFIG — read from GitHub Actions Secrets (env vars)
# ─────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID   = os.environ.get("CHAT_ID", "")


# ─────────────────────────────────────────────────────────
#  TOPICS — Core Tech + ML/AI + Trending (60 total)
# ─────────────────────────────────────────────────────────
TOPICS = {

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

ALL_TOPICS = [topic for group in TOPICS.values() for topic in group]


# ─────────────────────────────────────────────────────────
#  Pick today's topic (changes daily at midnight)
# ─────────────────────────────────────────────────────────
def pick_topic() -> str:
    seed = int(datetime.now().strftime("%Y%m%d"))
    random.seed(seed)
    return random.choice(ALL_TOPICS)


# ─────────────────────────────────────────────────────────
#  English filter — 2 layers
# ─────────────────────────────────────────────────────────
def is_english_title(title: str) -> bool:
    non_english_ranges = [
        (0x0900, 0x097F), (0x0C00, 0x0C7F), (0x0B80, 0x0BFF),
        (0x0C80, 0x0CFF), (0x0D00, 0x0D7F), (0x0A80, 0x0AFF),
        (0x0A00, 0x0A7F), (0x0980, 0x09FF), (0x4E00, 0x9FFF),
        (0x3040, 0x30FF), (0xAC00, 0xD7AF), (0x0600, 0x06FF),
    ]
    for char in title:
        cp = ord(char)
        for start, end in non_english_ranges:
            if start <= cp <= end:
                return False

    non_english_keywords = [
        "in tamil", "in telugu", "in hindi", "in kannada",
        "in malayalam", "in marathi", "in bengali", "in urdu",
        "tamil lo", "telugu lo", "hindi mein", "in chinese",
        "in japanese", "in korean", "in arabic",
    ]
    lower = title.lower()
    return not any(kw in lower for kw in non_english_keywords)


# ─────────────────────────────────────────────────────────
#  Search YouTube — returns exactly 1 English video
# ─────────────────────────────────────────────────────────
def search_youtube(query: str) -> dict | None:
    try:
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
    return None


# ─────────────────────────────────────────────────────────
#  Clean topic for display
# ─────────────────────────────────────────────────────────
def clean_topic(raw: str) -> str:
    for w in [" animation", " visually", " simply", " for beginners",
              " explained", " step by step", " under the hood"]:
        raw = raw.replace(w, "")
    return raw.strip().title()


# ─────────────────────────────────────────────────────────
#  Build Telegram message
# ─────────────────────────────────────────────────────────
def build_telegram_message(topic: str, video: dict | None) -> str:
    date_str = datetime.now().strftime("%A, %d %B %Y")
    lines = [
        "🎬 *Daily Tech Video Recommendation*",
        f"📅 {date_str}",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📌 *Today's Topic:*  _{clean_topic(topic)}_",
        "",
    ]
    if not video:
        lines.append("❌ No English video found today\\. Try again tomorrow\\!")
    else:
        lines += [
            f"▶️ *{video['title']}*",
            f"👤 {video['channel']}   ⏱ {video['duration']}",
            f"🔗 {video['url']}",
            "",
        ]
    lines += ["━━━━━━━━━━━━━━━━━━━━━━━━",
              "💡 _One video a day keeps ignorance away\\! 🚀_"]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
#  Send Telegram notification
# ─────────────────────────────────────────────────────────
def send_telegram(message: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        print("  ⚠️  BOT_TOKEN or CHAT_ID not set in environment.")
        return
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("  ✅  Telegram notification sent!")
        else:
            print(f"  ❌  Telegram error {r.status_code}: {r.text}")
    except Exception as err:
        print(f"  ❌  Failed: {err}")


# ─────────────────────────────────────────────────────────
#  Main — called directly by GitHub Actions
# ─────────────────────────────────────────────────────────
def main():
    print(f"\n  ⏳  Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    topic   = pick_topic()
    video   = search_youtube(topic)
    message = build_telegram_message(topic, video)

    print(f"  📌  Topic  : {clean_topic(topic)}")
    if video:
        print(f"  📺  Title  : {video['title']}")
        print(f"  👤  Channel: {video['channel']}")
        print(f"  ⏱   Duration: {video['duration']}")
        print(f"  🔗  URL    : {video['url']}")
    else:
        print("  ❌  No English video found.")

    send_telegram(message)


if __name__ == "__main__":
    main()