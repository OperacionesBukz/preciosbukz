import streamlit as st
import requests

# 🔒 Leer credenciales desde Streamlit Secrets
SHOPIFY_ACCESS_TOKEN = st.secrets["SHOPIFY_ACCESS_TOKEN"]
SHOPIFY_STORE = st.secrets["SHOPIFY_STORE"]

st.set_page_config(page_title="Consulta de precios Bukz", page_icon="📚", layout="centered")

st.markdown("""
    <style>
    .price {
        font-size: 2em;
        color: #008000;
        font-weight: bold;
    }
    .title {
        font-size: 1.3em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Consulta de precios Bukz")
st.write("Escanea el ISBN del libro para ver el nombre y precio.")

isbn = st.text_input("Escanee o escriba el ISBN:", "", placeholder="Ejemplo: 9781234567890")

def get_variant_by_sku(sku):
