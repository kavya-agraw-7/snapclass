import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject", )
def create_subject_dialog(teacher_id):
    st.write("enter subject details")
    sub_name = st.text_input("Subject Name",placeholder="eg: Mathematics")
    sub_id= st.text_input("Subject Code",placeholder="eg: MATH101")
    sub_section= st.text_input("Section",placeholder="eg: A")

    if st.button("Create Subject Now",type='primary',width='stretch'):
        if sub_name and sub_id and sub_section:
            try:#kuch bhi fail hoskta ho to usko try except block me rakhna chahiye
                create_subject(sub_name, sub_id, sub_section, teacher_id)
                st.toast("Subject created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {str(e)}")
        else:
            st.warning("Please fill in all the fields to create a subject.")            

                