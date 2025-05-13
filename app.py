from openai import OpenAI
import streamlit as st
import os

st.set_page_config(page_title="Generador de captions con IA", page_icon="📸", layout="centered")

LOGO_URL = "https://raw.githubusercontent.com/EManzur/ai-caption-generator/main/logo.png"  # Cambia esta por tu URL real
BANNER_URL = "https://raw.githubusercontent.com/EManzur/ai-caption-generator/main/banner.jpg"  # Cambia esta también

# Mostrar logo centrado arriba
st.markdown(
    f"""
    <div style='text-align: center; margin-top: 10px;'>
        <img src="{LOGO_URL}" alt="Logo" style="width: 150px;"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Mostrar banner de ancho completo
st.markdown(
    f"""
    <div style='margin: 20px auto; text-align: center;'>
        <img src="{BANNER_URL}" alt="Banner" style="width: 100%; max-height: 250px; object-fit: cover; border-radius: 10px;"/>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        body {
            background-color: #bc9cc4;
        }

        .block-container {
            padding-top: 2rem;
        }

        h1 {
            text-align: center;
            color: ##3a1367;
        }

        .main-header {
            background-color: #e30e63;
            padding: 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
            font-size: 32px;
            font-weight: 700;
        }

        .input-area {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }

        .caption-box {
            background-color: #fff6e8;
            padding: 20px;
            border-left: 6px solid #f39c12;
            border-radius: 10px;
            margin-top: 20px;
            color: #333;
            font-size: 16px;
            font-family: "Segoe UI", sans-serif;
        }

        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 180px;
            margin-bottom: 20px;
        }

        .footer {
            text-align: center;
            font-size: 12px;
            color: gray;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

my_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = my_api_key)

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Header ---
st.markdown("<header>📸 Generador de captions con IA</header>", unsafe_allow_html=True)
st.markdown("#### Genera 5 captions atractivas con hashtags para tu post de Instagram 💬✨")

# --- Input fields ---
description = st.text_input("Describe tu foto o idea:")
tone = st.selectbox("Elige un tono", ["Aesthetic 💅", "Divertido 🎉", "Inspirador 🚀", "Negocio 📈", "Romántico 💕", "Picante 🔥"])

def text_instagram_caption(description, tone):
    
    prompt = (

    f"""Genera 5 captions cortas y pegadizas para instagram con todo y hashtags.

    Descripcion: {description}
    Tono: {tone}.
    
    Cada caption debe de ser atractiva y optimizada para instagram.
    """)

    try:
        completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                                    {"role": "user",
                                     "content": prompt}
                                ],
                    temperature = 0.9,
                    max_tokens = 400
        )


        text_answer = completion.choices[0].message.content.strip()
    
        return text_answer

    except Exception as e:
        
        return f"⚠️ Error generating captions: {e}"


# --- Button + Output ---
if st.button("✨ Generar Captions"):
    if description:
        with st.spinner("Generando..."):
            captions = text_instagram_caption(description, tone)
        st.markdown(
                    '<div style="background-color: #FFFFFF; padding: 15px; border-radius: 10px; '
                    'border-left: 6px solid #dc6378; font-weight: bold; color: #f1c694; margin-top: 20px;">'
                    '✨ ¡Listo! Aquí están tus captions:'
                    '</div>',
                    unsafe_allow_html=True
                    )    
        #st.success("¡Listo! Aquí están tus captions:")
        st.markdown('<div class="caption-box">', unsafe_allow_html=True)
        st.markdown(f"```\n{captions}\n```")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Por favor ingresa una descripción.")

# --- Footer ---
st.markdown("<hr style='margin-top: 50px; border: none; height: 1px; background-color: #edeccf;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: #101652;'>"
    "✨ Captions generadas con IA (by OpenAI)"
    "</p>",
    unsafe_allow_html=True
)
