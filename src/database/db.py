from src.database.config import supabase
import bcrypt
from datetime import datetime


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    try:
        result = supabase.collection("teachers").get_list(1, 1, {"filter": f'username="{username}"'})
        return len(result.items) > 0
    except Exception as e:
        print(f"Error checking teacher: {e}")
        return False

def create_teacher(username, password, name):
    try:
        data = {
            "username": username,
            "password_hash": hash_pass(password),
            "name": name,
            "role": "teacher"
        }
        result = supabase.collection("teachers").create(data)
        return [{"id": result.id, "username": result.username, "name": result.name}]
    except Exception as e:
        print(f"Error creating teacher: {e}")
        return None

def teacher_login(username, password):
    try:
        result = supabase.collection("teachers").get_list(1, 1, {"filter": f'username="{username}"'})
        if len(result.items) > 0:
            teacher = result.items[0]
            stored_hash = teacher.password_hash if hasattr(teacher, 'password_hash') else ""
            if check_pass(password, stored_hash):
                return {
                    "teacher_id": teacher.id,
                    "username": teacher.username,
                    "name": teacher.name,
                    "role": teacher.role if hasattr(teacher, 'role') else "teacher"
                }
        return None
    except Exception as e:
        print(f"Error in teacher_login: {e}")
        return None


def get_all_students():
    try:
        result = supabase.collection("students").get_list(1, 500)
        students = []
        for item in result.items:
            face_emb = item.face_encoding if hasattr(item, 'face_encoding') else None
            if face_emb and isinstance(face_emb, str):
                try:
                    face_emb = [float(x.strip()) for x in face_emb.strip('[]').split(',') if x.strip()]
                except:
                    face_emb = None

            voice_emb = item.voice_encoding if hasattr(item, 'voice_encoding') else None
            if voice_emb and isinstance(voice_emb, str):
                try:
                    voice_emb = [float(x.strip()) for x in voice_emb.strip('[]').split(',') if x.strip()]
                except:
                    voice_emb = None

            students.append({
                "student_id": item.id,
                "name": item.name if hasattr(item, 'name') else "",
                "face_embedding": face_emb,
                "voice_embedding": voice_emb
            })
        return students
    except Exception as e:
        print(f"Error getting students: {e}")
        return []

def create_student(new_name, face_embedding=None, voice_embedding=None):
    try:
        data = {
            "name": new_name,
            "face_encoding": str(face_embedding) if face_embedding else "",
            "voice_encoding": str(voice_embedding) if voice_embedding else ""
        }
        result = supabase.collection("students").create(data)
        return [{
            "student_id": result.id,
            "name": result.name,
            "face_embedding": face_embedding,
            "voice_embedding": voice_embedding
        }]
    except Exception as e:
        print(f"Error creating student: {e}")
        return None


def create_subject(subject_code, name, section, teacher_id):
    try:
        data = {
            "subject_code": subject_code,
            "name": name,
            "section": section,
            "teacher_id": teacher_id,
            "total_students": 0,
            "total_classes": 0
        }
        result = supabase.collection("subjects").create(data)
        return [{"subject_id": result.id, "subject_code": result.subject_code, "name": result.name}]
    except Exception as e:
        print(f"Error creating subject: {e}")
        return None

def get_teacher_subjects(teacher_id):
    try:
        result = supabase.collection("subjects").get_list(1, 100, {"filter": f'teacher_id="{teacher_id}"'})
        subjects = []
        for item in result.items:
            try:
                students_result = supabase.collection("subject_students").get_list(1, 500, {
                    "filter": f'subject_id="{item.id}"'
                })
                total_students = len(students_result.items)
            except:
                total_students = 0

            try:
                attendance = supabase.collection("attendance").get_list(1, 500, {
                    "filter": f'subject_id="{item.id}"'
                })
                unique_sessions = len(set(
                    a.timestamp.split("T")[0] if hasattr(a, 'timestamp') and a.timestamp else ""
                    for a in attendance.items
                ))
            except:
                unique_sessions = 0

            subjects.append({
                "subject_id": item.id,
                "subject_code": item.subject_code if hasattr(item, 'subject_code') else "",
                "name": item.name if hasattr(item, 'name') else "",
                "section": item.section if hasattr(item, 'section') else "",
                "total_students": total_students,
                "total_classes": unique_sessions
            })
        return subjects
    except Exception as e:
        print(f"Error getting teacher subjects: {e}")
        return []


def enroll_student_to_subject(student_id, subject_id):
    try:
        check = supabase.collection("subject_students").get_list(1, 1, {
            "filter": f'student_id="{student_id}" && subject_id="{subject_id}"'
        })
        if len(check.items) > 0:
            return None

        data = {"student_id": student_id, "subject_id": subject_id}
        result = supabase.collection("subject_students").create(data)

        try:
            subject = supabase.collection("subjects").get_one(subject_id)
            current = subject.total_students if hasattr(subject, 'total_students') else 0
            supabase.collection("subjects").update(subject_id, {"total_students": current + 1})
        except:
            pass

        return [{"id": result.id}]
    except Exception as e:
        print(f"Error enrolling student: {e}")
        return None


def unenroll_student_to_subject(student_id, subject_id):
    try:
        result = supabase.collection("subject_students").get_list(1, 1, {
            "filter": f'student_id="{student_id}" && subject_id="{subject_id}"'
        })
        if len(result.items) > 0:
            supabase.collection("subject_students").delete(result.items[0].id)

            try:
                subject = supabase.collection("subjects").get_one(subject_id)
                current = subject.total_students if hasattr(subject, 'total_students') else 0
                supabase.collection("subjects").update(subject_id, {"total_students": max(0, current - 1)})
            except:
                pass

            return [{"id": result.items[0].id}]
        return None
    except Exception as e:
        print(f"Error unenrolling student: {e}")
        return None


def get_student_subjects(student_id):
    try:
        enrollments = supabase.collection("subject_students").get_list(1, 100, {
            "filter": f'student_id="{student_id}"'
        })

        results = []
        for enrollment in enrollments.items:
            try:
                subject = supabase.collection("subjects").get_one(enrollment.subject_id)
                results.append({
                    "subjects": {
                        "subject_id": subject.id,
                        "subject_code": subject.subject_code if hasattr(subject, 'subject_code') else "",
                        "name": subject.name if hasattr(subject, 'name') else "",
                        "section": subject.section if hasattr(subject, 'section') else ""
                    }
                })
            except Exception as ex:
                print(f"Error fetching subject {enrollment.subject_id}: {ex}")
                continue
        return results
    except Exception as e:
        print(f"Error getting student subjects: {e}")
        return []


def get_student_attendance(student_id):
    try:
        result = supabase.collection("attendance").get_list(1, 500, {
            "filter": f'student_id="{student_id}"'
        })

        logs = []
        for item in result.items:
            subject_name = ""
            subject_code = ""
            try:
                subject = supabase.collection("subjects").get_one(item.subject_id)
                subject_name = subject.name if hasattr(subject, 'name') else ""
                subject_code = subject.subject_code if hasattr(subject, 'subject_code') else ""
            except:
                pass

            logs.append({
                "subject_id": item.subject_id,
                "is_present": item.is_present if hasattr(item, 'is_present') else False,
                "timestamp": str(item.timestamp) if hasattr(item, 'timestamp') else "",
                "subjects": {
                    "name": subject_name,
                    "subject_code": subject_code
                }
            })
        return logs
    except Exception as e:
        print(f"Error getting student attendance: {e}")
        return []


def create_attendance(logs):
    try:
        for log in logs:
            data = {
                "student_id": log.get("student_id"),
                "subject_id": log.get("subject_id"),
                "timestamp": log.get("timestamp", datetime.now().isoformat()),
                "is_present": log.get("is_present", False)
            }
            supabase.collection("attendance").create(data)
        return True
    except Exception as e:
        print(f"Error creating attendance: {e}")
        return False


def get_attendance_for_teacher(teacher_id):
    try:
        # Get teacher's subjects
        subjects = get_teacher_subjects(teacher_id)
        subject_ids = [s["subject_id"] for s in subjects]

        if not subject_ids:
            return []

        # Build subject lookup map
        subject_map = {s["subject_id"]: s for s in subjects}

        # Fetch attendance for each subject
        all_records = []
        for sid in subject_ids:
            try:
                result = supabase.collection("attendance").get_list(1, 500, {
                    "filter": f'subject_id="{sid}"'
                })
                for item in result.items:
                    subject_info = subject_map.get(sid, {})
                    all_records.append({
                        "timestamp": str(item.timestamp) if hasattr(item, 'timestamp') else "",
                        "is_present": item.is_present if hasattr(item, 'is_present') else False,
                        "subjects": {
                            "name": subject_info.get("name", ""),
                            "subject_code": subject_info.get("subject_code", "")
                        }
                    })
            except Exception as ex:
                print(f"Error fetching attendance for subject {sid}: {ex}")
                continue

        return all_records
    except Exception as e:
        print(f"Error getting attendance for teacher: {e}")
        return []


def get_enrolled_students_for_subject(subject_id):
    """Get all enrolled students with their voice/face embeddings for a subject"""
    try:
        enrollments = supabase.collection("subject_students").get_list(1, 500, {
            "filter": f'subject_id="{subject_id}"'
        })

        students = []
        for enrollment in enrollments.items:
            try:
                student = supabase.collection("students").get_one(enrollment.student_id)

                face_emb = student.face_encoding if hasattr(student, 'face_encoding') else None
                if face_emb and isinstance(face_emb, str):
                    try:
                        face_emb = [float(x.strip()) for x in face_emb.strip('[]').split(',') if x.strip()]
                    except:
                        face_emb = None

                voice_emb = student.voice_encoding if hasattr(student, 'voice_encoding') else None
                if voice_emb and isinstance(voice_emb, str):
                    try:
                        voice_emb = [float(x.strip()) for x in voice_emb.strip('[]').split(',') if x.strip()]
                    except:
                        voice_emb = None

                students.append({
                    "student_id": student.id,
                    "name": student.name if hasattr(student, 'name') else "",
                    "face_embedding": face_emb,
                    "voice_embedding": voice_emb
                })
            except Exception as ex:
                print(f"Error fetching student {enrollment.student_id}: {ex}")
                continue

        return students
    except Exception as e:
        print(f"Error getting enrolled students: {e}")
        return []