import streamlit as st
import pandas as pd
import sqlite3
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

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 30%,
        #334155 60%,
        #0f172a 100%
    );
    background-attachment: fixed;
}

/* Title */
h1, h2, h3 {
    color: #ffffff !important;
    text-align: center;
    font-family: 'Poppins', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Input Fields */
.stTextInput input,
.stSelectbox div,
.stDateInput input {
    border-radius: 12px !important;
    border: 2px solid #38bdf8 !important;
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 15px;
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
    color: white;
    font-size: 16px;
    font-weight: bold;
    border: none;
    padding: 10px;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 20px rgba(59,130,246,0.7);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 10px;
}

/* Glass Effect Cards */
.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0px 8px 32px rgba(0,0,0,0.3);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.25),
        rgba(6,182,212,0.25)
    );
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    color: white;
    font-weight: bold;
}

/* Success Message */
.stSuccess {
    border-radius: 12px;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

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
