from openai import OpenAI
import streamlit as st
import os

st.set_page_config(page_title="Generador de captions con IA", page_icon="📸", layout="centered")

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #fefefe !important;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h4 {
            color: #2c3e50;
            text-align: center;
        }

        .stTextInput > div > input,
        .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: #2c3e50 !important;
            border-radius: 8px;
            padding: 10px;
        }

        .stButton>button {
            background-color: #ff6f61;
            color: white;
            padding: 0.75em 1.5em;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 16px;
        }

        .stButton>button:hover {
            background-color: #e04e41;
        }

        .caption-card {
            background-color: #fdf6e3;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

my_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = my_api_key)

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown("""
    <style>
        body {
            background-color: #fdf6e3;
        }
        .reportview-container {
            background: #fdf6e3;
        }
        header {
            background-color: #2c3e50;
            padding: 20px 0;
            text-align: center;
            color: white;
            font-size: 30px;
            font-weight: bold;
        }
        label, .stTextInput label, .stSelectbox label, .stMarkdown p {
            color: #2c3e50 !important;
            font-weight: 500;
        }
        .stTextInput > div > input,
        .stSelectbox > div > div {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
        }
        .stButton>button {
            background-color: #2c3e50;
            color: white;
            border: none;
            padding: 0.5em 1em;
            font-weight: bold;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #1a252f;
        }
        .caption-box {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-top: 20px;
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

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
                    'border-left: 6px solid #f1c40f; font-weight: bold; color: #2c3e50; margin-top: 20px;">'
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
st.markdown("<hr style='margin-top: 50px; border: none; height: 1px; background-color: #FFFFFF;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray;'>"
    "✨ Captions generadas con IA (by OpenAI)"
    "</p>",
    unsafe_allow_html=True
)
