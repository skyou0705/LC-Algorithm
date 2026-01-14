import streamlit as st
import google.generativeai as genai
import time
import urllib.parse # 用來處理圖片網址的

# --- 1. 頁面設定 ---
st.set_page_config(
    page_title="祿絟 AI 創意工廠",
    page_icon="🎨",
    layout="wide"
)

# 自定義 CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid #FF4B4B;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #FF9A9E, #FECFEF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 設定 AI (Gemini) ---
# 這裡一樣，本地測試用除了 try-except，建議上傳前把 Key 刪掉
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # 本地測試請填入您的 Key，上傳前請留空
    genai.configure(api_key="") 

model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. 側邊欄 ---
with st.sidebar:
    st.title("🎛️ 創意控制台")
    st.image("https://cdn-icons-png.flaticon.com/512/8673/8673233.png", width=80)
    st.write("---")
    st.info("左側是文字大腦 (Gemini)，右側是圖像引擎 (Pollinations)。")

# --- 4. 主畫面：分頁設計 (Tabs) ---
st.title("🎨 Luquan 的 AI 創意工廠")

# 建立兩個分頁
tab1, tab2 = st.tabs(["🧠 商業/玄學顧問 (文字)", "🎨 AI 繪圖生成器 (圖片)"])

# ==========================
# 分頁 1: 原本的文字功能
# ==========================
with tab1:
    st.header("商業與玄學諮詢")
    
    # 初始化文字記憶
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 顯示歷史訊息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 文字輸入框
    if prompt := st.chat_input("請輸入您的問題..."):
        # 顯示用戶輸入
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI 回答
        with st.chat_message("assistant"):
            with st.spinner("正在思考中..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"錯誤：{e}")

# ==========================
# 分頁 2: 新增的繪圖功能 (黑科技)
# ==========================
with tab2:
    st.header("✨ 免費 AI 繪圖生成")
    st.caption("輸入描述，AI 自動為你生成高品質圖片 (不限次數)")
    
    col_input, col_btn = st.columns([3, 1])
    
    with col_input:
        img_prompt = st.text_input("請描述你想畫的畫面 (建議用英文，或讓 AI 幫你翻譯)", placeholder="例如：一隻在太空漫步的賽博龐克貓咪")
    
    with col_btn:
        st.write("") #用來對齊
        st.write("") 
        generate_btn = st.button("🎨 開始繪圖")

    if generate_btn and img_prompt:
        with st.spinner("正在呼叫繪圖引擎..."):
            try:
                # --- 步驟 A: 如果用戶輸入中文，先用 Gemini 翻譯成英文 Prompt (畫得比較準) ---
                trans_prompt = f"Translate this to a detailed English image prompt: {img_prompt}"
                translation = model.generate_content(trans_prompt).text
                
                # --- 步驟 B: 使用 URL 黑科技生成圖片 ---
                # 我們把 Prompt 塞進網址裡，這個網站會直接回傳圖片
                encoded_prompt = urllib.parse.quote(translation)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
                
                # --- 步驟 C: 顯示圖片 ---
                st.success(f"生成完畢！(關鍵詞: {translation})")
                st.image(image_url, caption="由 Luquan AI 生成", use_container_width=True)
                
                # 下載按鈕 (讓用戶覺得這很有價值)
                st.info("💡 右鍵點擊圖片即可存檔")
                
            except Exception as e:
                st.error("繪圖失敗，請稍後再試。")