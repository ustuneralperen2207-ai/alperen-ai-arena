import streamlit as st
from google import genai
from groq import Groq
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide", initial_sidebar_state="collapsed")

# --- KUSURSUZ CSS SİHİRBAZLIĞI (MOBİL UYUMLU VE %100 LOGOSUZ) ---
st.markdown("""
    <style>
    /* Sağ üstteki Github/Deploy butonlarını gizler */
    [data-testid="stToolbar"] {visibility: hidden !important;}
    
    /* En alttaki Streamlit yazısını ve gereksiz logoları gizler */
    footer {visibility: hidden !important;}
    
    /* Arka Plan: Yazıların okunması için hafif karanlık filtre eklendi */
    .stApp { 
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"); 
        background-size: cover; 
        background-attachment: fixed; 
    }
    
    /* Ana Başlık */
    .main-title { 
        color: #ffffff; 
        text-shadow: 2px 2px 5px #000000; 
        text-align: center; 
        font-weight: 800; 
        font-size: 2.2rem; 
        padding-top: 20px;
        padding-bottom: 20px;
    }
    
    /* Konuşma Balonları */
    .bubble { 
        backdrop-filter: blur(10px); 
        background: rgba(20, 20, 20, 0.6); 
        border: 1px solid rgba(255, 255, 255, 0.2); 
        border-radius: 15px; 
        padding: 20px; 
        margin: 15px 0; 
        color: #ffffff; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .bubble-a { border-left: 6px solid #00d2ff; }
    .bubble-b { border-left: 6px solid #ff512f; }
    
    /* Ajan Rapor Kartları */
    .agent-card { 
        background: rgba(0, 0, 0, 0.6); 
        border: 1px solid #00d2ff; 
        border-radius: 10px; 
        padding: 12px; 
        font-size: 0.85rem; 
        color: #e0f7fa; 
        margin-bottom: 10px; 
    }

    /* İnovatif Jüri Paneli */
    .judge-panel {
        background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(50,40,0,0.9));
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 25px;
        color: #ffd700;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        margin-top: 30px;
    }

    /* Sol Menü (Karanlık Mod) */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 15, 0.95) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN YAPAY ZEKA ARENASI</h1>', unsafe_allow_html=True)

# --- SOL MENÜ (MOBİLDE SOL ÜSTTEKİ > İKONU İLE AÇILIR) ---
with st.sidebar:
    st.header("🔑 Güvenlik & API")
    st.info("💡 Mobilde ekranı genişletmek için menüyü x tuşundan kapatabilirsiniz.")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    groq_key = st.text_input("Groq API Key:", type="password")
    
    st.divider()
    st.markdown("### ⚓ Kaptan Bilgileri")
    st.write("🎓 **Mezun:** Marina Yönetimi")
    st.write("📜 **Belgeler:** STCW & CMAS 2*")

# --- ANA İÇERİK ---
konu = st.text_area("🎯 Münazara Vizyonu:", value="Alperen Üstüner için denizcilik kariyeri mi, karada yöneticilik mi?", height=90)
baslat = st.button("🚀 AJANLARI VE SÖZCÜLERİ ATEŞLE", use_container_width=True)

# Kota koruma fonksiyonu
def safe_gen(client, prompt):
    time.sleep(3)
    return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text

if baslat:
    if not gemini_key or not groq_key: 
        st.error("⚠️ Lütfen sol üstteki ok (>) simgesine tıklayarak yan menüyü açın ve API şifrelerinizi girin!")
    else:
        g_client = genai.Client(api_key=gemini_key)
        gr_client = Groq(api_key=groq_key)

        st.success("✅ Sistem devrede! Ajanlar analiz yapıyor, lütfen bekleyin...")

        # 1. AJAN ARAŞTIRMALARI
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("🔍 **A Tarafı Raporu**")
            ajan1 = safe_gen(g_client, f"{konu} hakkında denizcilik/kaptanlık maaş ve vizyon verisi bul. 2 kısa cümle.")
            st.markdown(f'<div class="agent-card"><b>🌊 Stratejist:</b><br>{ajan1}</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown("🔍 **B Tarafı Raporu**")
            ajan2_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"{konu} hakkında karada yöneticilik avantajı yaz. 2 kısa cümle."}], model='llama-3.3-70b-versatile')
            ajan2 = ajan2_resp.choices[0].message.content
            st.markdown(f'<div class="agent-card"><b>🏢 Sektör Analisti:</b><br>{ajan2}</div>', unsafe_allow_html=True)

        # 2. ANA KAPIŞMA
        cevap_a = safe_gen(g_client, f"Ajan notu: {ajan1}. Konu: {konu}. Sadece denizciliği sertçe savun.")
        st.markdown(f'<div class="bubble bubble-a"><b>🔵 GEMINI (DENİZCİ EKOLÜ):</b><br><br>{cevap_a}</div>', unsafe_allow_html=True)

        cevap_b_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"A şunu dedi: {cevap_a}. Ajan notu: {ajan2}. Sadece karayı sertçe savun ve A'yı çürüt."}], model='llama-3.3-70b-versatile')
        cevap_b = cevap_b_resp.choices[0].message.content
        st.markdown(f'<div class="bubble bubble-b"><b>🟠 LLAMA (STRATEJİST EKOLÜ):</b><br><br>{cevap_b}</div>', unsafe_allow_html=True)

        # 3. JÜRİ PANELİ
        juri_karari = safe_gen(g_client, f"Tartışmayı oku: A: {cevap_a} B: {cevap_b}. Alperen'in geçmişini düşünerek ona mantıklı olanı seç ve tek bir kazanan ilan et.")
        
        st.markdown(f"""
            <div class="judge-panel">
                <h3>⚖️ JÜRİ HEYETİ NİHAİ KARARI</h3>
                <hr style="border-color:#ffd700;">
                {juri_karari}
            </div>
            """, unsafe_allow_html=True)
        
        st.balloons()
