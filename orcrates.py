import streamlit as st
import orcratesTab1
import orcratesTab2

# Title of the app
st.title('OR Crates Simulator')
st.write("OR-Finishes Web Application")
st.write("gambling gambling gambling gambling gambling gambling gambling gambling gambling gambling gambling gambling gambling gambling")

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

if 'calc' not in st.session_state:
    st.session_state.calc = True
if 'buttonText' not in st.session_state:
    st.session_state.buttonText = "Crates Simulator"
    st.session_state.buttonDis = True
# Function to set the active tab
def set_active_tab():
    st.session_state.calc = not st.session_state.calc
    if st.session_state.calc==True:
        st.session_state.buttonText="Results"
    else:
        st.session_state.buttonText = "Crates Simulator"

# Function to show the dialog with crop information
@st.dialog("How to Use the OR Crates Simulator")
def showDialog():
    orcratesTab1.modalContent() 

# Create columns for buttons
col1, col2 = st.columns(2)

with col1:
    st.button(st.session_state.buttonText, on_click=set_active_tab,disabled=st.session_state.buttonDis,use_container_width=True)
with col2:
    if st.button("How to Use",use_container_width=True):
        showDialog()  # Call the dialog function

# Display content based on the active tab
if st.session_state.calc:
    orcratesTab1.formUI()
else:
    orcratesTab2.display()
    

st.write("")
st.write("")
st.write("")
st.markdown("""
---
""")
footer_container = st.container()
with footer_container:
    col1, col2, col3 = st.columns((3, 2, 1))
    
    with col1:
        st.write("Adapted by McSwagical (contact if issues occur.)")
        st.write("Built by sxdOwO")
    
    with col2:
        st.write("Copyright © Amelia Freeman")
    
    with col3:
        st.markdown("""
            <style>
                .discord-button {
                    display: inline-block;
                    background-color: #5865F2;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    border: 2px solid #111978;
                    border-radius: 5px;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                    transition: background-color 0.3s;
                }
                .discord-button:hover {
                    background-color: #3E20C4;  /* Change this to your desired hover color */
                }
            </style>
            <a href="https://discord.gg/or-finishes">
                <button target="_blank" class="discord-button">
                    <i class='fa-brands fa-discord'></i> <b>ORF</b>
                </button>
            </a>
                    
        """, unsafe_allow_html=True)