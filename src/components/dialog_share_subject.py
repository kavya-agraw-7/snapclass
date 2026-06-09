import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    # Auto-detect domain - works locally and when deployed
    try:
        base_url = st.context.url
        # Strip any existing query params
        base_url = base_url.split("?")[0].rstrip("/")
    except:
        base_url = "http://localhost:8501"

    join_url = f"{base_url}/?join_code={subject_code}"

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)
    out.seek(0)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        if st.button('Copy this link to share on Whatsapp or Email', type='primary'):
            st.write(f"`{join_url}`")
            st.toast('Link ready to copy!')

    with col2:
        st.markdown('### Scan to Join')
        st.image(out.getvalue(), caption='QRCODE for class joining')