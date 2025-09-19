import streamlit as st
import pymysql


# DB Connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="30_day_challenge",
    autocommit=True
)
cursor = conn.cursor()

st.title("💵 Expense Tracker")

mode = st.sidebar.radio("Select Mode", ["Track Expense", "List Expenses"])

if mode == "Track Expense":
    category = st.text_input("Enter Category")
    amount = st.number_input("Enter Amount", min_value=0)
    if st.button("Add Expense"):
        cursor.execute(
            "INSERT INTO expense_tracker(category,amount) VALUES(%s,%s);",
            (category, amount)
        )
        st.success("Expense Added ✅")

elif mode == "List Expenses":
    cursor.execute("SELECT * FROM expense_tracker")
    rows = cursor.fetchall()
    if rows:
        st.table(rows)
    else:
        st.info("No expenses found.")
