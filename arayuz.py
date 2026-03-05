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
    
    /* Modern Ofis Arka Planı */
    .stApp { 
        background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), url("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1920&q=80"); 
        background-size: cover; background-attachment: fixed; 
    }
    .main-title { color: #ffffff; text-align: center; font-weight: 800; font-size: 2.5rem; padding: 20px 0; letter-spacing: 1px;}
    
    /* Ajan Çalışma Masaları (Scroll eklendi ki çok uzun yazarlarsa ekran taşmasın) */
    .agent-card { 
        background: rgba(20, 25, 40, 0.85); 
        border-top: 4px solid #00d2ff; 
        border-radius: 10px; 
        padding: 20px; 
        color: #e0f7fa; 
        font-size: 0.9rem; 
        height: 350px; 
        overflow-y: auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Nihai Makale/Kağıt Tasarımı */
    .article-panel { 
        background: rgba(255, 255, 255, 0.95); 
        border-left: 8px solid #2196f3; 
        border-radius: 10px; 
        padding: 40px; 
        color: #1a1a1a; 
        margin-top: 20px; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.6); 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
    }
    
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95) !important; }
    [data-testid="stSidebar"] * { color: white
