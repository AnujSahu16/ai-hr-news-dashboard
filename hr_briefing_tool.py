import streamlit as st
import feedparser
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime
import html

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="HR Learning Co-Pilot",
    layout="wide",
    page_icon="🚀"
)

# API Key provided by user
API_KEY = "PASTE_YOUR_GOOGLE_API_KEY_HERE"

# Configure Gemini AI
try:
    genai.configure(api_key=API_KEY)
    # Using the model name we discovered from your test_gemini.py
    model = genai.GenerativeModel('models/gemini-2.5-pro')
except Exception as e:
    st.error(f"API Key Error: {e}. Please ensure the key is correct.")
    st.stop()

# RSS Feeds (Req 2)
RSS_FEEDS = {
    "ETHRWorld": "https://hr.economictimes.indiatimes.com/rss/topstories",
    "People Matters": "https://www.peoplematters.in/rss/feed",
    "Mint (HR)": "https://www.livemint.com/rss/industry/human-resources",
    "HRKatha": "https://www.hrkatha.com/feed/"
}

# --- 2. BACKEND FUNCTIONS ---

@st.cache_data(ttl=3600)  # Cache news for 1 hour
def fetch_top_20_news():
    """Fetches news from all RSS feeds and returns top 20."""
    all_entries = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if 'published_parsed' in entry and entry.published_parsed:
                    dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                else:
                    dt = datetime.now()
                all_entries.append({
                    "title": html.unescape(entry.title),
                    "link": entry.link,
                    "published_dt": dt,
                    "source": source,
                    "snippet": html.unescape(entry.get('summary', 'No snippet available.'))
                })
        except Exception as e:
            print(f"Error fetching {source}: {e}") # Log for debugging

    df = pd.DataFrame(all_entries)
    if not df.empty:
        df = df.drop_duplicates(subset=['title'])
        df = df.sort_values(by='published_dt', ascending=False)
    return df.head(20) # Req 6: Top 20 news

# --- NEW AI BRAIN ---
@st.cache_data # Cache the AI analysis
def get_strategic_analysis(headline, snippet):
    """
    (Req 1 & 5) New AI prompt to generate the "complete knowledge" card.
    """
    
    # This prompt is the new "intelligence" you requested.
    prompt = f"""
    You are my specialist HR Co-Pilot. I am an MBA HR student.
    Analyze this news story for my placement interviews.

    **Headline:** "{headline}"
    **Snippet:** "{snippet}"

    Generate a 5-part "Strategic Briefing Card" in this exact format.
    Your analysis must be deep, professional, and easy to understand.

    ### 1. Simple Summary (The "What")
    (Explain this news in 2 simple sentences, like you're talking to a colleague.)

    ### 2. HR Pillar & Concept (The "Where")
    (Where does this fit in an HR textbook? e.g., 'Talent Management > Performance Systems', or 'Compliance > Industrial Relations'.)

    ### 3. The "Then vs. Now" (The "Change")
    (This is the most important. Create a 2-column comparison table in Markdown showing what this topic was like in the past ("Then") vs. what this news means for today ("Now"). For example, if the news is about AI in hiring:
    | Then (Past) | Now (Current Trend) |
    |---|---|
    | Manual resume screening | AI-powered candidate sourcing |
    | Gut-feel interviews | Data-driven competency mapping |
    )

    ### 4. Strategic Importance (The "So What?")
    (Why should a CHRO care? Link this to a core business metric: **Cost**, **Risk**, or **Revenue/Brand**.)

    ### 5. Your Interview Script (The "How")
    (Give me a polished, confident script to say in an interview. Start with "I'm tracking this development..." and use the "Then vs. Now" insight.)
    """
    try:
        response = model.generate_content(prompt)
        if not response.parts:
            return "**Error from AI:** The AI returned an empty response (Content Safety Filter)."
        return response.text
    except Exception as e:
        return f"**Error from AI:** {str(e)}."

# --- 3. FRONTEND (The App UI) ---

st.title("🚀 HR Learning Co-Pilot")
st.caption(f"Your AI-powered dashboard for interview-ready HR intelligence.")

# --- Create the Tabs ---
tab1, tab2 = st.tabs(["📰 Daily Briefing", "🤖 AI Brainstorm Chat"])

# --- Tab 1: Daily Briefing (Your RSS Feed) ---
with tab1:
    col1, col2 = st.columns([1, 2]) # 1/3 for news list, 2/3 for analysis
    
    with col1:
        st.subheader("Top 20 Headlines")
        st.markdown("*(Updated daily)*")
        
        try:
            news_df = fetch_top_20_news()
            
            # Create a clean list of titles for the radio selector
            # (Req 6: News with dates)
            news_titles = [
                f"**{row['published_dt'].strftime('%b %d')}** | {row['title']} *({row['source']})*"
                for index, row in news_df.iterrows()
            ]
            
            if not news_titles:
                st.warning("No news found from feeds. Check RSS_FEEDS URLs.")
                st.stop()
            
            # The interactive news selector
            selected_title_str = st.radio(
                "Select a headline to analyze:",
                news_titles,
                label_visibility="collapsed"
            )
            
            # Find the full article data based on the selected title string
            selected_index = news_titles.index(selected_title_str)
            article = news_df.iloc[selected_index]

        except Exception as e:
            st.error(f"Could not load news feeds: {e}")
            st.stop()

    with col2:
        st.subheader("AI Strategic Analysis")
        
        # Display the AI analysis for the selected article
        with st.spinner(f"🤖 Calling HR Co-Pilot for: *{article['title']}*..."):
            
            # Run the NEW AI analysis function (Req 1)
            analysis = get_strategic_analysis(article['title'], article['snippet'])
            
            st.markdown(analysis) # Display the 5-point card
            st.divider()
            
            # (Req 4: Link of source)
            st.link_button("🔗 Read Full Source Article", article['link'])
            
            # --- NEW "BRAINSTORM" FEATURE ---
            if st.button("🧠 Brainstorm this Topic (in Tab 2)", type="primary"):
                # Load this analysis into the chat's memory
                st.session_state.chat_context = {
                    "title": article['title'],
                    "analysis": analysis 
                }
                st.success("Context loaded! Go to the 'AI Brainstorm Chat' tab to ask follow-up questions.")

# --- Tab 2: AI Brainstorm Chat ---
with tab2:
    st.subheader("🤖 Your AI Brainstorming Partner")

    # (Req 3: Key pointers at bottom)
    with st.expander("🔑 Key Pointers to Remember (For ALL Interviews)"):
        st.markdown("""
        * **Commercial Awareness:** Always link HR to business. How does this news *save money*, *make money*, or *reduce risk*?
        * **The STAR Method:** For behavioral questions, use **S**ituation, **T**ask, **A**ction, **R**esult.
        * **Data-Driven:** Mention metrics where possible (e.g., "This could reduce attrition by 10%").
        * **The "Why":** Don't just state the news, state the *implication* of the news.
        """)

    st.divider()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Check for a loaded topic
    if "chat_context" in st.session_state and st.session_state.chat_context:
        context = st.session_state.chat_context
        st.info(f"**Topic Loaded:** You are now discussing *'{context['title']}'*. Ask me anything about it.")
        
        # Clear chat history if context changes
        if "last_context" not in st.session_state or st.session_state.last_context != context['title']:
            st.session_state.messages = []
            st.session_state.last_context = context['title']
    else:
        st.info("Ask general HR questions, or select a topic from the 'Daily Briefing' tab to start a deep-dive chat.")

    # Display past chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    if prompt := st.chat_input("Ask a follow-up (e.g., 'Explain the 'Then vs. Now' in more detail')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                # Build the AI's "memory"
                system_prompt = "You are an expert HR Interview Coach."
                
                # Add the specific news context if it exists
                if "chat_context" in st.session_state and st.session_state.chat_context:
                    context = st.session_state.chat_context
                    system_prompt += f"\n\nThe user wants to brainstorm this specific topic: {context['title']}.\nHere is the initial analysis you already provided:\n{context['analysis']}\n\nNow, answer their follow-up question."

                full_prompt = system_prompt + "\n\nChat History:\n"
                for msg in st.session_state.messages[:-1]:
                    full_prompt += f"{msg['role']}: {msg['content']}\n"
                full_prompt += f"user: {prompt}"

                try:
                    response = model.generate_content(full_prompt)
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"**Error from AI:** {str(e)}"
                
                st.markdown(ai_response)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})