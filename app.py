import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Set page configuration
st.set_page_config(
    page_title="Job Title Generator",
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
    .import-box {
        background-color: #F0F9FF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Job Title Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create, manage, and export standardized job titles for your organization</p>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <strong>Getting Started:</strong> Enter a division and subdivision, select a hierarchy level, and the tool will automatically
    generate a standardized job title. All entries are stored in the table below for easy filtering and export.
    You can also import data from a CSV file.
</div>
""", unsafe_allow_html=True)

# Initialize session state to store our data
if 'job_data' not in st.session_state:
    st.session_state.job_data = pd.DataFrame(columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title', 'PERNR', 'JOB_CODE', 'Created'])

# Ensure all string columns are of string type to prevent sorting issues
if not st.session_state.job_data.empty:
    for col in ['Division', 'Subdivision', 'PERNR', 'JOB_CODE', 'Job Title', 'Final Job Title']:
        if col in st.session_state.job_data.columns:
            st.session_state.job_data[col] = st.session_state.job_data[col].astype(str)

# Create tabs for manual entry and import
tab1, tab2 = st.tabs(["Manual Entry", "Import from CSV"])

with tab1:
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
            
            # Additional fields for PERNR and JOB_CODE
            col4, col5 = st.columns(2)
            
            with col4:
                pernr = st.text_input("PERNR", placeholder="e.g., 105804")
            
            with col5:
                job_code = st.text_input("JOB_CODE", placeholder="e.g., A409-ESG")
            
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
                    'PERNR': [pernr if pernr else ""],
                    'JOB_CODE': [job_code if job_code else ""],
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

with tab2:
    # CSV Import Section
    st.markdown('<p class="section-header">Import Job Titles from CSV</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>CSV Import Instructions:</strong><br>
        • Upload a CSV file containing employee data<br>
        • The system will extract Division, PSL (as Subdivision), PERNR, and JOB_CODE<br>
        • Select a hierarchy level to apply to all imported entries<br>
        • Preview and confirm before adding to the database
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv", "txt"])
    
    # Add encoding selection
    encoding_options = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'windows-1252']
    selected_encoding = st.selectbox(
        "Select file encoding", 
        options=encoding_options,
        index=1,  # Default to latin-1 as it's more forgiving
        help="If you encounter encoding errors, try a different encoding"
    )
    
    # Option to treat as space-separated instead of comma-separated
    delimiter_option = st.radio(
        "File format", 
        options=["Comma-separated (CSV)", "Space-separated (TXT)"],
        index=1,  # Default to space-separated based on your sample data
        help="Select the format that matches your file"
    )
    delimiter = "," if delimiter_option == "Comma-separated (CSV)" else None  # None will use whitespace
    
    if uploaded_file is not None:
        try:
            # Read file content
            file_content = uploaded_file.read()
            
            # If space-separated, convert to proper CSV format first
            if delimiter_option == "Space-separated (TXT)":
                # Decode using selected encoding
                try:
                    content_str = file_content.decode(selected_encoding)
                    
                    # Display raw content preview 
                    with st.expander("Show raw file content"):
                        st.text(content_str[:1000] + "..." if len(content_str) > 1000 else content_str)
                    
                    # Process the space-separated data
                    lines = content_str.strip().split('\n')
                    
                    # Auto-detect header
                    if "PERNR" in lines[0] and "DIVISION" in lines[0] and "PSL" in lines[0]:
                        header = lines[0].split()
                        data_lines = lines[1:]
                    else:
                        # Assume first line is data, create generic headers
                        num_columns = len(lines[0].split())
                        default_headers = ["PERNR", "JOB_TEXT", "DIVISION", "PSL", "SUBPSL", "SAL_BAND", "JOB_CODE"]
                        
                        # Use default headers if they match the column count, otherwise create generic ones
                        if num_columns == len(default_headers):
                            header = default_headers
                        else:
                            header = [f"Column_{i+1}" for i in range(num_columns)]
                        
                        data_lines = lines
                    
                    # Convert to pandas DataFrame
                    data_rows = []
                    for line in data_lines:
                        # Split by whitespace but keep multiple spaces within quotes
                        values = []
                        current = ""
                        in_quotes = False
                        
                        for char in line:
                            if char == '"':
                                in_quotes = not in_quotes
                                current += char
                            elif char.isspace() and not in_quotes:
                                if current:
                                    values.append(current)
                                    current = ""
                            else:
                                current += char
                        
                        if current:
                            values.append(current)
                            
                        # Only add rows that have enough columns
                        if len(values) >= 4:  # Need at least PERNR, DIVISION, PSL, JOB_CODE
                            # Make sure we have enough values to match header length
                            while len(values) < len(header):
                                values.append("")
                            # Truncate if too many values
                            values = values[:len(header)]
                            data_rows.append(values)
                    
                    # Create DataFrame
                    csv_data = pd.DataFrame(data_rows, columns=header)
                    
                except Exception as e:
                    st.error(f"Error processing space-separated file: {str(e)}")
                    st.stop()
            else:
                # Regular CSV processing
                try:
                    # Try to read with pandas directly
                    csv_data = pd.read_csv(io.BytesIO(file_content), encoding=selected_encoding, delimiter=delimiter)
                except Exception as e:
                    st.error(f"Error reading CSV with pandas: {str(e)}")
                    st.stop()
            
            # Display preview of the processed data
            st.markdown("### CSV Preview")
            st.dataframe(csv_data.head(5), use_container_width=True)
            
            # Check if required columns exist
            required_columns = ['DIVISION', 'PSL', 'PERNR', 'JOB_CODE']
            
            # Map column names to expected columns (case insensitive)
            column_mapping = {}
            for col in csv_data.columns:
                for req_col in required_columns:
                    if col.upper() == req_col:
                        column_mapping[col] = req_col
            
            # Rename columns to expected format
            if column_mapping:
                csv_data.rename(columns=column_mapping, inplace=True)
            
            # Check for missing columns after mapping
            missing_columns = [col for col in required_columns if col not in csv_data.columns]
            
            if missing_columns:
                # Try to infer columns from data structure
                if len(csv_data.columns) >= 4:
                    st.warning(f"Missing columns: {', '.join(missing_columns)}. Trying to infer columns from data structure.")
                    
                    # Create mapping based on position
                    position_mapping = {}
                    
                    # If we have at least 4 columns, assume a specific order
                    if len(csv_data.columns) >= 7:
                        # Assume columns are in this order: PERNR, JOB_TEXT, DIVISION, PSL, SUBPSL, SAL_BAND, JOB_CODE
                        position_mapping = {
                            csv_data.columns[0]: 'PERNR',
                            csv_data.columns[2]: 'DIVISION',
                            csv_data.columns[3]: 'PSL',
                            csv_data.columns[6]: 'JOB_CODE'
                        }
                    elif len(csv_data.columns) >= 4:
                        # If fewer columns, make a best guess
                        position_mapping = {
                            csv_data.columns[0]: 'PERNR',
                            csv_data.columns[1]: 'DIVISION',
                            csv_data.columns[2]: 'PSL',
                            csv_data.columns[3]: 'JOB_CODE'
                        }
                    
                    # Apply mapping
                    csv_data.rename(columns=position_mapping, inplace=True)
                    
                    # Display the mapping we're using
                    st.info(f"Mapped columns: {position_mapping}")
                    
                    # Check again for missing columns
                    missing_columns = [col for col in required_columns if col not in csv_data.columns]
                
                if missing_columns:
                    st.error(f"Still missing required columns: {', '.join(missing_columns)}")
                    
                    # Show suggestions for manually creating columns
                    st.markdown("""
                    <div style="background-color: #FEF2F2; padding: 15px; border-radius: 5px; margin-top: 10px;">
                        <strong>Column Format Tip:</strong> Your file should have columns for:<br>
                        PERNR (employee ID), DIVISION (department), PSL (sub-division), and JOB_CODE (role code).<br>
                        Please ensure your file has these columns or is in a format where these can be identified.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the column names we found
                    st.write("Found columns:", list(csv_data.columns))
                    
                    st.stop()
            else:
                with st.form(key="import_form"):
                    st.markdown("### Automatic Hierarchy Level Assignment")
                    
                    # Display info about automatic hierarchy detection
                    st.info("""
                        The system will automatically analyze the JOB_TEXT field to determine the appropriate 
                        hierarchy level for each position. You can override this with a default selection below.
                    """)
                    
                    # Option to override automatic detection
                    use_auto_detection = st.checkbox("Use automatic hierarchy detection based on JOB_TEXT", value=True)
                    
                    # Hierarchy level selection only displayed if auto detection is turned off
                    imported_job_title = "Specialist"  # Default fallback
                    if not use_auto_detection:
                        imported_job_title = st.selectbox(
                            "Select Default Hierarchy Level for All Imported Entries",
                            options=[
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
                            ],
                            index=4  # Default to Specialist
                        )
                    
                    # Helper function to determine hierarchy level from job text
                    def determine_hierarchy_level(job_text):
                        """Analyzes job text to determine the appropriate hierarchy level"""
                        if not job_text or not isinstance(job_text, str):
                            return "Specialist"  # Default fallback
                        
                        job_text = job_text.lower()
                        
                        # C-level and top executives
                        if any(term in job_text for term in ["chief", "ceo", "cfo", "cio", "cto", "president", "exec vp"]):
                            return "Chief (Top of the Org)"
                            
                        # Senior Vice President
                        if any(term in job_text for term in ["sr vp", "sr. vp", "senior vp", "senior vice president", "sr vice president", "svp"]):
                            return "Senior Vice President"
                            
                        # Vice President
                        if any(term in job_text for term in [" vp", "vice president", "vice pres"]) and "senior" not in job_text and "sr" not in job_text:
                            return "Vice President"
                            
                        # Senior Director
                        if any(term in job_text for term in ["sr director", "sr. director", "senior director", "sr dir", "sr. dir", "senior dir"]):
                            return "Senior Director"
                            
                        # Director
                        if any(term in job_text for term in [" director", " dir "]) and "senior" not in job_text and "sr" not in job_text:
                            return "Director"
                            
                        # Senior Manager
                        if any(term in job_text for term in ["sr manager", "sr. manager", "senior manager", "sr mgr", "sr. mgr", "senior mgr"]):
                            return "Senior Manager"
                            
                        # Manager
                        if any(term in job_text for term in [" manager", " mgr", "supervisor", "supv", "lead"]) and "senior" not in job_text and "sr" not in job_text:
                            return "Manager"
                            
                        # Senior Specialist
                        if any(term in job_text for term in ["sr specialist", "sr. specialist", "senior specialist", "principal", "sr tech", "senior tech", "advisor", "sr prof", "senior prof"]):
                            return "Senior Specialist"
                            
                        # Specialist
                        if any(term in job_text for term in ["specialist", "technologist", "tech prof", "engineer", " tech", "technician", "scientist"]):
                            return "Specialist"
                            
                        # Senior Analyst
                        if any(term in job_text for term in ["sr analyst", "sr. analyst", "senior analyst"]):
                            return "Analyst"  # We'll use Analyst for Senior Analyst since it's not in our hierarchy levels
                            
                        # Analyst
                        if "analyst" in job_text and "associate" not in job_text:
                            return "Analyst"
                            
                        # Associate Analyst
                        if any(term in job_text for term in ["assoc analyst", "associate analyst", "jr analyst", "junior analyst"]):
                            return "Associate Analyst"
                            
                        # Senior Officer
                        if any(term in job_text for term in ["sr officer", "sr. officer", "senior officer", "sr secretary", "senior secretary", "sr assistant", "senior assistant"]):
                            return "Senior Officer"
                            
                        # Officer and other entry-level positions
                        if any(term in job_text for term in ["officer", "clerk", "secretary", "assistant", "coordinator", "rep", "operator", "handler"]):
                            return "Officer"
                        
                        # For roles without clear indicators, look for some contextual clues
                        if any(term in job_text for term in ["sr", "senior", "prin", "principal"]):
                            return "Senior Specialist"
                        
                        # Default fallback for unrecognized roles
                        return "Specialist"
                    
                    # Get JOB_TEXT column name (could be different case)
                    job_text_col = None
                    for col in csv_data.columns:
                        if col.upper() == "JOB_TEXT":
                            job_text_col = col
                            break
                    
                    # Preview of generated titles
                    st.markdown("### Title Generation Preview")
                    
                    # Create sample of titles to show
                    sample_size = min(5, len(csv_data))
                    sample_data = csv_data.head(sample_size).copy()
                    
                    # Generate sample titles and detected hierarchy levels
                    sample_data['Detected Hierarchy'] = ""
                    sample_data['Sample Final Title'] = ""
                    
                    # Generate sample titles using automatic detection or default
                    for i, row in sample_data.iterrows():
                        division = row['DIVISION']
                        subdivision = row['PSL']
                        
                        # Determine hierarchy level - automatic or default
                        if use_auto_detection and job_text_col:
                            job_text = str(row[job_text_col])
                            hierarchy = determine_hierarchy_level(job_text)
                            sample_data.at[i, 'Detected Hierarchy'] = hierarchy
                        else:
                            hierarchy = imported_job_title
                            sample_data.at[i, 'Detected Hierarchy'] = f"Default: {hierarchy}"
                        
                        # Generate final title
                        if hierarchy == "Chief (Top of the Org)":
                            final_title = f"Chief {division} Officer"
                        else:
                            final_title = f"{division} {subdivision} {hierarchy}"
                        
                        sample_data.at[i, 'Sample Final Title'] = final_title
                    
                    # Display sample with detected hierarchy levels
                    st.dataframe(
                        sample_data[['PERNR', 'DIVISION', 'PSL', 'Detected Hierarchy', 'Sample Final Title']],
                        use_container_width=True,
                        column_config={
                            "Sample Final Title": st.column_config.TextColumn(
                                "Sample Final Title",
                                width="large"
                            ),
                            "Detected Hierarchy": st.column_config.TextColumn(
                                "Detected Hierarchy Level",
                                width="medium"
                            )
                        }
                    )
                    
                    # Calculate total entries to be added
                    total_to_add = len(csv_data)
                    st.info(f"Total entries to be added: {total_to_add}")
                    
                    # Submit button
                    import_button = st.form_submit_button("Import All Job Titles")
                    
                    if import_button:
                        # Process the data
                        new_rows = []
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        
                        for _, row in csv_data.iterrows():
                            division = row['DIVISION']
                            subdivision = row['PSL']
                            pernr = str(row['PERNR'])
                            job_code = row['JOB_CODE']
                            
                            # MODIFIED: Use detected hierarchy level for each row if auto detection is enabled
                            if use_auto_detection and job_text_col:
                                job_text = str(row[job_text_col])
                                hierarchy_level = determine_hierarchy_level(job_text)
                            else:
                                hierarchy_level = imported_job_title
                            
                            # Generate final job title
                            if hierarchy_level == "Chief (Top of the Org)":
                                final_job_title = f"Chief {division} Officer"
                            else:
                                final_job_title = f"{division} {subdivision} {hierarchy_level}"
                            
                            # Add to new rows
                            new_rows.append({
                                'Division': division,
                                'Subdivision': subdivision,
                                'Job Title': hierarchy_level,  # MODIFIED: Use detected hierarchy level instead of default
                                'Final Job Title': final_job_title,
                                'PERNR': pernr,
                                'JOB_CODE': job_code,
                                'Created': timestamp
                            })
                        
                        # Create DataFrame from new rows
                        new_data = pd.DataFrame(new_rows)
                        
                        # Convert all data in the new rows to string type to prevent type comparison issues
                        for col in ['Division', 'Subdivision', 'PERNR', 'JOB_CODE']:
                            if col in new_data.columns:
                                new_data[col] = new_data[col].astype(str)
                        
                        # Also convert data types in the existing job_data to ensure consistency
                        if not st.session_state.job_data.empty:
                            for col in ['Division', 'Subdivision', 'PERNR', 'JOB_CODE']:
                                if col in st.session_state.job_data.columns:
                                    st.session_state.job_data[col] = st.session_state.job_data[col].astype(str)
                        
                        # Append to existing data
                        st.session_state.job_data = pd.concat([st.session_state.job_data, new_data], ignore_index=True)
                        
                        st.success(f"✅ Successfully imported {len(new_rows)} job titles!")
                        
        except Exception as e:
            st.error(f"Error processing CSV file: {str(e)}")
            st.markdown("""
            <div style="background-color: #FEF2F2; padding: 15px; border-radius: 5px; margin-top: 10px;">
                <strong>Formatting Tip:</strong> Make sure your CSV file has the following columns:<br>
                PERNR, JOB_TEXT, DIVISION, PSL, SUBPSL, SAL_BAND, JOB_CODE
            </div>
            """, unsafe_allow_html=True)

# Add a separator
st.markdown("<hr>", unsafe_allow_html=True)

# Initialize filter variables
division_filter = []
subdivision_filter = []
job_title_filter = []
pernr_filter = ""
job_code_filter = ""

# Create a sidebar for filters
st.sidebar.markdown('<p class="section-header">Filter Options</p>', unsafe_allow_html=True)

if not st.session_state.job_data.empty:
    st.sidebar.markdown("""
    <div style="font-size: 0.9rem; color: #6B7280; margin-bottom: 15px;">
        Use the filters below to find specific job titles in your database.
    </div>
    """, unsafe_allow_html=True)
    
    # Ensure all fields are strings before generating filter options
    string_columns = ['Division', 'Subdivision', 'Job Title']
    for col in string_columns:
        if col in st.session_state.job_data.columns:
            st.session_state.job_data[col] = st.session_state.job_data[col].astype(str)
    
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
    
    # Add new filters for PERNR and JOB_CODE
    pernr_filter = st.sidebar.text_input(
        "PERNR",
        help="Enter PERNR to search for specific employee"
    )
    
    job_code_filter = st.sidebar.text_input(
        "JOB_CODE",
        help="Enter JOB_CODE to search for specific job codes"
    )
    
    # Clear filters button
    if division_filter or subdivision_filter or job_title_filter or pernr_filter or job_code_filter:
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

# Apply text filters for PERNR and JOB_CODE
if pernr_filter:
    filtered_data = filtered_data[filtered_data['PERNR'].str.contains(pernr_filter, na=False)]

if job_code_filter:
    filtered_data = filtered_data[filtered_data['JOB_CODE'].str.contains(job_code_filter, na=False)]

# Main content - Database display
st.markdown('<p class="section-header">Job Titles Database</p>', unsafe_allow_html=True)

# Add counter for filtered results
if not st.session_state.job_data.empty:
    filter_text = ""
    if division_filter or subdivision_filter or job_title_filter or pernr_filter or job_code_filter:
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
    display_columns = ['Final Job Title', 'PERNR', 'JOB_CODE', 'Division', 'Subdivision', 'Job Title']
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
            "PERNR": st.column_config.TextColumn(
                "PERNR",
                width="small",
                help="Employee ID"
            ),
            "JOB_CODE": st.column_config.TextColumn(
                "JOB_CODE",
                width="medium",
                help="Job Code"
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
            st.session_state.job_data = pd.DataFrame(
                columns=['Division', 'Subdivision', 'Job Title', 'Final Job Title', 'PERNR', 'JOB_CODE', 'Created']
            )
            st.success("All data cleared!")
            st.rerun()
else:
    # Empty state message
    st.markdown("""
    <div style="background-color: #F9FAFB; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;">
        <div style="font-size: 2rem; margin-bottom: 10px; color: #9CA3AF;">📋</div>
        <p style="font-size: 1.2rem; font-weight: 500; color: #4B5563; margin-bottom: 5px;">No Job Titles Yet</p>
        <p style="color: #6B7280;">Add your first job title using the form above or import from a CSV file.</p>
    </div>
    """, unsafe_allow_html=True)

# Add an example expander in the sidebar
with st.sidebar:
    with st.expander("Example Data Format"):
        st.markdown("""
        ### Expected Data Format
        Your CSV or space-separated file should contain these columns:
        ```
        PERNR JOB_TEXT DIVISION PSL SUBPSL SAL_BAND JOB_CODE
        105804 A409-ESG-Senior-Secretary Ancillary-Support ESG MGT ESG-MGT D3-ESG A409-ESG
        129403 R505-ESG-Account-Rep Drilling-&-Evaluation Wireline Business-Development J1-ESG R505-ESG
        ```
        
        The system will use:
        - PERNR as the employee ID
        - DIVISION as the Division
        - PSL as the Subdivision 
        - JOB_CODE for reference
        """)
        
        # Add sample data download option
        sample_data = """PERNR JOB_TEXT DIVISION PSL SUBPSL SAL_BAND JOB_CODE
105804 A409-ESG-Senior Secretary Ancillary Support ESG MGT ESG MGT D3-ESG A409-ESG
129403 R505-ESG-Account Rep Drilling & Evaluation Wireline Business Development J1-ESG R505-ESG
220457 BD14-ESG-Tech Prof Drilling & Evaluation Baroid Grinding & Tolling I3-ESG BD14-ESG"""
        
        st.download_button(
            "Download Sample Data",
            sample_data,
            "sample_job_data.txt",
            "text/plain",
            help="Download a sample file format"
        )