import streamlit as st
import google.generativeai as genai
import time # 我們需要這個來做動畫效果

# --- 1. 頁面與視覺設定 ---
st.set_page_config(
    page_title="祿絟玄學 AI 商業決策系統",
    page_icon="🔮",
    layout="wide"
)

# 自定義 CSS：美化按鈕、隱藏選單、調整字體
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 讓按鈕看起來更高級 */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid #4CAF50;
    }
    
    /* 調整標題樣式 */
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 設定 AI ---
# 嘗試從 Streamlit 的秘密庫讀取 Key
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # 如果在自己電腦找不到秘密庫，就手動填入 (僅限本地測試用，上傳前刪掉)
    # 上傳到 GitHub 時，下面這行建議留空： genai.configure(api_key="")
    pass
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. 初始化記憶與狀態 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 側邊欄：控制台 ---
with st.sidebar:
    st.title("🎛️ 參數控制台")
    st.info("此系統結合大數據與傳統玄學，提供多維度決策支持。")
    
    role = st.selectbox(
        "🔮 選擇顧問模式",
        ["商業毒舌教練 (一針見血)", "玄學命理軍師 (五行佈局)", "溫暖心理諮詢 (情緒價值)", "冷靜數據分析師 (邏輯推演)"]
    )
    
    creativity = st.slider("💡 創意程度 (Temperature)", 0.0, 1.0, 0.7)
    
    st.write("---")
    if st.button("🗑️ 清空記憶 / 重啟"):
        st.session_state.messages = []
        st.rerun()

# --- 5. 主畫面：快捷操作區 ---
st.title("🔮 祿絟的 AI 決策系統 V1.0")
st.caption("🚀 結合商業邏輯與玄學智慧的虛擬智囊團")

# 快捷按鈕 (Quick Actions)
col1, col2, col3, col4 = st.columns(4)
user_prompt = None

with col1:
    if st.button("💰 創業點子評估"):
        user_prompt = "我有個創業點子，請幫我用最嚴格的商業邏輯評估，並指出 3 個致命風險。"
with col2:
    if st.button("😡 老闆罵人怎回"):
        user_prompt = "老闆剛剛罵了我一頓，請幫我生成一個不卑不亢、高情商的回覆，既能認錯又能展現價值。"
with col3:
    if st.button("📅 今日運勢解析"):
        user_prompt = "請結合今天的日期和五行能量，告訴我今天在工作上要注意什麼？什麼顏色能旺我？"
with col4:
    if st.button("💔 感情/合夥糾紛"):
        user_prompt = "我和合作夥伴（或伴侶）吵架了，請用玄學角度分析我們是否相沖，並給我一個解決方案。"

# --- 6. 聊天記錄顯示 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. 處理輸入 (核心邏輯) ---
# 如果用戶按了快捷按鈕，user_prompt 會有值；否則看聊天框
if prompt := (st.chat_input("請輸入您的問題...") or user_prompt):
    
    # 7.1 顯示用戶問題
    if not user_prompt: # 如果是按鈕觸發的，就不重複顯示在輸入框
        with st.chat_message("user"):
            st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 7.2 AI 思考與回應
    with st.chat_message("assistant"):
        # 建立一個佔位符
        response_container = st.empty()
        
        # --- ✨ 增加專業感：思考動畫 ---
        status_text = st.status("🧠 正在連結雲端大腦...", expanded=True)
        try:
            status_text.write("🔍 分析問題關鍵字...")
            time.sleep(0.5) # 假裝思考，增加儀式感
            
            status_text.write(f"⚡ 切換至「{role}」模式...")
            time.sleep(0.5)
            
            if "玄學" in role:
                status_text.write("☯️ 排盤運算五行生剋...")
                time.sleep(0.8)
            
            status_text.write("📝 正在生成最終策略...")
            
            # --- 呼叫 API ---
            # 這裡我們稍微調整 Prompt，要求 AI 用 Markdown 格式輸出，這樣比較漂亮
            full_prompt = f"""
            你現在是「{role}」。
            請用 Markdown 格式回答，適當使用粗體、列表和標題。
            如果是玄學模式，請給出一個「五行幸運指數（1-100分）」。
            
            用戶問題：{prompt}
            """
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(temperature=creativity)
            )
            
            # --- 顯示結果 ---
            status_text.update(label="✅ 分析完成！", state="complete", expanded=False)
            
            # 這裡我們可以把結果顯示得更好看
            response_container.markdown(response.text)
            
            # 存入記憶
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            status_text.update(label="❌ 發生錯誤", state="error")
            st.error(f"連線失敗：{e}")