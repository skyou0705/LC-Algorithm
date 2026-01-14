import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- 1. 頁面基礎設定 (必須在第一行) ---
st.set_page_config(
    page_title="Luquan AI | 玄學商業智囊",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS 設計師專區 (這裡是改外觀的重點) ---
st.markdown("""
    <style>
    /* 1. 全局背景：深色漸層，營造神秘高級感 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #FFFFFF;
    }
    
    /* 2. 隱藏預設的醜醜選單，但保留頂部空間 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 3. 標題樣式：紫金漸層字體 */
    h1 {
        background: -webkit-linear-gradient(45deg, #FFD700, #c77dff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        padding-bottom: 20px;
    }
    
    /* 4. 按鈕樣式：霓虹光澤按鈕 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6200ea, #b388ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0px 5px 15px rgba(98, 0, 234, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(98, 0, 234, 0.6);
    }
    
    /* 5. 輸入框美化 */
    .stTextInput>div>div>input, .stChatInput>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid #6200ea;
        border-radius: 15px;
    }
    
    /* 6. 側邊欄美化 */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 7. 聊天氣泡美化 */
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 設定 AI (Gemini) ---
try:
    # 嘗試從 Streamlit 雲端讀取 Key
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # 本地測試時，如果沒有設定 secrets，請在這裡填入 Key (上傳前建議留空)
    genai.configure(api_key="") 

model = genai.GenerativeModel('gemini-2.5-flash')

# --- 4. 側邊欄：品牌形象 ---
with st.sidebar:
    st.markdown("### 🔮 Luquan Metaphysics")
    st.caption("AI 與傳統智慧的終極結合")
    
    # 這裡可以放您的 Logo 圖片網址 (現在先用一個佔位符)
    st.image("https://cdn-icons-png.flaticon.com/512/6154/6154782.png", width=100)
    
    st.write("---")
    st.info("💡 **使用指南：**\n\n左側標籤切換功能，可進行商業諮詢或生成視覺圖像。")
    st.write("---")
    
    # 增加一個「聯繫作者」按鈕
    st.link_button("🌐 訪問祿絟的官方網站", "https://your-website.com")

# --- 5. 主畫面：功能分頁 ---
st.title("Luquan AI 決策中樞")

# 這裡我們用 CSS 調整了 Tabs 的外觀
tab1, tab2 = st.tabs(["🧠 全能顧問 (Text)", "🎨 靈感繪圖 (Image)"])

# ==========================
# 分頁 1: 商業與玄學顧問
# ==========================
with tab1:
    st.markdown("#### 💬 與您的專屬 AI 軍師對話")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 顯示對話紀錄
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("輸入問題：比如『幫我算算這個創業點子』或『今天穿什麼顏色旺我』..."):
        # 用戶訊息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI 回覆
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("🔮 正在連結高維數據庫..."):
                try:
                    # 這裡加上一個 System Prompt，強制 AI 保持人設
                    system_prompt = f"你現在是祿絟玄學 AI，請用專業、有深度且帶有一點神秘感的口吻回答。回答問題：{prompt}"
                    response = model.generate_content(system_prompt)
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    message_placeholder.error(f"連線中斷：{e}")

# ==========================
# 分頁 2: 繪圖生成
# ==========================
with tab2:
    st.markdown("#### ✨ 描述畫面，即刻顯化")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        img_prompt = st.text_input("請描述畫面 (例如：一條由霓虹燈組成的金龍，在未來的吉隆坡夜空飛行)", key="img_input")
    
    with col2:
        st.write("") # 排版佔位
        st.write("") 
        generate_btn = st.button("🎨 開始顯化", use_container_width=True)

    if generate_btn and img_prompt:
        with st.spinner("🎨 AI 畫師正在構圖中..."):
            try:
                # 1. 翻譯 Prompt
                trans_prompt = f"Translate this into a high-quality, detailed English text-to-image prompt, focus on aesthetics: {img_prompt}"
                translation = model.generate_content(trans_prompt).text
                
                # 2. 生成圖片 URL
                encoded_prompt = urllib.parse.quote(translation)
                # 這裡加了 seed 參數讓每次隨機，並設定寬高比
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"
                
                # 3. 展示
                st.image(image_url, caption=f"✨ {translation}", use_container_width=True)
                st.balloons() # 加一點成功特效
                
            except Exception as e:
                st.error("生成失敗，請稍後再試。")