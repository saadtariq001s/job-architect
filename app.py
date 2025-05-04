import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Job Title Generator",
    layout="wide"
)

# Add title and description
st.title("Job Title Generator")
st.markdown("Create and manage job titles by entering division, subdivision, and selecting a hierarchy level.")

# Initialize session state to store our data
if 'job_data' not in st.session_state:
    st.session_state.job_data = pd.DataFrame(columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title'])

# Create a form for user input
with st.form(key="job_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        division = st.text_input("Division", placeholder="e.g., Commercial")
    
    with col2:
        subdivision = st.text_input("Subdivision", placeholder="e.g., Strategy")
    
    with col3:
        job_titles = [
            "Officer",
            "Senior Officer",
            "Associate Analyst",
            "Analyst",
            "Specialist",
            "Senior Specialist",
            "Manager",
            "Senior Manager",
            "Director",
            "Senior Director",
            "Vice President",
            "Senior Vice President",
            "Chief (Top of the Org)"
        ]
        job_title = st.selectbox("Job Title", options=job_titles)
    
    # Generate the final job title before form submission
    if division and subdivision and job_title:
        if job_title == "Chief (Top of the Org)":
            final_job_title = f"Chief {division} Officer"
        else:
            final_job_title = f"{division} {subdivision} {job_title}"
    else:
        final_job_title = ""
    
    # Display the generated title
    st.markdown("### Preview")
    st.markdown(f"**Final Job Title:** {final_job_title}")
    
    submit_button = st.form_submit_button("Add Job Title")
    
    # Process form submission
    if submit_button and division and subdivision and job_title:
        # Create a new row
        new_row = pd.DataFrame({
            'Division': [division],
            'Subdivision': [subdivision],
            'Job Title': [job_title],
            'Final Job Title': [final_job_title]
        })
        
        # Append to existing data
        st.session_state.job_data = pd.concat([st.session_state.job_data, new_row], ignore_index=True)
        st.success("Job title added successfully!")

# Display the data table
st.markdown("## Job Titles Database")

# Filters for the data
st.markdown("### Filter Options")
col1, col2, col3 = st.columns(3)

with col1:
    if not st.session_state.job_data.empty:
        division_filter = st.multiselect(
            "Filter by Division",
            options=sorted(st.session_state.job_data['Division'].unique())
        )
    else:
        division_filter = []

with col2:
    if not st.session_state.job_data.empty:
        subdivision_filter = st.multiselect(
            "Filter by Subdivision",
            options=sorted(st.session_state.job_data['Subdivision'].unique())
        )
    else:
        subdivision_filter = []

with col3:
    if not st.session_state.job_data.empty:
        job_title_filter = st.multiselect(
            "Filter by Job Title",
            options=sorted(st.session_state.job_data['Job Title'].unique())
        )
    else:
        job_title_filter = []

# Apply filters
filtered_data = st.session_state.job_data.copy()

if division_filter:
    filtered_data = filtered_data[filtered_data['Division'].isin(division_filter)]

if subdivision_filter:
    filtered_data = filtered_data[filtered_data['Subdivision'].isin(subdivision_filter)]

if job_title_filter:
    filtered_data = filtered_data[filtered_data['Job Title'].isin(job_title_filter)]

# Display the filtered data
st.dataframe(filtered_data, use_container_width=True)

# Export functionality
if not filtered_data.empty:
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download as CSV",
        csv,
        "job_titles.csv",
        "text/csv",
        key='download-csv'
    )

# Clear all data button
if not st.session_state.job_data.empty:
    if st.button("Clear All Data"):
        st.session_state.job_data = pd.DataFrame(columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title'])
        st.success("All data cleared!")
        st.rerun()