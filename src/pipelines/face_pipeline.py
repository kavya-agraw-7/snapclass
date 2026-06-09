import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)
    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))
    return encodings


def predict_face_login(image_np):
    """For single-face login — returns (student_id, message) or (None, reason)"""
    encodings = get_face_embeddings(image_np)

    if not encodings:
        return None, "No face detected"

    encoding = encodings[0]  # Take first face for login

    # Always fetch fresh from DB (no cache) so newly registered students work
    student_db = get_all_students()

    if not student_db:
        return None, "No students registered"

    best_match_id = None
    best_match_name = ""
    best_distance = float('inf')
    THRESHOLD = 0.6

    for student in student_db:
        emb = student.get('face_embedding')
        if not emb:
            continue

        emb_np = np.array(emb)

        # Skip if shape doesn't match (corrupted embedding)
        if emb_np.shape != encoding.shape:
            print(f"[FaceLogin] Shape mismatch for {student.get('name')}: "
                  f"{emb_np.shape} vs {encoding.shape}")
            continue

        dist = np.linalg.norm(emb_np - encoding)
        print(f"[FaceLogin] Distance to {student.get('name')}: {dist:.4f}")

        if dist < best_distance:
            best_distance = dist
            best_match_id = student['student_id']
            best_match_name = student.get('name', '')

    if best_distance <= THRESHOLD:
        return best_match_id, f"Matched: {best_match_name} (dist={best_distance:.3f})"
    else:
        return None, f"No match found (closest dist={best_distance:.3f}, threshold={THRESHOLD})"


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding and len(embedding) > 0:
            if isinstance(embedding, list):
                embedding = np.array(embedding)
            X.append(embedding)
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None

    if len(X) == 1:
        return {'clf': None, 'X': X, 'y': y, 'single': True}

    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
        return {'clf': clf, 'X': X, 'y': y, 'single': False}
    except ValueError as e:
        print(f"Training error: {e}")
        return None


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}
    num_faces = len(encodings)

    if num_faces == 0:
        return detected_student, [], num_faces

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], num_faces

    X_train = model_data['X']
    y_train = model_data['y']
    all_students = sorted(list(set(y_train)))

    # Handle single student case
    if model_data.get('single', False):
        for encoding in encodings:
            student_embedding = X_train[0]
            best_match_score = np.linalg.norm(student_embedding - encoding)
            resemblance_threshold = 0.6
            if best_match_score <= resemblance_threshold:
                detected_student[y_train[0]] = True
        return detected_student, all_students, num_faces

    # Multiple students case
    clf = model_data['clf']

    for encoding in encodings:
     if len(all_students) >= 2:
        predicted_id = clf.predict([encoding])[0]
     else:
        predicted_id = all_students[0]

     try:
        index = y_train.index(predicted_id)
        student_embedding = X_train[index]
        best_match_score = np.linalg.norm(student_embedding - encoding)
        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            # ✅ Only update if this detection is more confident than previous
            if predicted_id not in detected_student or best_match_score < detected_student[predicted_id]:
                detected_student[predicted_id] = best_match_score
     except ValueError:
        continue

    return detected_student, all_students, num_faces