from openai import OpenAI
import streamlit as st
import os
import base64

st.set_page_config(page_title="Generador de captions con IA", page_icon="📸", layout="centered")

LOGO_URL = "https://raw.githubusercontent.com/EManzur/ai-caption-generator/main/logo.png"  
BANNER_URL = "https://raw.githubusercontent.com/EManzur/ai-caption-generator/main/banner.jpg" 

# Header 

st.markdown("""
    <style>
        .custom-header {
            background-color: white;
            border: solid #ff0092;
            padding: 5px 5px;
            display: flex;
            align-items: center;
            border-radius: 10px;
        }

        .custom-header img {
            height: 100px;
        }

        .custom-header h1 {
            color: #ff0092;
            font-size: 22px;
            margin: 0;
            padding-left: 10px;
        }
    </style>

    <div class="custom-header">
        <img src= "https://raw.githubusercontent.com/EManzur/ai-caption-generator/main/logo.png" alt="Logo" style = "border-radius: 10px;" >
        <h1> Caption Generator </h1>
    </div>
""", unsafe_allow_html=True)


# Mostrar banner de ancho completo
st.markdown(
    f"""
    <div style='margin: 20px auto; text-align: center;'>
        <img src="{BANNER_URL}" alt="Banner" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 10px;"/>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>

        .caption-box {
            background-color: #ff0092;
            border-left: 6px solid #f39c12;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 16px;
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
st.markdown("<h4 style = 'color: black; font-weight: 600' > 📸 Generador de captions con IA </h4>", unsafe_allow_html=True)
st.markdown("<p style = 'color: black;' > Genera 5 captions atractivas con hashtags para tu post de Instagram 💬✨ </p>", 
           unsafe_allow_html=True)

# --- Input fields ---
st.markdown("<p style='color: #34344e; font-weight:200; margin-bottom: -100px'📸 Sube una foto:</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Vista previa de la imagen", use_container_width=True)

st.markdown("<p style='color: #34344e; font-weight:200; margin-bottom: -100px'>🖼️ Describe tu foto:</p>", unsafe_allow_html=True)
description = st.text_input(label="", placeholder="Ej. Foto en la playa al atardecer")

st.markdown("<p style = 'color: #34344e; font-size: 16px; margin-bottom: -1000px' > Elige un tono: </p>", unsafe_allow_html = True)
tone = st.selectbox("", ["Aesthetic 💅", "Divertido 🎉", "Inspirador 🚀", "Negocio 📈", "Romántico 💕", "Picante 🔥"])


def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode()


def picture_instagram_caption(description, tone, base64_image):
    
    prompt = (

    f"""Genera 5 captions cortas y pegadizas para instagram con todo y hashtags.

    Descripcion: {description}
    Tono: {tone}.
    
    Cada caption debe de ser atractiva y optimizada para instagram.
    """)
    
    try:
        completion = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": prompt },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )
        
        text_answer = completion.output_text
        
        return text_answer
        
    except Exception as e:
        
        return f"⚠️ Error generating captions: {e}"

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
                    max_tokens = 800
        )


        text_answer = completion.choices[0].message.content.strip()
    
        return text_answer

    except Exception as e:
        
        return f"⚠️ Error generating captions: {e}"


# --- Button + Output ---
if st.button("✨ Generar Captions"):
    if description and uploaded_file:
        
        with st.spinner("Generando..."):
            
            base64_image = encode_image(uploaded_file)
            captions = picture_instagram_caption(description, tone, base64_image)
        
        st.markdown(
                    '<div style="background-color: #FFFFFF; padding: 15px; border-radius: 10px; '
                    'border-left: 6px solid #ff0092; font-weight: bold; color: #ff0092; margin-top: 5px;">'
                    '✨ ¡Listo! Aquí están tus captions:'
                    '</div>',
                    unsafe_allow_html=True
                    )
        
        #st.success("¡Listo! Aquí están tus captions:")
        #st.markdown('<div class="caption-box">', unsafe_allow_html=True)
        st.markdown(f"```\n{captions}\n```")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif description and not uploaded_file:
        
        with st.spinner("Generando..."):
            captions = text_instagram_caption(description, tone)
        
        st.markdown(
                    '<div style="background-color: #FFFFFF; padding: 15px; border-radius: 10px; '
                    'border-left: 6px solid #ff0092; font-weight: bold; color: #ff0092; margin-top: 5px;">'
                    '✨ ¡Listo! Aquí están tus captions:'
                    '</div>',
                    unsafe_allow_html=True
                    )
        
        #st.success("¡Listo! Aquí están tus captions:")
        #st.markdown('<div class="caption-box">', unsafe_allow_html=True)
        st.markdown(f"```\n{captions}\n```")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif not description and uploaded_file:
        
        with st.spinner("Generando..."):
            
            base64_image = encode_image(uploaded_file)
            captions = picture_instagram_caption(description, tone, base64_image)
        
        st.markdown(
                    '<div style="background-color: #FFFFFF; padding: 15px; border-radius: 10px; '
                    'border-left: 6px solid #ff0092; font-weight: bold; color: #ff0092; margin-top: 5px;">'
                    '✨ ¡Listo! Aquí están tus captions:'
                    '</div>',
                    unsafe_allow_html=True
                    )
        
        #st.success("¡Listo! Aquí están tus captions:")
        #st.markdown('<div class="caption-box">', unsafe_allow_html=True)
        st.markdown(f"```\n{captions}\n```")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.warning("Por favor ingresa una descripción o foto.")

# --- Footer ---
st.markdown("<hr style='margin-top: 50px; border: none; height: 1px; background-color: #34344e;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: #34344e;'>"
    "✨ Captions generadas con IA (by OpenAI)"
    "</p>",
    unsafe_allow_html=True
)
