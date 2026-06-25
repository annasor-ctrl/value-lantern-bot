import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION & BILINGUAL MULTI-STEP CONTENT ---
CONTENT = {
    "en": {
        "title": "🏮 The Value Lantern Workshop",
        "subtitle": "A reflective journey based on the Brené Brown methodology.",
        "nav_ex1": "🔥 1. The Flame",
        "nav_ex2": "🛡️ 2. The Glass",
        "nav_ex3": "🎒 3. The Handle",
        "nav_ex4": "🚀 4. The Radiance (AI)",
        
        "ex1_title": "🔥 Part 1: The Flame (Core Values)",
        "ex1_desc": "What are the 1–2 values that really light the way for you in the dark? These are your non-negotiables.",
        "ex1_options": ["Authenticity", "Courage", "Creativity", "Autonomy", "Family", "Growth", "Stability", "Kindness", "Compassion", "Justice"],
        "ex1_label": "Select your 1-2 core values:",
        
        "ex2_title": "🛡️ Part 2: Protecting the Flame (The Glass)",
        "ex2_desc": "All lanterns have glass to protect the flame. What behaviors, boundaries, or supportive people help protect your values from being blown out by stress?",
        "ex2_placeholder": "e.g., Saying 'no' to weekend work, talking to my mentor, keeping 8 hours of sleep...",
        "ex2_label": "What protects your values?",
        
        "ex3_title": "🎒 Part 3: Setting Down the Lantern (The Handle)",
        "ex3_desc": "When overwhelmed, we often set down our lantern and walk away from our values. Use the handle to identify your 'red flag' behaviors that show you are in trouble.",
        "ex3_placeholder": "e.g., Numbing out on social media, judging others harshly, isolation, skipping the gym...",
        "ex3_label": "What are your warning signs/red flags?",
        
        "ex4_title": "🚀 Part 4: Radiating Light (Your Practical Guide)",
        "ex4_desc": "Ready to bring it all together? Let's analyze your lantern map and create an actionable roadmap for your day-to-day life and work.",
        "btn_analyze": "✨ Generate AI Guidance",
        "loading": "Illuminating your path...",
        
        "system_prompt": """You are an empathetic, insightful life coach specializing in the 'Value Lantern' framework. 
Analyze the user's input based on: The Flame (Values), The Glass (Protection), and The Handle (Red Flags).
Provide guidance entirely in English.
Structure into 3 clear sections using emojis:
🏮 **Your Inner Light**: A deep, empowering reflection on their values.
⚠️ **Navigating the Shadows**: How to spot when they are 'setting down the handle' (red flags) and how to return to the light using their glass (protection).
💼 **Day-to-Day Radiance**: Provide 3 highly practical, specific actions they can apply to their Career/Daily life starting this week."""
    },
    "ja": {
        "title": "🏮 価値観のランタン・ワークショップ",
        "subtitle": "ブレネー・ブラウンのメソッドに基づく、自分を知るリフレクション旅。",
        "nav_ex1": "🔥 1. 炎 (価値観)",
        "nav_ex2": "🛡️ 2. ガラス (保護)",
        "nav_ex3": "🎒 3. 持ち手 (危険信号)",
        "nav_ex4": "🚀 4. 輝き (AI分析)",
        
        "ex1_title": "🔥 パート 1: 炎（核心的な価値観）",
        "ex1_desc": "暗闇の中であなたの道を本当に照らしてくれる、1〜2つの中心的な価値観は何ですか？これは妥協できないものです。",
        "ex1_options": ["自分らしさ", "勇気", "創造性", "自律性・自由", "家族", "成長", "安定・安心", "思いやり", "共感", "公正・正義"],
        "ex1_label": "1〜2つの核心的な価値観を選んでください：",
        
        "ex2_title": "🛡️ パート 2: 炎を守る（ガラスの盾）",
        "ex2_desc": "すべてのランタンには火を守るガラスがあります。ストレスの「風」で火が消えないように、あなたの価値観を守ってくれる行動、境界線、または支えてくれる人は誰ですか？",
        "ex2_placeholder": "例：週末の仕事を断る、メンターに相談する、8時間睡眠を死守する...",
        "ex2_label": "あなたの価値観を守るものは何ですか？",
        
        "ex3_title": "🎒 パート 3: ランタンを置く（持ち手・レッドフラッグ）",
        "ex3_desc": "限界を迎えた時、私たちはランタンを地面に置き、自分の価値観から遠ざかってしまうことがあります。あなたが「今、調子を崩している」と気づくための危険信号（行動パターン）を教えてください。",
        "ex3_placeholder": "例：SNSをダラダラ見続ける、他人に批判的になる、引きこもる、運動をやめる...",
        "ex3_label": "あなたの危険信号（レッドフラッグ）は何ですか？",
        
        "ex4_title": "🚀 パート 4: 光を放つ（日常への応用）",
        "ex4_desc": "すべての準備が整いました！あなたのランタンのマップを分析し、仕事や日常生活に活かすための具体的なロードマップを作成しましょう。",
        "btn_analyze": "✨ AIアドバイスを生成する",
        "loading": "道を照らしています...",
        
        "system_prompt": """You are an empathetic, insightful life coach specializing in the 'Value Lantern' framework. 
Analyze the user's input based on: The Flame (Values), The Glass (Protection), and The Handle (Red Flags).
Provide guidance entirely in Japanese.
Structure into 3 clear sections using emojis:
🏮 **あなたの内なる光**: ユーザーの価値観に対する深く、エンパワーメントを与える考察。
⚠️ **影のロードマップ**: 「持ち手を置いてしまっている（危険信号）」にどうやって気づき、どうやって「ガラス（保護）」を使って光に戻るかの実践的アドバイス。
💼 **日常を照らすアクション**: 仕事や私生活で今週から実践できる、具体的で少し遊び心のある3つのステップ。"""
    }
}

# --- 2. APP SETUP ---
st.set_page_config(page_title="Value Lantern", page_icon="🏮", layout="centered")

# Language toggle
lang_choice = st.radio("Language / 言語", ["English", "日本語"], horizontal=True, label_visibility="collapsed")
lang = "en" if lang_choice == "English" else "ja"
t = CONTENT[lang]

st.title(t["title"])
st.caption(t["subtitle"])
st.markdown("---")

# --- 3. EXERCISE TABS (Simulating Multiple Exercises) ---
tab1, tab2, tab3, tab4 = st.tabs([t["nav_ex1"], t["nav_ex2"], t["nav_ex3"], t["nav_ex4"]])

# Tab 1: The Flame
with tab1:
    st.subheader(t["ex1_title"])
    st.write(t["ex1_desc"])
    selected_values = st.multiselect(t["ex1_label"], t["ex1_options"], max_selections=2)
    st.caption("💡 Tip: Click the next tab above when done! / 完了したら上の次のタブをクリックしてください！")

# Tab 2: The Glass
with tab2:
    st.subheader(t["ex2_title"])
    st.write(t["ex2_desc"])
    glass_text = st.text_area(t["ex2_label"], placeholder=t["ex2_placeholder"], height=100)

# Tab 3: The Handle
with tab3:
    st.subheader(t["ex3_title"])
    st.write(t["ex3_desc"])
    handle_text = st.text_area(t["ex3_label"], placeholder=t["ex3_placeholder"], height=100)

# Tab 4: AI Analysis
with tab4:
    st.subheader(t["ex4_title"])
    st.write(t["ex4_desc"])
    
    if st.button(t["btn_analyze"], type="primary"):
        if not selected_values or not glass_text or
