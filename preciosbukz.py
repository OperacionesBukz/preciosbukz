import streamlit as st
import requests

# 🔒 Leer credenciales desde Streamlit Secrets
SHOPIFY_ACCESS_TOKEN = st.secrets["SHOPIFY_API_KEY"]
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

# ✅ Función para buscar el SKU (ISBN) en Shopify
def get_variant_by_sku(sku):
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    # Traemos varias variantes por página para buscar manualmente
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-10/variants.json?limit=250"
    variants = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break
        data = response.json()
        variants.extend(data.get("variants", []))
        # Revisa si hay siguiente página (paginación)
        url = response.links.get("next", {}).get("url")

    # 🔍 Buscar coincidencia exacta en todas las variantes
    variant = next((v for v in variants if str(v["sku"]).strip() == str(sku).strip()), None)

    if variant:
        product_id = variant["product_id"]
        product_url = f"https://{SHOPIFY_STORE}/admin/api/2024-10/products/{product_id}.json"
        product_resp = requests.get(product_url, headers=headers)

        product_title = None
        if product_resp.status_code == 200:
            product_title = product_resp.json().get("product", {}).get("title")

        return {
            "title": product_title,
            "sku": variant["sku"],
            "price": variant["price"],
        }

    return None

# ✅ Si el usuario ingresa un ISBN, ejecutar la búsqueda
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
