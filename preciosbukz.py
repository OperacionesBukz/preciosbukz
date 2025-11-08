import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")

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
    url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE}/admin/api/2024-10/variants.json?sku={sku}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("variants", [])
        if data:
            variant = data[0]
            product_id = variant["product_id"]
            product_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE}/admin/api/2024-10/products/{product_id}.json"
            product_resp = requests.get(product_url)
            product_title = None
            if product_resp.status_code == 200:
                product_title = product_resp.json().get("product", {}).get("title")

            return {
                "title": product_title,
                "sku": variant["sku"],
                "price": variant["price"],
            }
    return None

if isbn:
    with st.spinner("Consultando en Shopify..."):
        result = get_variant_by_sku(isbn.strip())

    if result:
        st.success("✅ Libro encontrado")
        st.markdown(f"<div class='title'>{result['title']}</div>", unsafe_allow_html=True)
        st.write(f"**ISBN:** {result['sku']}")
        st.markdown(f"<div class='price'>$ {result['price']}</div>", unsafe_allow_html=True)
    else:
        st.error("No se encontró ningún libro con ese ISBN en Shopify.")
