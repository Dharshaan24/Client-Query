import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from utils.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

st.title("Client Query Management System")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

if choice == "Register":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    role = st.selectbox("Role", ["Client", "Support"])

    if st.button("Register"):
        cursor.execute('INSERT INTO users(username, hashed_password, role) VALUES (?, ?, ?)', 
                       (username, make_hashes(password), role))
        conn.commit()
        st.success("Account created successfully! You can now login.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user and check_hashes(password, user[1]):
            role = user[2]
            st.success(f"Logged in as {role}")

            if role == "Client":
                st.header("Submit a Query")
                mail = st.text_input("Email ID")
                mobile = st.text_input("Mobile Number")
                heading = st.text_input("Query Heading")
                desc = st.text_area("Query Description")
                if st.button("Submit Query"):
                    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute('''INSERT INTO queries(mail_id, mobile_number, query_heading, query_description, status, query_created_time)
                                      VALUES (?, ?, ?, ?, "Open", ?)''', 
                                   (mail, mobile, heading, desc, created_time))
                    conn.commit()
                    st.success("Query submitted successfully!")

            elif role == "Support":
                st.header("Manage Queries")
                df = pd.read_sql_query("SELECT * FROM queries", conn)
                status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
                if status_filter != "All":
                    df = df[df['status'] == status_filter]
                st.dataframe(df)

                query_id = st.number_input("Enter Query ID to Close", step=1)
                if st.button("Close Query"):
                    closed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute('UPDATE queries SET status = "Closed", query_closed_time = ? WHERE query_id = ?', 
                                   (closed_time, query_id))
                    conn.commit()
                    st.success(f"Query {query_id} closed successfully!")

        else:
            st.error("Invalid Username or Password")
