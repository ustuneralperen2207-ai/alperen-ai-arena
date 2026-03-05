import streamlit as st
from google import genai
from groq import Groq
import time

# --- PROFESYONEL VE TEMİZ TASARIM ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide")

st.markdown("""
    <style>
    /* 1. SAĞ ALTTAKİ LOGOLARI SİLMEK İÇIN SİHİRLİ SATIRLAR (CRITICAL) */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2. ANA TASARIM */
    .stApp { 
        background: url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"); 
        background-size: cover; 
        background-attachment: fixed; 
    }
    .main-title { 
        color: white; 
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8); 
        text-align: center; 
        font-weight: 800; 
        font-size: 2.5rem; 
        padding: 20px 0;
    }
    
    /* Konuşma Balonları */
    .bubble { 
        backdrop-filter: blur(12px); 
        background: rgba(255, 255, 255, 0.1); 
        border: 1px solid rgba(255, 255, 255, 0.2); 
        border-radius: 20px; 
        padding: 20px; 
        margin: 10px 0; 
        color: white; 
    }
    .bubble-a { border-left: 8px solid #00d2ff; } /* Gemini */
    .bubble-b { border-left: 8px solid #ff512f; } /* Llama */
    
    /* Ajan Rapor Kartları */
    .agent-card { 
        background: rgba(0, 210, 255, 0.1); 
        border: 1px dashed #00d2ff; 
        border-radius: 10px; 
        padding: 10px; 
        font-size: 0.8rem; 
        color: #00d2ff; 
        margin: 5px; 
    }
    
    /* 3. İNOVATİF JÜRİ PANELİ (EN ALTA SABİTLENMİŞ) */
    .judge-panel-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        backdrop-filter: blur(15px);
        background: rgba(0, 0, 0, 0.9);
        border-top: 3px solid #ffd700;
        padding: 20px 0;
        z-index: 1000;
        text-align: center;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.5);
    }
    .judge-panel-text {
        color: #ffd700;
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* Sol Menü Arka Planı */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN ARAŞTIRMACI AI ARENASI</h1>', unsafe_allow_html=True)

# Sol Menü
with st.sidebar:
    st.header("🔑 Erişim Kontrolü")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    groq_key = st.text_input("Groq API Key:", type="password")
    st.divider()
    st.markdown("#### ⚓ Kaptan Bilgileri")
    st.write("Mezun: Marina Yönetimi")
    st.write("Belgeler: STCW & CMAS 2*")

# Konu ve Başlatma
konu = st.text_area("🎯 Münazara Vizyonu:", value="Alperen Üstüner için denizcilik kariyeri mi, karada yöneticilik mi?", height=80)
baslat = st.button("⚔️ AJANLARI VE SÖZCÜLERİ ATEŞLE", use_container_width=True)

# Kota dostu fonksiyon
def safe_gen(client, prompt):
    time.sleep(3) # İstekler arası zorunlu mola
    return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text

if baslat:
    if not gemini_key or not groq_key: 
        st.error("⚠️ API anahtarları eksik, lütfen sol menüden girin.")
    else:
        g_client = genai.Client(api_key=gemini_key)
        gr_client = Groq(api_key=groq_key)

        # 1. AJAN ARAŞTIRMALARI
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("🔍 **A Tarafı Ajan Raporları**")
            ajan1 = safe_gen(g_client, f"{konu} hakkında denizcilik maaş verisi bul. 2 kısa cümle.")
            st.markdown(f'<div class="agent-card"><b>Stratejist Raporu:</b><br>{ajan1}</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown("🔍 **B Tarafı Ajan Raporları**")
            ajan2 = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"{konu} hakkında kara yöneticiliği avantajı yaz. 2 kısa cümle."}], model='llama-3.3-70b-versatile').choices[0].message.content
            st.markdown(f'<div class="agent-card"><b>Sektör Analisti Raporu:</b><br>{ajan2}</div>', unsafe_allow_html=True)

        # 2. ANA KAPTIK
        # Gemini (A)
        cevap_a = safe_gen(g_client, f"Ajan notu: {ajan1}. Konu: {konu}. Denizciliği savun.")
        st.markdown(f'<div class="bubble bubble-a"><b>🌊 GEMINI (DENİZCİ):</b><br><br>{cevap_a}</div>', unsafe_allow_html=True)

        # Llama (B)
        cevap_b = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"A şunu dedi: {cevap_a}. Ajan notu: {ajan2}. Karayı savun."}], model='llama-3.3-70b-versatile').choices[0].message.content
        st.markdown(f'<div class="bubble bubble-b"><b>🏢 LLAMA (STRATEJİST):</b><br><br>{cevap_b}</div>', unsafe_allow_html=True)

        # 3. İNOVATİF SABİT JÜRİ PANELİ (NİHAİ KARAR)
        juri_karari = safe_gen(g_client, f"Tartışmayı oku: A: {cevap_a} B: {cevap_b}. Alperen için kesin bir kazanan seç.")
        
        # Ekranın en altına sabitlenen jüri paneli
        st.markdown(f"""
            <div class="judge-panel-container">
                <div class="judge-panel-text">
                    <h3>⚖️ JÜRİ HEYETİ NİHAİ KARARI</h3><br>
                    {juri_karari}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.balloons()
        
        # Juri paneli sabit olduğu için sayfanın altına boşluk ekliyoruz
        st.write("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
