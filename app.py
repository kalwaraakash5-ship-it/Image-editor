import streamlit as st
from PIL import Image
import io
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Image Editor", page_icon=None, layout="centered")

CLARITY_ID = "w28qqjis27"

components.html(f"""
<script type="text/javascript">
(function(c,l,a,r,i,t,y){{
    c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
}})(window, document, "clarity", "script", "{CLARITY_ID}");
</script>
""", height=0)

st.markdown("""
<style>
/* ── Global typography ─────────────────────────────── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "Helvetica Neue", sans-serif;
}

/* ── True black background ─────────────────────────── */
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main {
    background: #000000 !important;
}

/* ── Frosted black header ──────────────────────────── */
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0.75) !important;
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}

/* ── Centered narrow column ────────────────────────── */
.block-container {
    max-width: 680px !important;
    padding-top: 3.5rem !important;
    padding-bottom: 5rem !important;
}

/* ── Headings ──────────────────────────────────────── */
h1 {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.8px !important;
    color: #f5f5f7 !important;
    margin-bottom: 0.2rem !important;
    line-height: 1.1 !important;
}
h2, h3 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #f5f5f7 !important;
    letter-spacing: -0.2px !important;
}
p, label, span {
    color: #98989d !important;
}

/* ── Captions ──────────────────────────────────────── */
[data-testid="stCaptionContainer"] p {
    color: #636366 !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    text-align: center;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

/* ── File uploader card ────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #1c1c1e !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 16px !important;
    padding: 1.1rem 1rem !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(41, 151, 255, 0.5) !important;
}
[data-testid="stFileUploader"] label {
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #f5f5f7 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #636366 !important;
    font-size: 0.78rem !important;
}

/* ── Browse button ─────────────────────────────────── */
[data-testid="stFileUploader"] button {
    background: #2c2c2e !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 980px !important;
    color: #2997ff !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.3rem 1rem !important;
    transition: background 0.15s ease !important;
}
[data-testid="stFileUploader"] button:hover {
    background: #3a3a3c !important;
}

/* ── Download button ───────────────────────────────── */
[data-testid="stDownloadButton"] button {
    background: #2997ff !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 980px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    letter-spacing: -0.1px !important;
    transition: background 0.15s ease, transform 0.1s ease !important;
    box-shadow: 0 0 0 0 transparent !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #3aa3ff !important;
}
[data-testid="stDownloadButton"] button:active {
    background: #1a8ced !important;
    transform: scale(0.98) !important;
}

/* ── Spinner text ──────────────────────────────────── */
[data-testid="stSpinner"] p {
    color: #636366 !important;
    font-size: 0.85rem !important;
}

/* ── Divider ───────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.08) !important;
    margin: 2rem 0 !important;
}

/* ── Images ────────────────────────────────────────── */
[data-testid="stImage"] img {
    border-radius: 12px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.6) !important;
}

/* ── Sidebar ───────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] h2 {
    font-size: 0.95rem !important;
    color: #f5f5f7 !important;
    font-weight: 600 !important;
    letter-spacing: -0.1px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] small {
    color: #636366 !important;
    font-size: 0.8rem !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #1c1c1e !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] label {
    font-size: 0.8rem !important;
    color: #98989d !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #636366 !important;
    font-size: 0.72rem !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: #2c2c2e !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 980px !important;
    color: #2997ff !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    padding: 0.25rem 0.8rem !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: #2c2c2e !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 980px !important;
    color: #f5f5f7 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: background 0.15s ease !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
    background: #3a3a3c !important;
}

/* ── Hide Streamlit chrome ─────────────────────────── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Image Editor</h1>", unsafe_allow_html=True)
st.markdown(
    '<p style="color:#636366;font-size:1rem;margin-top:-0.4rem;margin-bottom:2.5rem;">'
    'Upload your images — we\'ll handle the rest.</p>',
    unsafe_allow_html=True
)

TICK_PATH = os.path.join(os.path.dirname(__file__), "tick.png")

with st.sidebar:
    st.markdown("## Tick Image")
    tick_exists = os.path.exists(TICK_PATH)

    if tick_exists:
        st.markdown('<p style="color:#30d158;">✓ tick.png is saved</p>', unsafe_allow_html=True)
        st.image(Image.open(TICK_PATH), width=80)
    else:
        upload_tick = st.file_uploader("Upload tick image")
        if upload_tick:
            Image.open(upload_tick).convert("RGBA").save(TICK_PATH, "PNG")
            st.rerun()

base_file = st.file_uploader("Base Image", type=["png","jpg","jpeg","webp"])
source_file = st.file_uploader("Source Image", type=["png","jpg","jpeg","webp"])

if base_file and source_file:
    base = Image.open(base_file).convert("RGBA").resize((1080,2400))
    source = Image.open(source_file).convert("RGBA").resize((1080,2400))
    tick = Image.open(TICK_PATH).convert("RGBA").resize((75,75))

    section1 = source.crop((58,300,730,545))
    section2 = source.crop((62,790,1021,1120))

    result = base.copy()
    result.paste(section1,(63,285),section1)
    result.paste(section2,(63,700),section2)
    result.paste(tick,(325,359),tick)

    st.image(result)

    buf = io.BytesIO()
    result.convert("RGB").save(buf, format="JPEG", quality=95)

    st.download_button("Download Image", buf.getvalue(), "edited_image.jpg")

else:
    st.info("Upload two images to begin")
