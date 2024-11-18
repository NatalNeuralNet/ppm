import streamlit as st
from ai import run_flow
from profiles import create_profile, get_notes, get_profile 
from form_submit import update_personal_info, add_note, delete_note

st.title("Pathway Mapper")

if "profile" not in st.session_state:
    st.session_state.profile = {"general": {"name": "", "major": "", "current_college": "", "gpa": ""}}
    
@st.fragment()
def personal_data_form():
    with st.form("personal_data"):
        st.header("Student Profile")
        profile = st.session_state.profile

        name = st.text_input("Name", value=profile["general"]["name"])

        majors = ("Computer Science", "Biology")
        # Ensure the major is valid; fallback to the first item in majors
        major = profile["general"].get("major", majors[0])
        if major not in majors:
            major = majors[0]

        major = st.selectbox("Major", majors, index=majors.index(major))

        # Safely handle GPA conversion and ensure float type
        gpa_value = profile["general"].get("gpa", 0.0)
        if isinstance(gpa_value, str):
            try:
                gpa_value = float(gpa_value.strip()) if gpa_value.strip() else 0.0
            except ValueError:
                gpa_value = 0.0
        else:
            gpa_value = float(gpa_value)  # Ensure value is float

        gpa = st.number_input(
            "G.P.A.",
            min_value=0.0,
            max_value=5.0,
            step=0.1,
            value=gpa_value,  # Ensure this is a float
        )

        schools = ("Merced College", "UC Davis")
        # Ensure the current_college is valid; fallback to the first item in schools
        current_college = profile["general"].get("current_college", schools[0])
        if current_college not in schools:
            current_college = schools[0]

        current_college = st.selectbox(
            "Schools", schools, index=schools.index(current_college)
        )

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, current_college, gpa]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile,
                        "general",
                        name=name,
                        major=major,
                        current_college=current_college,
                        gpa=gpa,
                    )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all of the data!")





@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goals = st.multiselect(
            "Select your Goals",
            ["Transfer", "Career Advice"],
            default=profile.get("goals", ["Transfer"]),
        )

        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile, "goals", goals=goals
                    )
                    st.success("Goals updated")
            else:
                st.warning("Please select at least one goal.")

@st.fragment()
def completed_courses_form():
    """
    Form for updating completed courses.
    """
    profile = st.session_state.profile
    # Ensure completed_courses is a dictionary, not a list
    completed_courses = profile.get("completed_courses", {
        "math": "",
        "science": "",
        "english": "",
        "general_ed": "",
        "major_specific": "",
        "other": "",
    })
    if not isinstance(completed_courses, dict):
        # Reset to default dictionary if the format is incorrect
        completed_courses = {
            "math": "",
            "science": "",
            "english": "",
            "general_ed": "",
            "major_specific": "",
            "other": "",
        }

    with st.form("completed_courses_form"):
        st.header("Completed Courses")

        # Input fields for each type of course
        math = st.text_input("Math", value=completed_courses.get("math", ""))
        science = st.text_input("Science", value=completed_courses.get("science", ""))
        english = st.text_input("English", value=completed_courses.get("english", ""))
        general_ed = st.text_input(
            "General Education", value=completed_courses.get("general_ed", "")
        )
        major_specific = st.text_input(
            "Major Specific", value=completed_courses.get("major_specific", "")
        )
        other = st.text_input("Other", value=completed_courses.get("other", ""))

        # Submit button
        completed_courses_submit = st.form_submit_button("Save")
        if completed_courses_submit:
            with st.spinner():
                # Update the profile with the completed courses
                st.session_state.profile = update_personal_info(
                    profile,
                    "completed_courses",
                    math=math,
                    science=science,
                    english=english,
                    general_ed=general_ed,
                    major_specific=major_specific,
                    other=other,
                )
            st.write("Debug: Completed Courses After Update:", st.session_state.profile["completed_courses"])
            st.success("Completed courses updated.")


@st.fragment()
def notes():
    st.subheader("Notes: ")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=i):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()
    
    new_note = st.text_input("Add a new note: ")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()

@st.fragment()
def continuous_chat():
    """
    Continuous chat feature that maintains chat history.
    """
    st.header("AI Chat")
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history dynamically
    for chat in st.session_state.chat_history:
        role, message = chat
        if role == "user":
            st.markdown(f"**You:** {message}")
        elif role == "ai":
            st.markdown(f"**AI:** {message}")

    # Input for user's message
    user_input = st.text_input("Your Message", key="chat_input")
    if st.button("Send"):
        if user_input:
            # Append user's input to chat history
            st.session_state.chat_history.append(("user", user_input))
            
            # Get AI's response
            with st.spinner("Waiting for AI response..."):
                try:
                    ai_response = run_flow(st.session_state.profile, user_input)
                    # Append AI's response to chat history
                    st.session_state.chat_history.append(("ai", ai_response))
                except Exception as e:
                    st.error(f"Error: {e}")
            # Refresh the chat dynamically
            st.rerun()

@st.fragment()
def forms():
    # Ensure profile_id is initialized
    if "profile_id" not in st.session_state:
        profile_id = 2  # Default profile_id; replace with dynamic logic if needed
        try:
            profile = get_profile(profile_id)
            if profile:
                # Profile already exists
                st.session_state.profile_id = profile_id
                st.session_state.profile = profile
            else:
                # Create a new profile
                profile_id, profile = create_profile(profile_id)
                st.session_state.profile_id = profile_id
                st.session_state.profile = profile
        except Exception as e:
            st.error(f"Error fetching or creating profile: {e}")
            return

    # Ensure completed_courses exists in profile
    if "completed_courses" not in st.session_state.profile:
        st.session_state.profile["completed_courses"] = {
            "math": "",
            "science": "",
            "english": "",
            "general_ed": "",
            "major_specific": "",
            "other": "",
        }

    # Ensure notes are initialized
    if "notes" not in st.session_state:
        try:
            st.session_state.notes = get_notes(st.session_state.profile_id)
        except Exception as e:
            st.error(f"Error fetching notes: {e}")
            st.session_state.notes = []
    
    # Call all forms and the continuous chat
    personal_data_form()
    goals_form()
    completed_courses_form()
    notes()
    continuous_chat()



if __name__ == "__main__":
    forms()