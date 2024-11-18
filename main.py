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

        majors = ("Aerospace Engineering, B.S.", "Agribusiness and Food Industry Management, B.S.", "Agricultural Business, B.S.", "Agricultural Communication, B.S.", "Agricultural Science, B.S.", "Agricultural Systems Management, B.S.", "Animal Health Science, B.S.", 
                  "Animal Science, B.S.", "Anthropology And Geography, B.S.", "Anthropology B.A.", "Apparel Merchandising and Management, B.S.", "Architectural Engineering, B.S.", "Architecture, B. Architecture", "Architecture, B.A.", "Art And Design, B. Fine Arts", "Art B.A.", 
                  "Art B.F.A.", "Art History, B.A.", "Biochemistry, B.S.", "Biological Sciences, B.S.", "Biology B.S.", "Biomedical Engineering, B.S.", "Bioresource And Agricultural Engineering, B.S.", "Biotechnology, B.S.", "Botany B.S.", "Business Administration, B.S.", "Business Administration B.S.", 
                  "Chemical Engineering, B.S.", "Chemistry, B.S.", "Chemistry, B.A.", "Chemistry B.S.", "Child Development, B.S.", "Child Development & Family Relations B.A.", "City And Regional Planning, B.S.", "Civil Engineering, B.S.", "Communication B.A.", "Communication Studies, B.A.", 
                  "Comparative Ethnic Studies, B.A.", "Computer Engineering, B.S.", "Computer Science, B.S.", "Construction Engineering and Management, B.S.", "Construction Management, B.S.", "Criminology and Justice Studies B.A.", "Critical Race, Gender & Sexuality Studies B.A.", "Dairy Science, B.S.", 
                  "Dance Studies [Interdisciplinary Studies B.A - Dance Studies Concentration]", "Early Childhood Studies, B.A.", "Economics, B.S.", "Economics B.A.", "Electrical Engineering, B.S.", "Electromechanical Systems Engineering Technology, B.S.", "Electronic Systems Engineering Technology, B.S.", "English, B.A.", "English B.A.", "Environmental Biology, B.S.", 
                  "Environmental Earth And Soil Science, B.S.", "Environmental Engineering, B.S.", "Environmental Management And Protection, B.S.", "Environmental Resource Engineering B.S.", "Environmental Science & Management B.S.", "Environmental Studies B.A.", "Facilities Engineering Technology, B.S.", "Fisheries Biology B.S.", "Food Science, B.S.", "Food Science and Technology, B.S.", "Forest And Fire Sciences, B.S.", "Forestry B.S.", "French & Francophone Studies B.A.", "Gender, Ethnicity and Multicultural Studies, B.A.", "General Engineering, B.S.", "Geography B.A.", "Geography B.S.", "Geology B.A.", "Geology B.S.", "Global Studies and Maritime Affairs, B.A.", "Graphic Communication, B.S.", "History, B.A.", "History B.A.", "Hospitality Management, B.S.", "Industrial Engineering, B.S.", "Industrial Technology And Packaging, B.S.", "International Studies B.A.", "Journalism, B.S.", "Journalism B.A.", "Kinesiology, B.S.", "Kinesiology B.S.", "Landscape Architecture, B.S.", "Landscape Architecture, B.L.A.", "Leadership Studies [Interdisciplinary Studies B.A. - Leadership Studies Concentration]", "Liberal Arts And Engineering Studies, B.A.", "Liberal Studies, B.S.", "Liberal Studies B.A.", "Manufacturing Engineering, B.S.", "Marine Engineering Technology, B.S.", "Marine Sciences, B.S.", "Marine Transportation, B.S.", "Materials Engineering, B.S.", "Mathematics, B.S", "Mathematics B.A.", "Mathematics B.S.", "Mechanical Engineering, B.S.", "Microbiology, B.S.", "Music, B.A.", "Music B.A.", "Music B.M.", "Music B.S.", "Native American Studies B.A.", "Nursing B.S.N. (RN-BSN)", "Nutrition, B.S.", "Oceanography B.S.", "Philosophy, B.A.", "Philosophy B.A.", "Physical Science B.A.", "Physics, B.S.", "Physics, B.A.", "Physics B.S.", "Plant Science, B.S.", "Plant Sciences, B.S.", "Political Science, B.A.", "Political Science, B.S.", "Political Science B.A.", "Psychology, B.S.", "Psychology B.A.", "Public Health, B.S.", "Rangeland Resource Science B.S.", "Recreation, Parks And Tourism Administration", "Recreation Administration B.A.", "Religious Studies B.A.", "Science, Technology, and Society, B.A.", "Social Work B.A.", "Sociology, B.A.", "Sociology B.A.", "Software Engineering, B.S.", "Spanish, B.A.", "Spanish B.A.", "Statistics, B.S.", "Theatre Arts, B.A.", "Theatre Arts B.A.", "Urban and Regional Planning, B.S.", "Wildlife B.S.", "Wine And Viticulture, B.S.", "Zoology B.S."

)
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

        schools = ("Allan Hancock College", "American River College", "Antelope Valley College",
 "Bakersfield College", "Barstow Community College", "Berkeley City College", "Butte College", 
"Cabrillo College", "Canada College", "Cerritos College", "Cerro Coso Community College", "Chabot College", "Chaffey College", "Citrus College", "City College of San Francisco", "Clovis Community College", "Coalinga College", "Coastline Community College", "College of Alameda", "College of Marin", "College of San Mateo", "College of the Canyons", "College of the Desert", "College of the Redwoods", "College of the Sequoias", "College of the Siskiyous", 
"Columbia College", "Compton College", "Compton Community College", "Contra Costa College", "Copper Mountain College", "Cosumnes River College", "Crafton Hills College", "Cuesta College", "Cuyamaca College", "Cypress College",
"De Anza College", "Diablo Valley College", "East Los Angeles College", 
"El Camino College", "Evergreen Valley College", 
"Feather River College", "Folsom Lake College", "Foothill College", "Fresno City College", "Fullerton College", "Gavilan College", "Glendale Community College", "Golden West College", "Grossmont College", 
"Hartnell College", 
"Imperial Valley College", "Irvine Valley College", 
"Kings River College", 
"Lake Tahoe Community College", "Laney College", "Las Positas College", "Lassen Community College", "Lemoore College", "Long Beach City College", "Los Angeles City College", "Los Angeles Harbor College", "Los Angeles Mission College", "Los Angeles Pierce College", "Los Angeles Southwest College", "Los Angeles Trade Technical College", "Los Angeles Valley College", "Los Medanos College", 
"Madera Community College", "Mendocino College", "Merced College", "Merritt College", "MiraCosta College", "Mission College", "Modesto Junior College", "Monterey Peninsula College", "Moorpark College", "Moreno Valley College", "Mount San Antonio College", "Mt. San Jacinto College", 
"Napa Valley College", "Norco College", 
"Ohlone College", "Orange Coast College", "Oxnard College", 
"Palo Verde College", "Palomar College", "Pasadena City College", "Porterville College", 
"Rancho Santiago College", "Reedley College", "Rio Hondo College", "Riverside City College", 
"Sacramento City College", "Saddleback College", "San Bernardino Valley College", "San Diego City College", "San Diego Mesa College", "San Diego Miramar College", "San Joaquin Delta College", "San Jose City College", "Santa Ana College", "Santa Barbara City College", "Santa Monica College", "Santa Rosa Junior College", "Santiago Canyon College", "Shasta College", "Sierra College", "Skyline College", "Solano Community College", "Southwestern College", 
"Taft College", 
"Ventura College", "Victor Valley College", "Vista Community College", 
"West Hills College Coalinga", "West Hills College Lemoore", "West Los Angeles College", "West Valley College", "Woodland Community College", 
"Yuba College", 
"California Maritime Academy", "California Polytechnic University, Humboldt", "California Polytechnic University, Pomona", "California Polytechnic University, San Luis Obispo", "California State University, Bakersfield", "California State University, Channel Islands", "California State University, Chico", "California State University, Dominguez Hills", "California State University, East Bay", "California State University, Fresno", "California State University, Fullerton",
"California State University, Hayward", "California State University, Long Beach", "California State University, Los Angeles", "California State University, Maritime Academy", "California State University, Monterey Bay", "California State University, Northridge", "California State University, Sacramento", "California State University, San Bernardino", "California State University, San Marcos", "California State University, Stanislaus", "Humboldt State University", "San Diego State University",
"San Francisco State University, San Jose State University", "Sonoma State University","University of California, Berkeley", "University of California, Davis", "University of California, Irvine", "University of California, Los Angeles", "University of California, Merced", "University of California, Riverside", "University of California, San Diego", "University of California, Santa Barbara", "University of California, Santa Cruz", "California Baptist University, California Lutheran University", 
"Charles R. Drew University of Medicine and Science", "Concordia University Irvine", "Dominican University of California", "Fresno Pacific University", "Humphreys University", "Laguna College of Art + Design", "Los Angeles Pacific University", "Loyola Marymount University", "Menlo College", "Mount Saint Mary's University Los Angeles", "National University", "Notre Dame de Namur University", "Palo Alto University", "Pepperdine University", "Reach University", "Saint Mary's College of California", 
"Samuel Merritt University", "Santa Clara University", "Simpson University", "Touro University Worldwide", "University of La Verne", "University of Redlands", "University of the Pacific", "University of the West", "Whittier College")
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
