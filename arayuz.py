import streamlit as st
from google import genai
from groq import Groq
import time
import requests
from bs4 import BeautifulSoup

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Otonom AI Ajansı", page_icon="🏢", layout="wide")

# --- GELİŞMİŞ CSS TASARIMI ---
st.markdown("""
    <style>
    footer {visibility: hidden !important;}
    .stApp { background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), url("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1920&q=80"); background-size: cover; background-attachment: fixed; }
    .main-title { color: #ffffff; text-align: center; font-weight: 800; font-size: 2.5rem; padding: 20px 0; }
    .agent-card { background: rgba(20, 25, 40, 0.85); border-top: 4px solid #00d2ff; border-radius: 10px; padding: 20px; color: #e0f7fa; font-size: 0.9rem; height: 350px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5);}
    .article-panel { background: rgba(255, 255, 255, 0.95); border-left: 8px solid #2196f3; border-radius: 10px; padding: 40px; color: #1a1a1a; margin-top: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.6); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6;}
    
    /* Yeni Twitter (X) Kutusu Tasarımı */
    .twitter-panel { background: rgba(15, 20, 25, 0.95); border: 1px solid #1DA1F2; border-radius: 15px; padding: 30px; color: #ffffff; margin-top: 20px; box-shadow: 0 10px 30px rgba(29, 161, 242, 0.2); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;}
    .tweet-divider { border-bottom: 1px solid #38444d; margin: 15px 0;}
    .image-prompt { color: #1DA1F2; font-size: 0.85rem; font-style: italic; margin-top: 5px;}
    
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🏢 YENİ NESİL OTONOM AJANS</h1>', unsafe_allow_html=True)

# --- SOL MENÜ ---
with st.sidebar:
    st.header("🔑 Güvenlik")
    gemini_key = st.text_input("Gemini API (Baş Editör):", type="password")
    groq_key = st.text_input("Groq API (Araştırma & Sosyal Medya):", type="password")
    
# --- KONTROL PANELİ ---
st.markdown("### 🎛️ Görev ve Özellikler")
col1, col2 = st.columns([2, 1])

with col1:
    gorev = st.text_area("🎯 İş Emri (Ne araştıralım/yazalım?):", value="Yapay zeka araçları dijital pazarlamayı nasıl değiştiriyor?", height=120)

with col2:
    url_input = st.text_input("🔗 Canlı URL Ekle (Opsiyonel):", placeholder="https://ornek-haber-sitesi.com")
    vibe_degeri = st.slider("🎭 Üslup ve Ton (Vibe Slider)", min_value=0, max_value=100, value=50, help="0: Çok ciddi/Akademik | 50: Profesyonel | 100: YouTuber/Eğlenceli")

baslat = st.button("🚀 AJANSI VE SOSYAL MEDYA EKİBİNİ ÇALIŞTIR", use_container_width=True)

# Üslup Belirleyici
if vibe_degeri < 30:
    vibe_metni = "Çok ciddi, akademik, veriye dayalı ve resmi bir üslup."
elif vibe_degeri < 70:
    vibe_metni = "Profesyonel, akıcı, modern ve okuması keyifli bir üslup."
else:
    vibe_metni = "Çok enerjik, samimi, esprili, bol emojili, bir Youtuber veya yakın arkadaş gibi bir üslup."

# Canlı URL Okuma Fonksiyonu
def url_oku(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Sitedeki tüm paragrafları çeker (Kelime sınırını aşmamak için ilk 4000 karakteri alır)
        metin = ' '.join([p.text for p in soup.find_all('p')])
        return metin[:4000] if metin else "URL'de okunabilir metin bulunamadı."
    except Exception as e:
        return f"URL Okuma Hatası: {e}"

# Güvenli İstek Fonksiyonları
def safe_gemini(client, prompt):
    time.sleep(2) 
    try:
        return client.models.generate_content(model='gemini-2.5-flash', contents=prompt).text
    except Exception as e:
        return f"⚠️ Gemini Hatası: {str(e)}"

def safe_groq(client, prompt):
    try:
        resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model='llama-3.3-70b-versatile')
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Llama Hatası: {str(e)}"

if baslat:
    if not gemini_key or not groq_key: 
        st.error("⚠️ Lütfen sol menüden API şifrelerinizi girin!")
    else:
        g_client = genai.Client(api_key=gemini_key.strip())
        gr_client = Groq(api_key=groq_key.strip())

        st.success("✅ Ekip iş başında! Lütfen ajanların işini bitirmesini bekleyin...")

        # --- CANLI URL KONTROLÜ ---
        ek_veri = ""
        if url_input:
            with st.spinner("🌐 Canlı web sitesi taranıyor..."):
                web_metni = url_oku(url_input)
                ek_veri = f"\n\nKullanıcının verdiği canlı internet sitesinden çekilen güncel veri şudur: {web_metni}"

        col_a, col_b = st.columns(2)
        
        # 1. AŞAMA: ARAŞTIRMA
        with col_a:
            st.markdown("### 🔍 1. Araştırmacı (Llama 3)")
            prompt1 = f"Görev: '{gorev}'. {ek_veri} Bu verileri kullanarak derinlemesine bir araştırma yap. İstenilen Üslup: {vibe_metni}."
            arastirma_notu = safe_groq(gr_client, prompt1)
            st.markdown(f'<div class="agent-card">{arastirma_notu}</div>', unsafe_allow_html=True)
                
        # 2. AŞAMA: ANALİZ
        with col_b:
            st.markdown("### 🧠 2. Analist (Llama 3)")
            prompt2 = f"Görev: '{gorev}'. Araştırma verileri: '{arastirma_notu}'. Bu verilere farklı bir bakış açısı ekle. İstenilen Üslup: {vibe_metni}."
            analiz_notu = safe_groq(gr_client, prompt2)
            st.markdown(f'<div class="agent-card">{analiz_notu}</div>', unsafe_allow_html=True)

        # 3. AŞAMA: NİHAİ MAKALE
        st.divider()
        st.markdown("### ✍️ 3. Baş Editör (Gemini)")
        prompt3 = f"Görev: '{gorev}'. Araştırma: {arastirma_notu}. Analiz: {analiz_notu}. Bu verileri harmanlayarak bir makale yaz. DİKKAT EDİLECEK ÜSLUP: {vibe_metni}."
        
        try:
            time.sleep(2)
            nihai_makale = g_client.models.generate_content(model='gemini-2.5-flash', contents=prompt3).text
        except:
            nihai_makale = safe_groq(gr_client, prompt3) # Gemini hata verirse Llama devralır
            
        st.markdown(f'<div class="article-panel">{nihai_makale}</div>', unsafe_allow_html=True)

        # 4. AŞAMA: TWITTER (X) SOSYAL MEDYA UZMANI
        st.divider()
        st.markdown("### 🐦 4. Sosyal Medya Uzmanı (X Flood)")
        with st.spinner("Makale Twitter formatına dönüştürülüyor..."):
            prompt4 = f"""
            Şu makaleyi bir Twitter (X) flood'una (dizisine) dönüştür. 
            Makale: {nihai_makale}
            KURALLAR (ÇOK ÖNEMLİ):
            1) Flood tarzında olacak. Üslup: {vibe_metni}
            2) Her bir tweet KESİNLİKLE 280 karakteri geçmeyecek.
            3) Okuyucunun devamını okuması için SON TWEET HARİÇ her tweetin sonuna '++' işareti koy.
            4) Her tweet metninin hemen altına, o tweet ile paylaşılabilecek yapay zeka ile üretilmeye uygun İngilizce bir görsel promptu (fikri) yaz. (Örnek format: [Image Idea: A futuristic robot typing on a laptop, cinematic lighting])
            """
            twitter_flood = safe_groq(gr_client, prompt4)
            
            # Twitter şıklığı için tasarlandı
            st.markdown(f"""
                <div class="twitter-panel">
                    <h4 style='color: #1DA1F2; margin-bottom: 20px;'>📱 Yayına Hazır Twitter Dizisi</h4>
                    {twitter_flood.replace('++', '++<br><hr class="tweet-divider">')}
                </div>
                """, unsafe_allow_html=True)
            
        st.balloons()
