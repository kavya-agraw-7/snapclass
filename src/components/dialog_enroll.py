import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code to enroll in a subject')
    default_code = st.session_state.get('auto_join_code', '')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')
    if st.button('Enroll', type='primary', width='stretch'):
        if join_code:
            try:
                res = supabase.collection("subjects").get_list(1, 1, {
                    "filter": f'subject_code="{join_code}"'
                })
                if res.items:
                    subject = res.items[0]
                    student_id = st.session_state.student_data['student_id']
                    
                    # Check if already enrolled
                    check = supabase.collection("subject_students").get_list(1, 1, {
                        "filter": f'subject_id="{subject.id}" && student_id="{student_id}"'
                    })
                    
                    if check.items:
                        st.warning('You are already enrolled in this subject')
                    else:
                        enroll_student_to_subject(student_id, subject.id)
                        st.success(f'Enrolled in {subject.name} successfully!')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning('Subject code not found!')
            except Exception as e:
                st.error(f'Error: {e}')
        else:
            st.warning('Please enter a valid subject code')