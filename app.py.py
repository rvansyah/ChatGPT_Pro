import streamlit as st
from modules.chat_manager import ChatManager
from modules.vision import image_to_text
from modules.ai_model import query_ai
from PIL import Image
import io

st.set_page_config(page_title="ChatGPT Pro", layout="wide", page_icon="🤖")

with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/3369400?v=4", width=80)
    st.markdown("### [moh irvansyah]")
    st.markdown("**ChatGPT Pro (Gratis)**")
    st.divider()
    st.markdown("#### ⚙️ Pengaturan (dummy)")
    st.checkbox("Mode Gelap", value=False, disabled=True)
    st.checkbox("Multi-turn Chat", value=True, disabled=True)
    st.markdown("---")
    st.markdown("Made with ❤️ [GitHub](https://github.com/rvansyah)")

if "chat" not in st.session_state:
    st.session_state.chat = ChatManager()

st.title("🤖 ChatGPT Pro Gratis & Canggih")

for msg in st.session_state.chat.history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
            if msg.get("image"):
                st.image(msg["image"], width=200)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"], unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([5, 2])
    with cols[0]:
        prompt = st.text_area("Ketik...", key="prompt", height=80, max_chars=1000)
    with cols[1]:
        image_file = st.file_uploader("Upload gambar (opsional)", type=["jpg", "jpeg", "png"], key="image")
    submitted = st.form_submit_button("Kirim 🚀")

if submitted and (prompt or image_file):
    image_bytes = None
    image_caption = ""
    if image_file:
        image = Image.open(image_file)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        image_bytes = buf.read()
        image_caption = image_to_text(image)
    full_prompt = prompt
    if image_caption:
        full_prompt += f"\n[Gambar: {image_caption}]"
    st.session_state.chat.add_user_message(prompt, image_bytes)
    ai_reply = query_ai(full_prompt, st.session_state.chat.history)
    st.session_state.chat.add_ai_message(ai_reply)
    st.experimental_rerun()