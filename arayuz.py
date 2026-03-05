import streamlit as st
from google import genai
from groq import Groq
import time

# --- PROFESYONEL TASARIM ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"); background-size: cover; background-attachment: fixed; }
    .main-title { color: white; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); text-align: center; font-weight: 800; font-size: 2.5rem; }
    .bubble { backdrop-filter: blur(12px); background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 20px; margin: 10px 0; color: white; }
    .agent-card { background: rgba(0, 210, 255, 0.1); border: 1px dashed #00d2ff; border-radius: 10px; padding: 10px; font-size: 0.8rem; color: #00d2ff; margin: 5px; }
    .judge-panel { background: rgba(0, 0, 0, 0.8); border: 2px solid #ffd700; border-radius: 15px; padding: 20px; color: #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN ARAŞTIRMACI AI ARENASI</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Erişim & Kontrol")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    groq_key = st.text_input("Groq API Key:", type="password")
    st.divider()
    st.markdown("#### ⚓ Kaptan Bilgileri")
    st.write("Mezuniyet: Marina ve Yat İşletmeciliği")
    st.write("Sertifika: STCW & CMAS 2*")

# --- ANA PANEL ---
konu = st.text_area("🎯 Tartışılacak Vizyon:", value="Alperen Üstüner için denizcilik kariyeri mi, karada yöneticilik mi?", height=70)
baslat = st.button("⚔️ AJANLARI VE SÖZCÜLERİ ATEŞLE", use_container_width=True)

def safe_gen(client, prompt):
    time.sleep(2) # Kota dostu bekleme
    return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text

if baslat:
    if not gemini_key or not groq_key: st.error("Lütfen anahtarları girin!")
    else:
        g_client = genai.Client(api_key=gemini_key)
        gr_client = Groq(api_key=groq_key)

        # --- AJAN ARAŞTIRMALARI ---
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("🔍 **A Tarafı Ajan Raporları**")
            ajan1 = safe_gen(g_client, f"{konu} hakkında denizcilik maaş ve kariyer verisi bul. 2 kısa cümle.")
            st.markdown(f'<div class="agent-card"><b>Stratejist Raporu:</b><br>{ajan1}</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown("🔍 **B Tarafı Ajan Raporları**")
            ajan2 = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"{konu} hakkında kara yöneticiliği avantajı yaz. 2 kısa cümle."}], model='llama-3.3-70b-versatile').choices[0].message.content
            st.markdown(f'<div class="agent-card"><b>Sektör Analisti Raporu:</b><br>{ajan2}</div>', unsafe_allow_html=True)

        # --- ANA MÜNAZARA ---
        cevap_a = safe_gen(g_client, f"Ajan notu: {ajan1}. Konu: {konu}. Denizciliği savun.")
        st.markdown(f'<div class="bubble" style="border-left: 8px solid #00d2ff;"><b>🌊 GEMINI (DENİZCİ):</b><br>{cevap_a}</div>', unsafe_allow_html=True)

        cevap_b = gr_client.chat.completions.create(messages=[{"role": "user", "content": f"A şunu dedi: {cevap_a}. Ajan notu: {ajan2}. Karayı savun."}], model='llama-3.3-70b-versatile').choices[0].message.content
        st.markdown(f'<div class="bubble" style="border-left: 8px solid #ff512f;"><b>🏢 LLAMA (STRATEJİST):</b><br>{cevap_b}</div>', unsafe_allow_html=True)

        # --- DETAYLI JÜRİ PANELİ ---
        st.divider()
        juri_karari = safe_gen(g_client, f"Şu tartışmayı değerlendir ve Alperen için bir yol çiz: A: {cevap_a} B: {cevap_b}")
        st.markdown(f'<div class="judge-panel"><h3>⚖️ JÜRİ HEYETİ NİHAİ KARARI</h3><br>{juri_karari}</div>', unsafe_allow_html=True)
        st.balloons()
