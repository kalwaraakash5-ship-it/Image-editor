import streamlit as st
from PIL import Image
import io
import os

st.set_page_config(page_title="Image Editor", page_icon=None, layout="centered")

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

# ── Sidebar: one-time tick image setup ──────────────────
with st.sidebar:
    st.markdown("## Tick Image")
    tick_exists = os.path.exists(TICK_PATH)

    if tick_exists:
        st.markdown(
            '<p style="color:#30d158;font-size:0.82rem;font-weight:500;margin-bottom:0.75rem;">'
            '✓ tick.png is saved</p>',
            unsafe_allow_html=True
        )
        st.image(Image.open(TICK_PATH), width=80)
        st.markdown("<br>", unsafe_allow_html=True)
        replace_file = st.file_uploader(
            "Replace tick image",
            type=["png", "jpg", "jpeg", "webp"],
            key="tick_replace"
        )
        if replace_file:
            img = Image.open(replace_file).convert("RGBA")
            img.save(TICK_PATH, format="PNG")
            st.success("Saved! Refresh the page.")
    else:
        st.markdown(
            '<p style="color:#ff453a;font-size:0.82rem;font-weight:500;margin-bottom:0.75rem;">'
            '✗ No tick.png found</p>',
            unsafe_allow_html=True
        )
        upload_tick = st.file_uploader(
            "Upload tick image",
            type=["png", "jpg", "jpeg", "webp"],
            key="tick_upload"
        )
        if upload_tick:
            img = Image.open(upload_tick).convert("RGBA")
            img.save(TICK_PATH, format="PNG")
            st.success("Saved! Refresh the page.")

# ── Main uploads ─────────────────────────────────────────
base_file   = st.file_uploader("Base Image",   type=["png", "jpg", "jpeg", "webp"])
source_file = st.file_uploader("Source Image", type=["png", "jpg", "jpeg", "webp"])

if base_file and source_file:
    if not os.path.exists(TICK_PATH):
        st.error("tick.png not found in the app folder. Please add it to artifacts/image-editor/ and restart.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Base")
            st.image(Image.open(base_file), width="stretch")
            base_file.seek(0)
        with col2:
            st.caption("Source")
            st.image(Image.open(source_file), width="stretch")
            source_file.seek(0)

        st.divider()

        with st.spinner("Processing…"):
            base   = Image.open(base_file).convert("RGBA").resize((1080, 2400), Image.LANCZOS)
            source = Image.open(source_file).convert("RGBA").resize((1080, 2400), Image.LANCZOS)
            tick   = Image.open(TICK_PATH).convert("RGBA").resize((75, 75), Image.LANCZOS)

            section1 = source.crop((58, 300, 730, 545))
            section2 = source.crop((62, 790, 1021, 1100))

            result = base.copy()
            result.paste(section1, (63, 285), section1)
            result.paste(section2, (63, 715), section2)
            result.paste(tick,     (307, 359), tick)

        st.markdown(
            "<h3 style='color:#f5f5f7;margin-bottom:0.75rem;'>Result</h3>",
            unsafe_allow_html=True
        )
        st.image(result, width="stretch")

        st.markdown("<br>", unsafe_allow_html=True)
        buf = io.BytesIO()
        result.convert("RGB").save(buf, format="JPEG", quality=95)
        st.download_button(
            label="Download Image",
            data=buf.getvalue(),
            file_name="edited_image.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )

else:
    st.markdown("""
    <div style="
        background: #1c1c1e;
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 1rem;
    ">
        <div style="font-size:2.8rem;margin-bottom:1.2rem;filter:grayscale(0.2);">🖼️</div>
        <p style="font-size:1.05rem;font-weight:600;color:#f5f5f7;margin:0 0 0.5rem;">
            Upload two images to begin
        </p>
        <p style="font-size:0.85rem;color:#636366;margin:0;letter-spacing:-0.1px;">
            Base image &nbsp;·&nbsp; Source image
        </p>
    </div>
    """, unsafe_allow_html=True)
