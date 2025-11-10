import streamlit as st
import requests

SHOPIFY_ACCESS_TOKEN = st.secrets["SHOPIFY_API_KEY"]
SHOPIFY_STORE = st.secrets["SHOPIFY_STORE"]

st.set_page_config(page_title="Consulta de precios Bukz", page_icon="📚", layout="centered")

st.title("📚 Consulta de precios Bukz")
st.write("Escanea el ISBN del libro para ver el nombre y precio.")

# Botón para limpiar el campo (simula 'enfocar de nuevo')
if st.button("🆕 Nuevo ISBN / Escanear otro"):
    st.session_state["isbn_input"] = ""

isbn = st.text_input(
    "Escanee o escriba el ISBN:",
    key="isbn_input",
    placeholder="Ejemplo: 9781234567890",
    label_visibility="collapsed"
)

def get_variant_by_sku(sku):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }

    query = f"""
    {{
      productVariants(first: 1, query: "sku:{sku}") {{
        edges {{
          node {{
            id
            sku
            price
            product {{
              title
            }}
          }}
        }}
      }}
    }}
    """

    url = f"https://{SHOPIFY_STORE}/admin/api/2024-10/graphql.json"
    response = requests.post(url, json={"query": query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        edges = data.get("data", {}).get("productVariants", {}).get("edges", [])
        if edges:
            node = edges[0]["node"]
            return {
                "title": node["product"]["title"],
                "sku": node["sku"],
                "price": node["price"],
            }
    return None

if isbn:
    with st.spinner("Consultando en Shopify..."):
        result = get_variant_by_sku(isbn.strip())

    if result:
        st.success("✅ Libro encontrado")
        st.markdown(f"**{result['title']}**")
        st.write(f"**ISBN:** {result['sku']}")
        st.markdown(f"### 💲${result['price']}")
    else:
        st.error("No se encontró ningún libro con ese ISBN.")
