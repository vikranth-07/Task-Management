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

def update_task(task_id, new_status):

    cursor.execute(
        """
        UPDATE tasks
        SET status = ?
        WHERE id = ?
        """,
        (new_status, task_id)
    )

    conn.commit()

    return cursor.rowcount

if st.button("Update Status"):
    rows = update_task(id,status)

    if rows > 0:
        st.success("Task Updated Successfully")
    else:
        st.error("Task ID Not Found")
        
        tasks = get_tasks(user)

tasks = get_tasks(user)

df = pd.DataFrame(
    tasks,
    columns=[
        "Task ID",
        "User",
        "Task",
        "Priority",
        "Due Date",
        "Status"
    ]
)

st.dataframe(df, use_container_width=True)

task_options = {
    f"{task[0]} - {task[2]}": task[0]
    for task in tasks
}

selected_task = st.selectbox(
    "Select Task",
    list(task_options.keys())
)

selected_id = task_options[selected_task]

new_status = st.selectbox(
    "Status",
    ["Pending", "In Progress", "Completed"]
)

if st.button("Update"):

    update_task(selected_id, new_status)

    st.success("Task Updated")

if st.button("Update"):

    update_task(selected_id, new_status)

    st.success("Updated")

    st.rerun()

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
