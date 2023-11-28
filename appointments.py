import streamlit as st
from datetime import datetime, timedelta
from csv import DictWriter
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Healthcare Appointment", page_icon="👩‍⚕️", layout="centered", initial_sidebar_state="auto")

st.title("Healthcare Appointment Form")

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="extracted_data", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Patient Information
with st.form(key="app_form"):
    with st.expander("Patient Information"):
        patient_name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=150, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

# Contact Information
    with st.expander("Contact Information"):
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")

# Appointment Details
    with st.expander("Appointment Details"):
        today = datetime.today().date()
        max_date = today + timedelta(days=365 * 10)  # Maximum date is set to 10 years from today
        min_date = today + timedelta(days=1)  # Minimum date is set to tomorrow
        preferred_date = st.date_input("Preferred Date", min_value=today, format="DD/MM/YYYY")
        preferred_time = st.time_input("Preferred Time")
        department = st.selectbox("Department", ["Cardiology", "Dermatology", "Orthopedics", "Neurology", "Other"])

# Additional Information
    additional_info = st.text_area("Additional Information or Questions")
    submit_button = st.form_submit_button(label ="Submit Appointment details")

# Submit Button
if submit_button:
    # Check if the selected date is in the past
    if preferred_date < today:
        st.warning("Please select a date in the future for your appointment.")
    else:
        # You can add your backend logic to process the appointment here
        st.success("Appointment submitted successfully! We will contact you shortly.")


        # Saving the form data into a csv file
        column_names = ["Patient Name", "Age", "Gender", "Email", "Phone Number", "Appointment Date", "Time", "Department", "Queries"]
        data_dict = {
            "Patient Name": patient_name,
            "Age": age,
            "Gender": gender,
            "Email": email,
            "Phone Number": phone_number,
            "Appointment Date": preferred_date,
            "Time": preferred_time,
            "Department": department,
            "Queries": additional_info
        }
        
        app_data =pd.DataFrame(
            
            [{
            "Patient Name": patient_name,
            "Age": age,
            "Gender": gender,
            "Email": email,
            "Phone Number": phone_number,
            "Appointment Date": preferred_date,
            "Time": preferred_time,
            "Department": department,
            "Queries": additional_info
        }
            ])

        updated_df =pd.concat([existing_data, app_data], ignore_index =True)
        conn.update(worksheet="extracted_data", data=updated_df)
        st.success("Your appointment is succesfully scheduled")


        
       
