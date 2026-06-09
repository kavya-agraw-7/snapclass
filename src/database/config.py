import streamlit as st
from pocketbase import PocketBase

# Read from secrets when deployed, fallback to local for development
POCKETBASE_URL = st.secrets.get("POCKETBASE_URL", "http://127.0.0.1:8090")
supabase = PocketBase(POCKETBASE_URL)

def check_supabase_connection():
    try:
        supabase.collection("teachers").get_list(1, 1)
        return True, "Success", "Connected to PocketBase successfully!"
    except Exception as e:
        return False, "Connection Error", f"Failed to connect: {str(e)}"