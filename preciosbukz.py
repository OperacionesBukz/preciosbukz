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

# Campo de texto normal
isbn = st.text_input("Escanee o escriba el ISBN:", "", placeholder="Ejemplo: 9781234567890", key="isbn_input")

# Botón para enfocar el campo
focus_button = st.button("📘 Ubicar cursor en el campo")

if focus_button:
    st.markdown(
        """
        <script>
        const input = window.document.querySelector('input[id^="isbn_input"]');
        if (input) {
            input.focus();
            input.select();
        }
        </script>
        """,
        unsafe_allow_html=True
    )

# ✅ Función para buscar el SKU (ISBN) en Shopify
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
    else:
        st.error(f"Error al consultar Shopify: {response.status_code}")
        st.write(response.text)

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

