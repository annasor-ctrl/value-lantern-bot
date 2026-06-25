import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION & BILINGUAL CONTENT DATABASE ---
CONTENT = {
    "en": {
        "title": "🏮 The Value Lantern Workshop",
        "subtitle": "Discover your core values, protect your light, and illuminate your life.",
        "step1_header": "🔥 Step 1: The Fuel (Your Core Values)",
        "step1_desc": "Select up to 3 core values that make your lantern burn brightest:",
        "step1_options": ["Creativity", "Autonomy", "Family", "Growth", "Stability", "Kindness", "Adventure", "Health"],
        "step2_header": "💨 Step 2: The Wind (Your Drains)",
        "step2_desc": "What environmental factors or stressors tend to blow out your light?",
        "step2_options": ["Micromanagement", "Lack of sleep", "Routine/Repetitive tasks", "Toxic environment", "Overwork", "Isolation"],
        "step3_header": "💼 Step 3: Current Focus",
        "step3_desc": "Where do you want to apply these values right now?",
        "step3_options": ["Career & Work", "Daily Routine & Lifestyle", "Relationships & Family"],
        "btn_analyze": "✨ Illuminate My Path",
        "loading": "Analyzing your Value Lantern...",
        "system_prompt": "You are an empathetic, insightful life coach specializing in the 'Value Lantern' exercise. Help the user understand their values and apply them. Respond ENTIRELY in English. Structure with: 🏮 The Light, 🛡️ The Glass, and 🚀 The Radiance (3 actions)."
    },
    "ja": {
        "title": "🏮 価値観のランタン・ワークショップ",
        "subtitle": "あなたの核心的な価値観を発見し、光を守り、人生を照らしましょう。",
        "step1_header": "🔥 ステップ 1: 燃料（あなたの価値観）",
        "step1_desc": "あなたのランタンを最も強く輝かせる価値観を最大3つ選んでください：",
        "step1_options": ["創造性", "自律性・自由", "家族・大切な人", "成長・学習", "安定・安心", "思いやり・貢献", "冒険・挑戦", "健康・ウェルビーイング"],
        "step2_header": "💨 ステップ 2: 強風（あなたを消耗させるもの）",
        "step2_desc": "どのような環境やストレス要因が、あなたのランタンの火を吹き消してしまいそうになりますか？",
        "step2_options": ["マイクロマネジメント", "睡眠不足・疲労", "単調な繰り返し作業", "ネガティブな環境", "過剰な労働", "孤独感・孤立"],
        "step3_header": "💼 ステップ 3: 現在のフォーカス",
        "step3_desc": "これらの価値観を、今どこで一番活かしたいですか？",
        "step3_options": ["キャリア・仕事", "日常生活・ライフスタイル", "人間関係・家族"],
        "btn_analyze": "✨ ランタンに火をともす",
        "loading": "ランタンのデータを分析中...",
        "system_prompt": "You are an empathetic, insightful life coach specializing in the 'Value Lantern' exercise. Help the user understand their values and apply them. Respond ENTIRELY in Japanese. Structure with: 🏮 あなたの光, 🛡️ ガラスの盾, and 🚀 日常を照らすアクション (3 steps)."
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

# --- 3. THE INTERACTIVE EXERCISE ---
st.subheader(t["step1_header"])
st.write(t["step1_desc"])
selected_values = st.multiselect("Values", t["step1_options"], max_selections=3, key="v", label_visibility="collapsed")

st.subheader(t["step2_header"])
st.write(t["step2_desc"])
selected_drains = st.multiselect("Drains", t["step2_options"], key="d", label_visibility="collapsed")

st.subheader(t["step3_header"])
st.write(t["step3_desc"])
selected_focus = st.selectbox("Focus", t["step3_options"], key="f", label_visibility="collapsed")

st.markdown("---")

# --- 4. FREE GEMINI AI GENERATION ---
if st.button(t["btn_analyze"], type="primary"):
    if not selected_values or not selected_drains:
        st.warning("Please pick at least one value and drain! / 価値観と消耗要因を1つ以上選択してください！")
    else:
        with st.spinner(t["loading"]):
            try:
                # Grab the free Gemini API key from Streamlit's settings
                gemini_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=gemini_key)
                
                # Setup the model with your custom system prompt
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=t["system_prompt"]
                )
                
                user_message = f"Values: {', '.join(selected_values)}\nDrains: {', '.join(selected_drains)}\nFocus Area: {selected_focus}"
                response = model.generate_content(user_message)
                
                st.balloons()
                st.success("Analysis Complete! / 分析が完了しました！")
                st.markdown("### 📋 Your Value Lantern Report")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Make sure your GEMINI_API_KEY is pasted in Streamlit Advanced Secrets! Error: {e}")
