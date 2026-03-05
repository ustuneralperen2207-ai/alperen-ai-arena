import streamlit as st
from google import genai
from groq import Groq
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide")

# --- CSS (Görsel Tasarım) ---
st.markdown("""
    <style>
    footer {visibility: hidden !important;}
    .stApp { 
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"); 
        background-size: cover; background-attachment: fixed; 
    }
    .main-title { color: #ffffff; text-align: center; font-weight: 800; font-size: 2.2rem; padding: 20px 0; }
    .bubble { backdrop-filter: blur(10px); background: rgba(20, 20, 20, 0.7); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 15px; padding: 20px; margin: 15px 0; color: #ffffff; }
    .bubble-a { border-left: 6px solid #00d2ff; }
    .bubble-b { border-left: 6px solid #ff512f; }
    .agent-card { background: rgba(0, 0, 0, 0.7); border: 1px solid #00d2ff; border-radius: 10px; padding: 12px; font-size: 0.85rem; color: #e0f7fa; margin-bottom: 10px; }
    .judge-panel { background: linear-gradient(135deg, rgba(20,20,20,0.9), rgba(50,40,0,0.9)); border: 2px solid #ffd700; border-radius: 15px; padding: 25px; color: #ffd700; text-align: center; margin-top: 30px; }
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95) !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stSidebar"] input { color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN YAPAY ZEKA ARENASI</h1>', unsafe_allow_html=True)

# --- SOL MENÜ VE ŞİFRELER ---
with st.sidebar:
    st.header("🔑 Güvenlik & API")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    groq_key = st.text_input("Groq API Key:", type="password")
    
    st.divider()
    st.markdown("### ⚓ Kaptan Bilgileri")
    st.write("Yapay zekalar bu bilgileri sadece konuyla ilgiliyse dikkate alacaktır.")
    st.write("🎓 **Mezun:** Marina Yönetimi")
    st.write("📜 **Belgeler:** STCW & CMAS 2*")

# --- ANA İÇERİK ---
konu = st.text_area("🎯 Münazara Vizyonu (İstediğin konuyu yaz):", value="Yapay zeka insanlığın sonunu mu getirecek, yoksa kurtarıcısı mı olacak?", height=90)
baslat = st.button("🚀 AJANLARI VE SÖZCÜLERİ ATEŞLE", use_container_width=True)

# Gelişmiş Hata Yakalayıcı (Model 2.5 Flash olarak güncellendi)
def safe_gen(client, prompt):
    time.sleep(3) 
    try:
        return client.models.generate_content(model='gemini-2.5-flash', contents=prompt).text
    except Exception as e:
        return f"⚠️ Gemini Hatası: Lütfen limitleri aşmadığınızdan veya şifrenizi doğru girdiğinizden emin olun. (Detay: {str(e)})"

if baslat:
    g_key_clean = gemini_key.strip() if gemini_key else ""
    gr_key_clean = groq_key.strip() if groq_key else ""

    if not g_key_clean or not gr_key_clean: 
        st.error("⚠️ Lütfen sol menüden API şifrelerinizi eksiksiz girin!")
    else:
        g_client = genai.Client(api_key=g_key_clean)
        gr_client = Groq(api_key=gr_key_clean)

        st.success("✅ Sistem devrede! Ajanlar belirlediğiniz konu üzerine istihbarat topluyor...")

        # 1. AJANLAR (Artık konuya göre dinamik çalışıyorlar)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("🔍 **A Tarafı (Destekleyici) Raporu**")
            ajan1 = safe_gen(g_client, f"Konu: '{konu}'. Bu konuda 'A Tarafı'nı (Destekleyen/Pozitif yön) temsil edeceksin. Bu görüşü destekleyen 2 kısa cümlelik mantıklı bir ön bilgi hazırla.")
            st.markdown(f'<div class="agent-card"><b>🔵 Ajan 1:</b><br>{ajan1}</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown("🔍 **B Tarafı (Karşıt) Raporu**")
            try:
                ajan2_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"Konu: '{konu}'. Bu konuda 'B Tarafı'nı (Karşı çıkan/Negatif yön) temsil edeceksin. Karşıt görüşü savunan 2 kısa cümlelik bir ön bilgi hazırla."}], model='llama-3.3-70b-versatile')
                ajan2 = ajan2_resp.choices[0].message.content
            except Exception as e:
                ajan2 = f"⚠️ Groq Hatası: {str(e)}"
            st.markdown(f'<div class="agent-card"><b>🟠 Ajan 2:</b><br>{ajan2}</div>', unsafe_allow_html=True)

        # 2. SÖZCÜLER (Özgür tartışma)
        cevap_a = safe_gen(g_client, f"Sen A tarafısın. Tartışma Konusu: '{konu}'. Ajanının şu notunu kullan: '{ajan1}'. Sadece kendi tarafını ikna edici ve sert bir üslupla savun. Asla karşı tarafın haklı olabileceğini kabul etme.")
        st.markdown(f'<div class="bubble bubble-a"><b>🔵 GEMINI (A TARAFI):</b><br><br>{cevap_a}</div>', unsafe_allow_html=True)

        try:
            cevap_b_resp = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"Sen B tarafısın. Tartışma Konusu: '{konu}'. A tarafı şunu dedi: '{cevap_a}'. Ajanının şu notunu kullan: '{ajan2}'. A tarafının mantığını acımasızca çürüt ve tam zıttı olan kendi görüşünü savun."}], model='llama-3.3-70b-versatile')
            cevap_b = cevap_b_resp.choices[0].message.content
        except Exception as e:
            cevap_b = f"⚠️ Llama Hatası: {str(e)}"
        st.markdown(f'<div class="bubble bubble-b"><b>🟠 LLAMA (B TARAFI):</b><br><br>{cevap_b}</div>', unsafe_allow_html=True)

        # 3. JÜRİ (Tarafsız)
        juri_karari = safe_gen(g_client, f"Sen tarafsız bir jürisin. Konu: '{konu}'.\n\nA Tarafı'nın Argümanı: {cevap_a}\n\nB Tarafı'nın Argümanı: {cevap_b}\n\nİki tarafı mantık, tutarlılık ve ikna edicilik açısından değerlendir. Açıklamanı yaptıktan sonra KESİN BİR KAZANAN ilan et.")
        st.markdown(f'<div class="judge-panel"><h3>⚖️ JÜRİ HEYETİ NİHAİ KARARI</h3><hr style="border-color:#ffd700;">{juri_karari}</div>', unsafe_allow_html=True)
        st.balloons()
