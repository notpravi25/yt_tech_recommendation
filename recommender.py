"""
╔══════════════════════════════════════════════════════════╗
║        Daily Tech Video Recommender 🎬  v2.0            ║
║   No repeats · Tracks history · Telegram · GitHub Actions║
╚══════════════════════════════════════════════════════════╝
"""

import os
import json
import random
import requests
from datetime import datetime
from youtube_search import YoutubeSearch


# ─────────────────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────────────────
BOT_TOKEN        = os.environ.get("BOT_TOKEN", "")
CHAT_ID          = os.environ.get("CHAT_ID", "")
HISTORY_FILE     = "sent_videos.json"   # tracked inside the repo
MAX_CANDIDATES   = 10                   # how many YT results to scan per topic


# ─────────────────────────────────────────────────────────
#  TOPICS
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

ALL_TOPICS = [t for group in TOPICS.values() for t in group]


# ─────────────────────────────────────────────────────────
#  HISTORY — load / save sent_videos.json
# ─────────────────────────────────────────────────────────
def load_history() -> dict:
    """
    Returns the history dict:
    {
      "sent_urls":  ["https://...", ...],      ← all URLs ever sent
      "log": [
        {"date": "2026-04-13", "topic": "...", "title": "...", "url": "..."},
        ...
      ]
    }
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"sent_urls": [], "log": []}


def save_history(history: dict, video: dict, topic: str) -> None:
    """Append today's video to history and save."""
    today = datetime.now().strftime("%Y-%m-%d")
    history["sent_urls"].append(video["url"])
    history["log"].append({
        "date":    today,
        "topic":   clean_topic(topic),
        "title":   video["title"],
        "channel": video["channel"],
        "url":     video["url"],
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"  💾  History updated — {len(history['sent_urls'])} videos tracked so far.")


# ─────────────────────────────────────────────────────────
#  TOPIC SELECTION — avoid recently used topics too
# ─────────────────────────────────────────────────────────
def pick_topic(history: dict) -> str:
    """
    Pick a random topic, preferring ones not used in the last 30 days.
    Falls back to any topic if everything was recently used.
    """
    recent_topics = {
        entry["topic"].lower()
        for entry in history.get("log", [])[-30:]   # last 30 entries
    }

    fresh = [t for t in ALL_TOPICS
             if clean_topic(t).lower() not in recent_topics]

    pool = fresh if fresh else ALL_TOPICS
    seed = int(datetime.now().strftime("%Y%m%d"))
    random.seed(seed)
    return random.choice(pool)


# ─────────────────────────────────────────────────────────
#  ENGLISH FILTER
# ─────────────────────────────────────────────────────────
def is_english(title: str) -> bool:
    non_english_ranges = [
        (0x0900, 0x097F), (0x0C00, 0x0C7F), (0x0B80, 0x0BFF),
        (0x0C80, 0x0CFF), (0x0D00, 0x0D7F), (0x0A80, 0x0AFF),
        (0x0A00, 0x0A7F), (0x0980, 0x09FF), (0x4E00, 0x9FFF),
        (0x3040, 0x30FF), (0xAC00, 0xD7AF), (0x0600, 0x06FF),
    ]
    for char in title:
        cp = ord(char)
        for s, e in non_english_ranges:
            if s <= cp <= e:
                return False

    blocked = [
        "in tamil", "in telugu", "in hindi", "in kannada",
        "in malayalam", "in marathi", "in bengali", "in urdu",
        "tamil lo", "telugu lo", "hindi mein",
        "in chinese", "in japanese", "in korean", "in arabic",
    ]
    lower = title.lower()
    return not any(kw in lower for kw in blocked)


# ─────────────────────────────────────────────────────────
#  YOUTUBE SEARCH — skip already-sent videos
# ─────────────────────────────────────────────────────────
def search_youtube(query: str, sent_urls: list) -> dict | None:
    """
    Fetches up to MAX_CANDIDATES results.
    Skips non-English titles AND urls already in history.
    Returns the first fresh English video found.
    """
    try:
        results = YoutubeSearch(query, max_results=MAX_CANDIDATES).to_dict()
    except Exception as err:
        print(f"  Search error: {err}")
        return None

    for item in results:
        title    = item.get("title", "")
        channel  = item.get("channel", "Unknown Channel")
        suffix   = item.get("url_suffix", "")
        duration = item.get("duration", "N/A")
        url      = f"https://www.youtube.com{suffix}" if suffix else ""

        if not url:
            continue
        if not is_english(title):
            print(f"  ⏭️   Skipped (non-English): {title[:50]}")
            continue
        if url in sent_urls:
            print(f"  ⏭️   Skipped (already sent): {title[:50]}")
            continue

        # Fresh English video found ✅
        return {"title": title, "channel": channel,
                "url": url, "duration": duration}

    return None   # nothing new found


# ─────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────
def clean_topic(raw: str) -> str:
    for w in [" animation", " visually", " simply", " for beginners",
              " explained", " step by step", " under the hood"]:
        raw = raw.replace(w, "")
    return raw.strip().title()


# ─────────────────────────────────────────────────────────
#  TELEGRAM
# ─────────────────────────────────────────────────────────
def build_message(topic: str, video: dict, total_sent: int) -> str:
    date_str = datetime.now().strftime("%A, %d %B %Y")
    lines = [
        "🎬 *Daily Tech Video Recommendation*",
        f"📅 {date_str}",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📌 *Topic:*  _{clean_topic(topic)}_",
        "",
        f"▶️ *{video['title']}*",
        f"👤 {video['channel']}   ⏱ {video['duration']}",
        f"🔗 {video['url']}",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📊 _Video #{total_sent} in your learning journey\\!_",
        "💡 _One video a day keeps ignorance away\\! 🚀_",
    ]
    return "\n".join(lines)


def send_telegram(message: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        print("  ⚠️  BOT_TOKEN or CHAT_ID not set.")
        return False
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("  ✅  Telegram notification sent!")
            return True
        print(f"  ❌  Telegram error {r.status_code}: {r.text}")
        return False
    except Exception as err:
        print(f"  ❌  {err}")
        return False


# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────
def main():
    print(f"\n  ⏳  Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")

    # 1. Load history
    history   = load_history()
    sent_urls = history.get("sent_urls", [])
    print(f"  📖  History loaded — {len(sent_urls)} videos sent so far.")

    # 2. Pick a fresh topic
    topic = pick_topic(history)
    print(f"  📌  Topic: {clean_topic(topic)}")

    # 3. Search for a video not sent before
    video = search_youtube(topic, sent_urls)

    if not video:
        # Fallback: try a few random other topics
        print("  🔄  No fresh video on this topic, trying another topic...")
        for _ in range(5):
            fallback_topic = random.choice(ALL_TOPICS)
            video = search_youtube(fallback_topic, sent_urls)
            if video:
                topic = fallback_topic
                break

    if not video:
        print("  ❌  Could not find a fresh English video. Skipping today.")
        return

    print(f"  📺  Found : {video['title']}")
    print(f"  👤  Channel: {video['channel']}")
    print(f"  ⏱   Duration: {video['duration']}")
    print(f"  🔗  URL    : {video['url']}")

    # 4. Send Telegram message
    total_sent = len(sent_urls) + 1
    message    = build_message(topic, video, total_sent)
    send_telegram(message)

    # 5. Save to history (so it's never sent again)
    save_history(history, video, topic)


if __name__ == "__main__":
    main()
