import streamlit as st
from google import genai
from groq import Groq
import time

# --- SAYFA AYARLARI VE CSS ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden !important;}
    .stApp { background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"); background-size: cover; background-attachment: fixed; }
    .main-title { color: #ffffff; text-align: center; font-weight: 800; font-size: 2.2rem; padding: 20px 0; }
    .bubble { backdrop-filter: blur(10px); background: rgba(20, 20, 20, 0.7); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 15px; padding: 20px; margin: 15px 0; color: #ffffff; }
    .bubble-a { border-left: 6px solid #00d2ff; }
    .bubble-b { border-left: 6px solid #ff512f; }
    .agent-card { background: rgba(0, 0, 0, 0.7); border: 1px solid #00d2ff; border-radius: 10px; padding: 12px; font-size: 0.85rem; color: #e0f7fa; margin-bottom: 10px; }
    .judge-panel { background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(50,40,0,0.9)); border: 2px solid #ffd700; border-radius: 15px; padding: 25px; color: #ffd700; text-align: center; margin-top: 30px; }
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN YAPAY ZEKA ARENASI</h1>', unsafe_allow_html=True)

# --- ŞİFRE HAFIZASI (SESSION STATE) ---
if "g_key" not in st.session_state: st.session_state.g_key = ""
if "gr_key" not in st.session_state: st.session_state.gr_key = ""

with st.sidebar:
    st.header("🔑 Güvenlik & API")
    st.info("Kutulara şifrenizi yapıştırıp dışarı tıklamanız yeterlidir.")
    
    # type="password" ile siyah noktalar garantiye alındı (.strip() ile boşluklar silinir)
    gemini_input = st.text_input("Gemini API Key:", type="password", value=st.session_state.g_key)
    groq_input = st.text_input("Groq API Key:", type="password", value=st.session_state.gr_key)
    
    # Şifreyi hafızaya alırken başındaki/sonundaki görünmez boşlukları temizler
    st.session_state.g_key = gemini_input.strip()
    st.session_state.gr_key = groq_input.strip()
    
    # Onay Mekanizması
    if st.session_state.g_key and st.session_state.gr_key:
        st.success("✅ Şifreler başarıyla tanımlandı!")

    st.divider()
    st.markdown("### ⚓ Kaptan Bilgileri")
    st.write("🎓 **Mezun:** Marina Yönetimi")
    st.write("📜 **Belgeler:** STCW & CMAS 2*")

# --- ANA İÇERİK ---
konu = st.text_area("🎯 Münazara Vizyonu:", value="Alperen Üstüner için denizcilik kariyeri mi, karada yöneticilik mi?", height=90)
baslat = st.button("🚀 AJANLARI VE SÖZCÜLERİ ATEŞLE", use_container_width=True)

# ÇÖZÜM: Crash Önleyici (Anti-Crash) Fonksiyon
def safe_gen(client, prompt):
    time.sleep(3)
    try:
        return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text
    except Exception as e:
        return f"⚠️ API Hatası! Google Gemini şu an cevap vermiyor. Lütfen şifrenizi doğru kopyaladığınızdan emin olun."

if baslat:
    if not st.session_state.g_key or not st.session_state.gr_key: 
        st.error("⚠️ Lütfen sol menüden API şifrelerinizi eksiksiz girin!")
    else:
        g_client = genai.Client(api_key=st.session_state.g_key)
        gr_client = Groq(api_key=st.session_state.gr_key)

        st.success("✅ Sistem devrede! Ajanlar analiz yapıyor, lütfen bekleyin...")

        # 1. AJAN ARAŞTIRMALARI (Hata Korumalı)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("🔍 **A Tarafı Raporu**")
            ajan1 = safe_gen(g_client, f"{konu} hakkında denizcilik vizyonu bul. 2 kısa cümle.")
            st.markdown(f'<div class="agent-card"><b>🌊 Stratejist:</b><br>{ajan1}</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown("🔍 **B Tarafı Raporu**")
            try:
                ajan2_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"{konu} hakkında karada yöneticilik avantajı yaz. 2 kısa cümle."}], model='llama-3.3-70b-versatile')
                ajan2 = ajan2_resp.choices[0].message.content
            except Exception as e:
                ajan2 = "⚠️ Groq API Hatası. Şifrenizi kontrol edin."
            st.markdown(f'<div class="agent-card"><b>🏢 Sektör Analisti:</b><br>{ajan2}</div>', unsafe_allow_html=True)

        # 2. ANA KAPIŞMA
        cevap_a = safe_gen(g_client, f"Ajan notu: {ajan1}. Konu: {konu}. Sadece denizciliği sertçe savun.")
        st.markdown(f'<div class="bubble bubble-a"><b>🔵 GEMINI (DENİZCİ EKOLÜ):</b><br><br>{cevap_a}</div>', unsafe_allow_html=True)

        try:
            cevap_b_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"A şunu dedi: {cevap_a}. Ajan notu: {ajan2}. Sadece karayı sertçe savun ve A'yı çürüt."}], model='llama-3.3-70b-versatile')
            cevap_b = cevap_b_resp.choices[0].message.content
        except Exception as e:
            cevap_b = "⚠️ Llama 3 API Hatası. Şifrenizi kontrol edin."
        st.markdown(f'<div class="bubble bubble-b"><b>🟠 LLAMA (STRATEJİST EKOLÜ):</b><br><br>{cevap_b}</div>', unsafe_allow_html=True)

        # 3. JÜRİ PANELİ
        juri_karari = safe_gen(g_client, f"Tartışmayı oku: A: {cevap_a} B: {cevap_b}. Geçmişi düşünerek ona mantıklı olanı seç ve tek kazanan ilan et.")
        
        st.markdown(f'<div class="judge-panel"><h3>⚖️ JÜRİ HEYETİ NİHAİ KARARI</h3><hr style="border-color:#ffd700;">{juri_karari}</div>', unsafe_allow_html=True)
        st.balloons()
