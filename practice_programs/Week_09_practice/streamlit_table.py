import os, json
import streamlit as st

DATA_PATH = "msms.json"

def load_data(path = DATA_PATH):
    if os.path.exists(path):
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)

        st.session_state.students = data.get("students", [])
        # st.session_state.courses = data.get("courses", [])

    else:
        st.session_state.setdefault("students", [])
        # st.session_state.setdefault("courses", [])

def students_table(students):
    st.dataframe(students, use_container_width = True, hide_index = True)

def save_json(path = DATA_PATH):
    with open(path, "w", encoding = "utf-8") as f:
        json.dump(
            {'students': st.session_state.students, 'courses': st.session_state.courses},
            f, indent = 2
        )

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System")
    st.sidebar.title("MSMS")
    page = st.sidebar.radio("Go to", ["🏠Home", "🧑‍🎓Students", "📚Courses"], index = 0)
    st.sidebar.markdown("---")
    if "theme_compact" not in st.session_state:
        st.session_state.theme_compact = False
    st.session_state.theme_compact = st.sidebar.checkbox(
        "Compact tables", value = st.session_state.theme_compact
    )
    load_data()
    if page == "🏠Home":
        st.title("MSMS DashBoard")

        colA, colB = st.columns(2)
        with colA:
            st.subheader("Students")
            students_table(st.session_state.students)
        with colB:
            pass

if __name__ == "__main__":
    launch()