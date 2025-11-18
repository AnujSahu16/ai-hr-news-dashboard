# 🚀 AI-Powered HR Intelligence Dashboard

**Transforming daily HR news into strategic interview insights using Generative AI.**

### 🎯 The Problem
HR professionals and MBA students need to stay updated with daily news (ETHRWorld, People Matters), but simply reading headlines isn't enough. To ace interviews and drive strategy, one must understand the **"So What?"**—the business impact, risk, and strategic link behind every story.

### 💡 The Solution
I built this **HR Intelligence Dashboard**, an interactive Python application that acts as a 24/7 Senior HR Mentor. It fetches live news and uses **Google Gemini Pro** to deconstruct every story into a strategic briefing.

---

### ✨ Key Features

* **📰 Real-Time Intelligence:** Automatically aggregates the top 20 daily HR headlines from trusted sources like *ETHRWorld*, *People Matters*, and *Mint*.
* **🧠 Deep AI Analysis:** One-click analysis powered by **Google Gemini** that breaks down news into:
    * **HR Concept Mapping:** Links news to core pillars (e.g., Compliance, Talent Acquisition).
    * **Business Impact:** Explains the ROI, Risk, or Brand impact.
    * **"Then vs. Now" Analysis:** A comparative look at how trends have shifted.
* **💬 Interactive Brainstorming:** A built-in chat interface to ask follow-up questions (e.g., *"How would I defend this policy in a debate?"*).
* **🔍 Strategic Search:** Integrated web search to deep-dive into specific topics like "Moonlighting" or "Labour Codes."

---

### 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **AI Engine:** Google Gemini API (`gemini-2.5-pro`)
* **Data Fetching:** `feedparser` (RSS) & `duckduckgo-search` (Web Search)
* **Data Processing:** Pandas

---

### 🚀 How to Run This Tool Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/AnujSahu16/ai-hr-news-dashboard.git](https://github.com/AnujSahu16/ai-hr-news-dashboard.git)
    cd ai-hr-news-dashboard
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Your API Key**
    * Get a free API key from [Google AI Studio](https://aistudio.google.com/).
    * Open `hr_dashboard.py` and paste your key in the `API_KEY` variable.

4.  **Launch the App**
    ```bash
    streamlit run hr_dashboard.py
    ```

---

### 👨‍💻 About Me
Built by **Anuj Sahu** as a strategic initiative to leverage AI for HR Analytics and Learning. Connect with me on LinkedIn!
