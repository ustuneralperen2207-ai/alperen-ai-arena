import streamlit as st
from google import genai
from groq import Groq
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide")

# --- KUSURSUZ VE SORUNSUZ CSS ---
st.markdown("""
    <style>
    /* Gereksiz logoları gizle */
    footer {visibility: hidden !important;}
    
    /* Arka Plan */
    .stApp { 
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"); 
        background-size: cover; 
        background-attachment: fixed; 
    }
    .main-title { color: #ffffff; text-align: center; font-weight: 800; font-size: 2.2rem; padding: 20px 0; }
    
    /* Balonlar ve Kartlar */
    .bubble { backdrop-filter: blur(10px); background: rgba(20, 20, 20, 0.7); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 15px; padding: 20px; margin: 15px 0; color: #ffffff; }
    .bubble-a { border-left: 6px solid #00d2ff; }
    .bubble-b { border-left: 6px solid #ff512f; }
    .agent-card { background: rgba(0, 0, 0, 0.7); border: 1px solid #00d2ff; border-radius: 10px; padding: 12px; font-size: 0.85rem; color: #e0f7fa; margin-bottom: 10px; }
    .judge-panel { background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(50,40,0,0.9)); border: 2px solid #ffd700; border-radius: 15px; padding: 25px; color: #ffd700; text-align: center; margin-top: 30px; }
    
    /* Sol Menü Düzenlemesi - BEYAZ YAZI HATASI BURADA ÇÖZÜLDÜ */
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95) !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stSidebar"] input { color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN YAPAY ZEKA ARENASI</h1>', unsafe_allow_html=True)

# --- SOL MENÜ VE ŞİFRELER ---
with st.sidebar:
    st.header("🔑 Güvenlik & API")
    
    # Şifreler artık net bir şekilde nokta nokta (••••) görünecek
    gemini_key = st.text_input("Gemini API Key:", type="password")
    groq_key = st.text_input("Groq API Key:", type="password")

    st.divider()
    st.markdown("### ⚓ Kaptan Bilgileri")
    st.write("🎓 **Mezun:** Marina Yönetimi")
    st.write("📜 **Belgeler:** STCW & CMAS 2*")

# --- ANA İÇERİK ---
konu = st.text_area("🎯 Münazara Vizyonu:", value="Alperen Üstüner için denizcilik kariyeri mi, karada yöneticilik mi?", height=90)
baslat = st.button("🚀 AJANLARI VE SÖZCÜLERİ ATEŞLE", use_container_width=True)

# Gelişmiş Hata Yakalayıcı (Google'ın neden kızdığını bize söyleyecek)
def safe_gen(client, prompt):
    time.sleep(3) # Google kota limiti için bekleme
    try:
        return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text
    except Exception as e:
        return f"⚠️ Gemini Hatası: {str(e)} (Şifre yanlış olabilir veya dakikalık ücretsiz limitiniz dolmuş olabilir.)"

if baslat:
    # Boşlukları otomatik silen koruma
    g_key_clean = gemini_key.strip() if gemini_key else ""
    gr_key_clean = groq_key.strip() if groq_key else ""

    if not g_key_clean or not gr_key_clean: 
        st.error("⚠️ Lütfen sol menüden API şifrelerinizi eksiksiz girin!")
    else:
        g_client = genai.Client(api_key=g_key_clean)
        gr_client = Groq(api_key=gr_key_clean)

        st.success("✅ Sistem devrede! Ajanlar analiz yapıyor, lütfen bekleyin...")

        # 1. AJANLAR
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
                ajan2 = f"⚠️ Groq Hatası: {str(e)}"
            st.markdown(f'<div class="agent-card"><b>🏢 Sektör Analisti:</b><br>{ajan2}</div>', unsafe_allow_html=True)

        # 2. SÖZCÜLER
        cevap_a = safe_gen(g_client, f"Ajan notu: {ajan1}. Konu: {konu}. Sadece denizciliği sertçe savun.")
        st.markdown(f'<div class="bubble bubble-a"><b>🔵 GEMINI (DENİZCİ EKOLÜ):</b><br><br>{cevap_a}</div>', unsafe_allow_html=True)

        try:
            cevap_b_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"A şunu dedi: {cevap_a}. Ajan notu: {ajan2}. Sadece karayı sertçe savun ve A'yı çürüt."}], model='llama-3.3-70b-versatile')
            cevap_b = cevap_b_resp.choices[0].message.content
        except Exception as e:
            cevap_b = f"⚠️ Llama Hatası: {str(e)}"
        st.markdown(f'<div class="bubble bubble-b"><b>🟠 LLAMA (STRATEJİST EKOLÜ):</b><br><br>{cevap_b}</div>', unsafe_allow_html=True)

        # 3. JÜRİ
        juri_karari = safe_gen(g_client, f"Tartışmayı oku: A: {cevap_a} B: {cevap_b}. Geçmişi düşünerek ona mantıklı olanı seç ve tek kazanan ilan et.")
        st.markdown(f'<div class="judge-panel"><h3>⚖️ JÜRİ HEYETİ NİHAİ KARARI</h3><hr style="border-color:#ffd700;">{juri_karari}</div>', unsafe_allow_html=True)
        st.balloons()
