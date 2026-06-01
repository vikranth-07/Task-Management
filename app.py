import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    task_name TEXT,
    priority TEXT,
    due_date TEXT,
    status TEXT
)
""")

conn.commit()

st.markdown("""
<style>

.stApp{
background:
linear-gradient(
135deg,
#ff0080,
#7928ca,
#0070f3,
#00dfd8
);

background-size:400% 400%;

animation:gradientBG 15s ease infinite;
}

@keyframes gradientBG{

0%{
background-position:0% 50%;
}

50%{
background-position:100% 50%;
}

100%{
background-position:0% 50%;
}

}

</style>
""",unsafe_allow_html=True)


st.title("📋 Smart Task Manager")

def register_user(username, password):
    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username,password)
        )
        conn.commit()
        return True
    except:
        return False

def login_user(username,password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    return cursor.fetchone()

def add_task(user, task, priority, due_date, status):

    cursor.execute(
        """
        INSERT INTO tasks
        (username,task_name,priority,due_date,status)
        VALUES(?,?,?,?,?)
        """,
        (user,task,priority,due_date,status)
    )

    conn.commit()

def get_tasks(user):

    cursor.execute(
        "SELECT * FROM tasks WHERE username=?",
        (user,)
    )

    return cursor.fetchall()

def update_task(task_id,status):

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status,task_id)
    )

    conn.commit()

def delete_task(task_id):

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()

menu = st.sidebar.selectbox(
    "Menu",
    ["Login","Register"]
)

if menu == "Register":

    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if register_user(username,password):
            st.success("Registration Successful")
        else:
            st.error("User Already Exists")




if menu == "Login":

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            username,
            password
        )

        if user:
            st.session_state["user"] = username
            st.success("Login Successful")




if "user" in st.session_state:

    user = st.session_state["user"]

    st.title("Task Dashboard")

    task = st.text_input("Task")

    priority = st.selectbox(
        "Priority",
        ["High","Medium","Low"]
    )

    due_date = st.date_input("Due Date")

    status = st.selectbox(
        "Status",
        ["Pending",
         "In Progress",
         "Completed"]
    )

    if st.button("Add Task"):

        add_task(
            user,
            task,
            priority,
            str(due_date),
            status
        )

        st.success("Task Added")



if "user" in st.session_state:

    user = st.session_state["user"]

    tasks = get_tasks(user)

    df = pd.DataFrame(
        tasks,
        columns=[
            "ID",
            "User",
            "Task",
            "Priority",
            "Due Date",
            "Status"
        ]
    )

    st.dataframe(df)


task_id = st.number_input(
    "Task ID",
    min_value=1
)

if st.button("Delete Task"):
    delete_task(task_id)
    st.success("Deleted")


update_id = st.number_input(
    "Update Task ID",
    min_value=1
)

new_status = st.selectbox(
    "New Status",
    ["Pending",
     "In Progress",
     "Completed"]
)

if st.button("Update"):
    update_task(update_id,new_status)
    st.success("Updated")
