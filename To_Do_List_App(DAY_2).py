import streamlit as st
import pymysql


# DB Connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="YOUR PASSWORD",
    database="30_day_challenge",
    autocommit=True
)
cursor = conn.cursor()

st.title("To do list app")
task = st.text_input("Enter the task")
sub = st.button("Submit Task")

if sub:
    cursor.execute(
        "INSERT INTO to_do_list(task, status) VALUES (%s, %s)",
        (task, False)  # or "False" if column is VARCHAR
    )
    st.success("Task added successfully")
    st.rerun()

st.title("Pending Tasks")
if "refresh" not in st.session_state:
    st.session_state.refresh = 0

cursor.execute("SELECT id, task FROM to_do_list WHERE status=0")
rows = cursor.fetchall()
for r in rows:
    task_id, task_text = r
    if st.checkbox(task_text, key=task_id):
        cursor.execute("UPDATE to_do_list SET status = 1 WHERE id = %s", (task_id,))
        st.balloons()
        # st.experimental_rerun()

        st.session_state["refresh"] += 1

st.title("Done Task")

cursor.execute("SELECT task FROM to_do_list WHERE status=1")
rows = cursor.fetchall()
for r in rows:
    st.markdown(str(f"~~{r[0]}~~"))

clear = st.button("Clear")
if clear:
    cursor.execute("TRUNCATE TABLE to_do_list;")
    st.session_state["refresh"] += 1

