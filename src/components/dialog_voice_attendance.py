import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.db import get_enrolled_students_for_subject
from src.components.dialog_attendance_results import show_attendance_result
from datetime import datetime
import pandas as pd


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write('Record audio of students saying "I am present". AI will recognise each voice.')

    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyse Audio', width='stretch', type='primary'):
        if not audio_data:
            st.warning('Please record audio first!')
            return

        with st.spinner('Processing Audio...'):
            enrolled_students = get_enrolled_students_for_subject(selected_subject_id)

            if not enrolled_students:
                st.warning('No students enrolled in this course')
                return

            # Build candidates dict — only students with voice embeddings
            candidates_dict = {
                s['student_id']: s['voice_embedding']
                for s in enrolled_students
                if s.get('voice_embedding')
            }

            if not candidates_dict:
                st.error('No enrolled students have voice profiles registered')
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results = []
            attendance_to_log = []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for student in enrolled_students:
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = score > 0

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Score": f"{score:.2f}" if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)