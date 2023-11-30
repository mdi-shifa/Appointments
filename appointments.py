import streamlit as st
from datetime import datetime, timedelta
from csv import DictWriter
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
st.set_page_config(page_title="Healthcare Appointment", page_icon="👩‍⚕️", layout="centered", initial_sidebar_state="auto")

st.title("Healthcare Appointment Form")

conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="extracted_data", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

#Automation email 
sender_email = "healthcare.bot.pesu@gmail.com"
mail_pass = "hmjs vexa tciy wked"
subject = " Healthcare Appointment Confirmation"

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
        # Validation checks
        validation_passed = True

        if not patient_name:
            st.empty().warning("Please enter your full name.")
            validation_passed = False

        if not email:
            st.empty().warning("Email is mandatory. Please enter your email.")
            validation_passed = False

        if len(phone_number) != 10 or not phone_number.isdigit():
            st.empty().warning("Phone number should be 10 digits long and contain only numbers.")
            validation_passed = False

        if validation_passed:
            # Your backend logic to process the appointment here
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

            app_data = pd.DataFrame([data_dict])

            updated_df = pd.concat([existing_data, app_data], ignore_index=True)
            conn.update(worksheet="extracted_data", data=updated_df)
            st.success("Please Check the confirmation mail sent to your mail id")

            #Automation email 
            sender_email = "healthcare.bot.pesu@gmail.com"
            mail_pass = "hmjs vexa tciy wked"
            subject = " Healthcare Appointment Confirmation"

            # Sending email confirmation
            email_body = f"Dear {patient_name},\n\nThank you for scheduling an appointment with us.\n\nAppointment Details:\nDate: {preferred_date}\nTime: {preferred_time}\nDepartment: {department}\n\nWe look forward to seeing you!\n\nBest regards,\nThe Healthcare Team"

            em = EmailMessage()
            em["From"] = sender_email
            em["To"] = email
            em["Subject"] = subject
            em.set_content(email_body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smt:
                smt.login(sender_email, mail_pass)
                smt.sendmail(sender_email, email, em.as_string())
