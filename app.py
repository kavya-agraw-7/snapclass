# import streamlit as st

# # DEBUG - Check if secrets are loading
# st.write("URL:", st.secrets["SUPABASE_URL"])
# st.write("KEY exists:", bool(st.secrets["SUPABASE_KEY"]))
# st.stop()  # This stops execution here so you only see the debug info

import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.components.dialog_enroll import enroll_dialog
from src.database.config import check_supabase_connection


def main():
    st.set_page_config(
        page_title='SnapClass-Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )
    # Verify database connection
    is_connected, error_title, error_desc = check_supabase_connection()
    if not is_connected:
        st.title("SnapClass Database Status")
        st.error(f"### {error_title}\n\n{error_desc}", icon="🚨")
        st.info(
            "💡 **How to resolve this:**\n\n"
            "1. Make sure PocketBase is running: `cd pocketbase` and `.\\pocketbase.exe serve`\n"
            "2. Open Admin UI at http://127.0.0.1:8090/_/\n"
            "3. For each collection, set API Rules: List rule = `1 = 1`, View rule = `1 = 1`\n"
            "4. Refresh this page.",
            icon="ℹ️"
        )
        st.stop()
    
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

    join_code = st.query_params.get('join_code')
    if join_code:
        if st.session_state['login_type'] != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            enroll_dialog(join_code)


if __name__ == "__main__":
    main()