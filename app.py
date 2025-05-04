import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Job Architect",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .stForm {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    .section-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 15px;
        border-left: 5px solid #3B82F6;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
    }
    .success-message {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #10B981;
    }
    .stDataFrame {
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Job Architect</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create, manage, and export standardized job titles for your organization</p>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <strong>Getting Started:</strong> Enter a division and subdivision, select a hierarchy level, and the tool will automatically
    generate a standardized job title. All entries are stored in the table below for easy filtering and export.
</div>
""", unsafe_allow_html=True)

# Initialize session state to store our data
if 'job_data' not in st.session_state:
    st.session_state.job_data = pd.DataFrame(columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title', 'Created'])

# Create two columns: form and stats
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown('<p class="section-header">Create Job Title</p>', unsafe_allow_html=True)
    
    # Create a form with improved styling
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
            job_title = st.selectbox("Hierarchy Level", options=job_titles)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Generate the final job title before form submission
        if division and subdivision and job_title:
            if job_title == "Chief (Top of the Org)":
                final_job_title = f"Chief {division} Officer"
            else:
                final_job_title = f"{division} {subdivision} {job_title}"
        else:
            final_job_title = ""
        
        # Display the generated title with better styling
        st.markdown("#### Generated Title Preview")
        if final_job_title:
            st.markdown(f"""
            <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; border-left: 4px solid #0EA5E9; margin-bottom: 20px;">
                <span style="color: #0369A1; font-weight: 500;">Final Job Title:</span> 
                <span style="font-size: 1.2rem; font-weight: bold;">{final_job_title}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #FEF2F2; padding: 15px; border-radius: 5px; border-left: 4px solid #EF4444; margin-bottom: 20px;">
                <span style="color: #B91C1C; font-weight: 500;">Please fill all fields to generate a job title</span>
            </div>
            """, unsafe_allow_html=True)
        
        submit_col1, submit_col2 = st.columns([1, 2])
        with submit_col1:
            submit_button = st.form_submit_button("➕ Add Job Title")
        
        # Process form submission
        if submit_button and division and subdivision and job_title:
            # Create a new row
            new_row = pd.DataFrame({
                'Division': [division],
                'Subdivision': [subdivision],
                'Job Title': [job_title],
                'Final Job Title': [final_job_title],
                'Created': [datetime.now().strftime("%Y-%m-%d %H:%M")]
            })
            
            # Append to existing data
            st.session_state.job_data = pd.concat([st.session_state.job_data, new_row], ignore_index=True)
            st.markdown("""
            <div class="success-message">
                ✅ Job title added successfully!
            </div>
            """, unsafe_allow_html=True)

with right_col:
    # Show statistics if there is data
    if not st.session_state.job_data.empty:
        st.markdown('<p class="section-header">Statistics</p>', unsafe_allow_html=True)
        
        total_entries = len(st.session_state.job_data)
        divisions_count = st.session_state.job_data['Division'].nunique()
        subdivisions_count = st.session_state.job_data['Subdivision'].nunique()
        
        st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <p style="font-size: 1.2rem; margin-bottom: 10px; color: #334155;"><strong>Database Overview</strong></p>
            <p style="margin: 5px 0; font-size: 1rem;"><span style="color: #64748B;">Total Entries:</span> <strong>{total_entries}</strong></p>
            <p style="margin: 5px 0; font-size: 1rem;"><span style="color: #64748B;">Unique Divisions:</span> <strong>{divisions_count}</strong></p>
            <p style="margin: 5px 0; font-size: 1rem;"><span style="color: #64748B;">Unique Subdivisions:</span> <strong>{subdivisions_count}</strong></p>
        </div>
        """, unsafe_allow_html=True)

# Add a separator
st.markdown("<hr>", unsafe_allow_html=True)

# Initialize filter variables
division_filter = []
subdivision_filter = []
job_title_filter = []

# Create a sidebar for filters
st.sidebar.markdown('<p class="section-header">Filter Options</p>', unsafe_allow_html=True)

if not st.session_state.job_data.empty:
    st.sidebar.markdown("""
    <div style="font-size: 0.9rem; color: #6B7280; margin-bottom: 15px;">
        Use the filters below to find specific job titles in your database.
    </div>
    """, unsafe_allow_html=True)
    
    division_filter = st.sidebar.multiselect(
        "Division",
        options=sorted(st.session_state.job_data['Division'].unique()),
        help="Select one or more divisions to filter"
    )
    
    subdivision_filter = st.sidebar.multiselect(
        "Subdivision",
        options=sorted(st.session_state.job_data['Subdivision'].unique()),
        help="Select one or more subdivisions to filter"
    )
    
    job_title_filter = st.sidebar.multiselect(
        "Hierarchy Level",
        options=sorted(st.session_state.job_data['Job Title'].unique()),
        help="Select one or more hierarchy levels to filter"
    )
    
    # Clear filters button
    if division_filter or subdivision_filter or job_title_filter:
        if st.sidebar.button("Clear Filters", type="secondary"):
            # This will trigger a rerun with empty filters
            st.rerun()
else:
    st.sidebar.info("Add job titles to enable filtering")

# Apply filters to data
filtered_data = st.session_state.job_data.copy()

if division_filter:
    filtered_data = filtered_data[filtered_data['Division'].isin(division_filter)]

if subdivision_filter:
    filtered_data = filtered_data[filtered_data['Subdivision'].isin(subdivision_filter)]

if job_title_filter:
    filtered_data = filtered_data[filtered_data['Job Title'].isin(job_title_filter)]

# Main content - Database display
st.markdown('<p class="section-header">Job Titles Database</p>', unsafe_allow_html=True)

# Add counter for filtered results
if not st.session_state.job_data.empty:
    filter_text = ""
    if division_filter or subdivision_filter or job_title_filter:
        filter_text = f" (filtered: showing {len(filtered_data)} of {len(st.session_state.job_data)} entries)"
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <div style="font-size: 1rem; color: #4B5563;">
            Showing all job titles{filter_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display the filtered data with improved styling
if not filtered_data.empty:
    # Reorder columns to show Final Job Title first
    display_columns = ['Final Job Title', 'Division', 'Subdivision', 'Job Title']
    if 'Created' in filtered_data.columns:
        display_columns.append('Created')
    
    st.dataframe(
        filtered_data[display_columns],
        use_container_width=True,
        column_config={
            "Final Job Title": st.column_config.TextColumn(
                "Final Job Title",
                width="large",
                help="The complete job title"
            ),
            "Created": st.column_config.DatetimeColumn(
                "Created On",
                format="MMM DD, YYYY • HH:mm",
                help="When this entry was created"
            )
        },
        hide_index=True
    )
    
    # Action buttons in a row
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Export functionality
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            "💾 Export as CSV",
            csv,
            "job_titles.csv",
            "text/csv",
            key='download-csv',
            help="Download the current filtered view as a CSV file"
        )
    
    with col2:
        # Clear all data button
        if st.button("🗑️ Clear All Data", help="Remove all job titles from the database"):
            # Update for the latest columns
            if 'Created' in st.session_state.job_data.columns:
                st.session_state.job_data = pd.DataFrame(columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title', 'Created'])
            else:
                st.session_state.job_data = pd.DataFrame(columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title'])
            st.success("All data cleared!")
            st.rerun()
else:
    # Empty state message
    st.markdown("""
    <div style="background-color: #F9FAFB; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;">
        <div style="font-size: 2rem; margin-bottom: 10px; color: #9CA3AF;">📋</div>
        <p style="font-size: 1.2rem; font-weight: 500; color: #4B5563; margin-bottom: 5px;">No Job Titles Yet</p>
        <p style="color: #6B7280;">Add your first job title using the form above to get started.</p>
    </div>
    """, unsafe_allow_html=True)