import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.database.config import check_supabase_connection


def main():
    st.set_page_config(
        page_title='SnapClass-Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )

    is_connected, error_title, error_desc = check_supabase_connection()
    if not is_connected:
        st.title("SnapClass Database Status")
        st.error(f"### {error_title}\n\n{error_desc}", icon="🚨")
        st.info(
            "💡 **How to resolve this:**\n\n"
            "1. Make sure PocketBase is running\n"
            "2. Check your POCKETBASE_URL secret is set correctly\n"
            "3. Refresh this page.",
            icon="ℹ️"
        )
        st.stop()

    # Handle QR code join link
    join_code = st.query_params.get('join_code')
    if join_code:
        st.session_state['auto_join_code'] = join_code
        if st.session_state.get('login_type') != 'student':
            st.session_state['login_type'] = 'student'
            st.rerun()

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()


if __name__ == "__main__":
    main()