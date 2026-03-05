import streamlit as st
from google import genai
from groq import Groq
import time

# --- TASARIM VE CAM EFEKTİ ---
st.set_page_config(page_title="Alperen'in AI Arenası", page_icon="🏟️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-title { color: white; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); text-align: center; font-weight: 800; font-size: 3rem; }
    .bubble { backdrop-filter: blur(12px); background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 25px; padding: 20px; margin: 15px 0; color: white; }
    .bubble-a { border-left: 10px solid #00d2ff; }
    .bubble-b { border-left: 10px solid #ff512f; }
    .agent-note { font-size: 0.85rem; color: #00d2ff; font-style: italic; margin-bottom: 5px; }
    .judge-panel { background: rgba(0, 0, 0, 0.7); border: 2px solid #ffd700; border-radius: 20px; padding: 25px; color: #ffd700; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏟️ ALPEREN\'İN ARAŞTIRMACI AI ARENASI</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 Erişim Paneli")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    groq_key = st.text_input("Groq API Key:", type="password")
    st.info("İpucu: 429 hatası alırsanız 1 dakika bekleyip tekrar deneyin.")

col_mid = st.columns([1, 5, 1])[1]
with col_mid:
    konu = st.text_area("🎯 Münazara Konusu:", value="Alperen Üstüner için denizcilik kariyeri mi, karada yöneticilik mi?", height=80)
    baslat = st.button("⚔️ AJANLARI GÖREVE ÇAĞIR", use_container_width=True)

# --- HATA YAKALAMA FONKSİYONU (Quota Koruması) ---
def safe_generate(client, model_id, prompt):
    try:
        time.sleep(1) # Her istek öncesi 1 sn bekleme (Kota dostu)
        return client.models.generate_content(model=model_id, contents=prompt).text
    except Exception as e:
        if "429" in str(e):
            st.warning("⚠️ Google Kotası Doldu. 5 saniye içinde tekrar deniyorum...")
            time.sleep(5)
            return client.models.generate_content(model=model_id, contents=prompt).text
        return f"Hata oluştu: {str(e)}"

if baslat:
    if not gemini_key or not groq_key:
        st.error("API anahtarları eksik!")
    else:
        g_client = genai.Client(api_key=gemini_key)
        gr_client = Groq(api_key=groq_key)
        
        # --- AJAN ARAŞTIRMA SÜRECİ ---
        with st.status("🕵️ Araştırmacı Ajanlar Çalışıyor...", expanded=True) as status:
            # A Tarafı Ajanları (Google Gemini üzerinden)
            st.write("🔍 **Ajan 1 (Denizcilik Stratejisti):** Marina mezuniyetinin avantajlarını analiz ediyor...")
            analiz1 = safe_generate(g_client, 'gemini-1.5-flash', f"Konu: {konu}. Marina yönetimi ve STCW belgelerinin global iş pazarındaki değerini 2 cümlede özetle.")
            
            st.write("🔍 **Ajan 2 (Ekonomik Analist):** Maaş ve sürdürülebilirlik raporu hazırlıyor...")
            analiz2 = safe_generate(g_client, 'gemini-1.5-flash', f"Konu: {konu}. Denizcilik vs Kara yöneticiliği maaş potansiyelini 2 cümlede kıyasla.")
            
            # B Tarafı Ajanları (Groq üzerinden - Hızlı ve Kotasız)
            st.write("🔍 **Ajan 3 (Aile ve Düzen Danışmanı):** Karada yaşamanın psikolojik etkilerini inceliyor...")
            gr_res = gr_client.chat.completions.create(
                messages=[{"role": "user", "content": f"Konu: {konu}. Karada düzenli bir hayatın avantajlarını 2 cümlede yaz."}],
                model='llama-3.3-70b-versatile'
            )
            analiz3 = gr_res.choices[0].message.content
            
            status.update(label="✅ Tüm veriler toplandı. Sözcüler sahneye çıkıyor!", state="complete")

        # --- TARAFLARIN KONUŞMASI ---
        # Gemini (A Tarafı) ajanların verisini kullanarak konuşur
        prompt_A = f"Sen A tarafısın. Ajanlarının şu verilerini kullan: '{analiz1}' ve '{analiz2}'. Konu: {konu}. Denizciliği savun."
        cevap_A = safe_generate(g_client, 'gemini-1.5-flash', prompt_A)
        
        st.markdown(f'<div class="bubble bubble-a"><div class="agent-note">📡 Ajan Analizi Dahil Edildi</div><b>🌊 GEMINI (DENİZCİ EKOLÜ):</b><br><br>{cevap_A}</div>', unsafe_allow_html=True)

        # Llama (B Tarafı)
        prompt_B = f"A tarafı şunu dedi: '{cevap_A}'. Ajanın şu notunu kullan: '{analiz3}'. Karada kalmayı savun ve A'yı çürüt."
        res_b = gr_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_B}],
            model='llama-3.3-70b-versatile'
        )
        cevap_B = res_b.choices[0].message.content
        st.markdown(f'<div class="bubble bubble-b"><div class="agent-note">📡 Ajan Analizi Dahil Edildi</div><b>🏢 LLAMA 3.3 (KARA STRATEJİSTİ):</b><br><br>{cevap_B}</div>', unsafe_allow_html=True)

        # --- HAKEM HEYETİ ---
        st.divider()
        hakem_final = safe_generate(g_client, 'gemini-1.5-flash', f"Şu tartışmayı teknik ve mantık açısından puanla. A: {cevap_A} B: {cevap_B}. Alperen Üstüner için kesin bir kazanan seç.")
        st.markdown(f'<div class="judge-panel"><h3>⚖️ HAKEM HEYETİ KARARI</h3><br>{hakem_final}</div>', unsafe_allow_html=True)
        st.balloons()
