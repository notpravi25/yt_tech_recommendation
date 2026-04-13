# yt_tech_recommendation
# 🎬 Daily Tech Video Recommender

> **One high-quality English YouTube video, delivered to your Telegram every day at 5:30 PM IST — automatically, even when your laptop is off.**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-2088FF?style=flat&logo=githubactions)
![Telegram](https://img.shields.io/badge/Notify-Telegram-26A5E4?style=flat&logo=telegram)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📱 What You Get Every Day

```
🎬 Daily Tech Video Recommendation
📅 Monday, 13 April 2026
━━━━━━━━━━━━━━━━━━━━━━━━
📌 Today's Topic: How Large Language Models Work

▶️ Large Language Models explained simply
👤 Kurzgesagt   ⏱ 12:34
🔗 https://www.youtube.com/watch?v=...

━━━━━━━━━━━━━━━━━━━━━━━━
💡 One video a day keeps ignorance away! 🚀
```

---

## ✨ Features

- 🤖 **60 curated topics** across AI, ML, and trending tech
- 🔤 **English-only filter** — rejects Hindi, Telugu, Tamil and other language videos automatically
- 📅 **One video per day** — focused, not overwhelming
- ⚡ **Zero intervention** — runs on GitHub's servers, laptop can be OFF
- 🔐 **Secure** — Telegram credentials stored as GitHub Secrets, never in code
- 🛠️ **Easy to extend** — just add topics to a list

---

## 📚 Topic Categories

<details>
<summary>⚙️ Tech Fundamentals (20 topics)</summary>

- How car engines work
- How electric vehicles work
- How nuclear reactors work
- How rockets work
- How satellites orbit earth
- How GPS navigation works
- How Wi-Fi works
- How a CPU processor works
- How quantum computers work
- How semiconductors are made
- ...and more

</details>

<details>
<summary>🤖 AI & Machine Learning (20 topics)</summary>

- How neural networks work
- How large language models (LLMs) work
- How ChatGPT works
- How transformers work
- How deep learning works
- How reinforcement learning works
- How diffusion models work
- What is RAG (Retrieval Augmented Generation)
- How embeddings work
- What is AGI
- ...and more

</details>

<details>
<summary>🔥 Trending Tech (20 topics)</summary>

- How humanoid robots work
- How Neuralink works
- How SpaceX Starship works
- How Starlink satellite internet works
- How self-driving cars work
- How nuclear fusion works
- How CRISPR gene editing works
- What is spatial computing
- How quantum cryptography works
- How hydrogen fuel cells work
- ...and more

</details>

---

## 🏗️ Project Structure

```
daily-tech-recommender/
├── recommender.py                   ← main Python script
├── requirements.txt                 ← dependencies
├── README.md                        ← you are here
└── .github/
    └── workflows/
        └── daily_recommender.yml    ← GitHub Actions schedule
```

---

## ⚙️ How It Works

```
GitHub Actions Scheduler (5:30 PM IST daily)
        ↓
Picks a random topic from 60 curated topics
        ↓
Searches YouTube for that topic
        ↓
Filters results — English only
        ↓
Sends 1 video recommendation to Telegram
        ↓
Done ✅ (until tomorrow)
```

---

## 🚀 Setup Guide

### 1. Create a Telegram Bot
1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **bot token** you receive

### 2. Get Your Chat ID
1. Send any message to your new bot
2. Visit: `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
3. Find `"chat":{"id": XXXXXXX}` — copy that number

### 3. Add GitHub Secrets
Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret Name | Value |
|---|---|
| `BOT_TOKEN` | Your Telegram bot token |
| `CHAT_ID` | Your Telegram chat ID |

### 4. Test It
Go to **Actions** tab → **Daily Tech Video Recommender** → **Run workflow**

Check your Telegram — the recommendation arrives within seconds! 🎉

---

## 🕐 Schedule

The workflow runs daily at **12:00 UTC = 5:30 PM IST**.

To change the time, edit this line in `.github/workflows/daily_recommender.yml`:
```yaml
- cron: "0 12 * * *"
```

| Want it at | Change cron to |
|---|---|
| 7:00 AM IST | `30 1 * * *` |
| 12:00 PM IST | `30 6 * * *` |
| 5:30 PM IST | `0 12 * * *` |
| 9:00 PM IST | `30 15 * * *` |

---

## ➕ Adding More Topics

Open `recommender.py` and add any string to the relevant list:

```python
"AI & Machine Learning": [
    ...
    "how graph neural networks work explained",  # ← add like this
],
```

---

## ⚠️ Important Note

GitHub pauses scheduled workflows after **60 days of repo inactivity**.
To prevent this, visit your repo once every 2 months and click **Run workflow** once manually.

---

## 🛠️ Built With

- [Python 3.11](https://python.org)
- [youtube-search](https://pypi.org/project/youtube-search/)
- [GitHub Actions](https://github.com/features/actions)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

*Built to make daily tech learning effortless.* 🚀
