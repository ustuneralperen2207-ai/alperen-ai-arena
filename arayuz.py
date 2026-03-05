import streamlit as st
from google import genai
from groq import Groq
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Otonom AI Ajansı", page_icon="🏢", layout="wide")

# --- KURUMSAL AJANS TASARIMI (CSS) ---
st.markdown("""
    <style>
    footer {visibility: hidden !important;}
    .stApp { background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), url("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1920&q=80"); background-size: cover; background-attachment: fixed; }
    .main-title { color: #ffffff; text-align: center; font-weight: 800; font-size: 2.5rem; padding: 20px 0; letter-spacing: 1px;}
    .agent-card { background: rgba(20, 25, 40, 0.85); border-top: 4px solid #00d2ff; border-radius: 10px; padding: 20px; color: #e0f7fa; font-size: 0.9rem; height: 350px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5);}
    .article-panel { background: rgba(255, 255, 255, 0.95); border-left: 8px solid #2196f3; border-radius: 10px; padding: 40px; color: #1a1a1a; margin-top: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.6); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6;}
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] input { color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏢 OTONOM YAPAY ZEKA AJANSI</h1>', unsafe_allow_html=True)

# --- SOL MENÜ ---
with st.sidebar:
    st.header("🔑 Ajans Yönetimi")
    gemini_key = st.text_input("Gemini API (Sadece Baş Editör):", type="password")
    groq_key = st.text_input("Groq API (Araştırmacı & Analist):", type="password")
    
    st.divider()
    st.info("💡 **Bilgi:** Sistem limitleri aşmamak için ağır araştırmaları Llama 3'e yaptırır, son düzenlemeyi Gemini'ye bırakır.")

# --- İŞ EMRİ (GÖREV) ---
gorev = st.text_area("🎯 Ajansa Verilecek İş Emri (Herhangi bir konu yazın):", value="İnsanlık Mars'a koloni kurduğunda, Dünya'daki ekonomi ve uluslararası ilişkiler bundan nasıl etkilenir?", height=90)
baslat = st.button("🚀 AJANSI ÇALIŞTIR", use_container_width=True)

# Güvenli İstek Fonksiyonları
def safe_gemini(client, prompt):
    time.sleep(2) 
    try:
        return client.models.generate_content(model='gemini-2.5-flash', contents=prompt).text
    except Exception as e:
        return f"⚠️ Gemini Hatası (Kota dolmuş olabilir): {str(e)}"

def safe_groq(client, prompt):
    try:
        resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model='llama-3.3-70b-versatile')
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Groq Hatası: {str(e)}"

if baslat:
    g_key_clean = gemini_key.strip() if gemini_key else ""
    gr_key_clean = groq_key.strip() if groq_key else ""

    if not g_key_clean or not gr_key_clean: 
        st.error("⚠️ Lütfen sol menüden API şifrelerinizi girin!")
    else:
        g_client = genai.Client(api_key=g_key_clean)
        gr_client = Groq(api_key=gr_key_clean)

        st.success("✅ İş Emri Alındı! Llama 3 araştırmaya başladı...")

        col_a, col_b = st.columns(2)
        
        # 1. AŞAMA: ARAŞTIRMA (ARTIK GROQ/LLAMA YAPIYOR)
        with col_a:
            st.markdown("### 🔍 1. Araştırmacı (Llama 3)")
            with st.spinner("İnternet ve veri tabanları taranıyor..."):
                prompt1 = f"Sen kıdemli bir araştırmacısın. Görev: '{gorev}'. Bu konu hakkında derinlemesine bir araştırma yap. Önemli gerçekleri, verileri ve dinamikleri topla. Yorum katmadan objektif verileri listele."
                arastirma_notu = safe_groq(gr_client, prompt1)
                st.markdown(f'<div class="agent-card">{arastirma_notu}</div>', unsafe_allow_html=True)
                
        # 2. AŞAMA: ANALİZ VE ELEŞTİRİ (YİNE GROQ/LLAMA)
        with col_b:
            st.markdown("### 🧠 2. Eleştirel Analist (Llama 3)")
            with st.spinner("Araştırma verileri denetleniyor..."):
                prompt2 = f"Sen eleştirel bir stratejistsin. Görev: '{gorev}'. Araştırmacının topladığı veriler şunlar: '{arastirma_notu}'. Bu verilerdeki eksikleri bul, farklı bakış açıları ekle ve konuyu derinleştir."
                analiz_notu = safe_groq(gr_client, prompt2)
                st.markdown(f'<div class="agent-card">{analiz_notu}</div>', unsafe_allow_html=True)

        # 3. AŞAMA: NİHAİ YAZIM (DEĞERLİ GEMINI KOTAMIZ BURAYA SAKLANDI)
        st.divider()
        st.markdown("### ✍️ 3. Baş Editör (Gemini - Nihai Rapor)")
        with st.spinner("Tüm veriler harmanlanıp makale yazılıyor... (Lütfen bekleyin)"):
            prompt3 = f"Sen uzman bir baş yazar ve editörsün. Görev: '{gorev}'.\n\nAraştırmacının Notları: {arastirma_notu}\n\nAnalistin Eklemeleri: {analiz_notu}\n\nBu iki veriyi harmanla. Alt başlıklar, profesyonel bir giriş ve etkili bir sonuç bölümü kullanarak harika bir makale/rapor yaz. Metin akıcı ve ikna edici olmalı."
            nihai_makale = safe_gemini(g_client, prompt3)
            
            st.markdown(f'<div class="article-panel">{nihai_makale}</div>', unsafe_allow_html=True)
            
        st.balloons()
