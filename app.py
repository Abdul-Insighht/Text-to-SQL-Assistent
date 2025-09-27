# from dotenv import load_dotenv
# load_dotenv() ## load all the environemnt variables

# import streamlit as st
# import os
# import sqlite3

# import google.generativeai as genai
# ## Configure Genai Key

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ## Function To Load Google Gemini Model and provide queries as response

# def get_gemini_response(question,prompt):
#     model=genai.GenerativeModel('gemini-2.0-flash-lite')
#     response=model.generate_content([prompt[0],question])
#     return response.text

# ## Fucntion To retrieve query from the database

# def read_sql_query(sql,db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
#     for row in rows:
#         print(row)
#     return rows

# ## Define Your Prompt
# prompt=[
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
#     SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
#     the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
#     \nExample 2 - Tell me all the students studying in Data Science class?, 
#     the SQL command will be something like this SELECT * FROM STUDENT 
#     where CLASS="Data Science"; 
#     also the sql code should not have ``` in beginning or end and sql word in output

#     """


# ]

# ## Streamlit App

# st.set_page_config(page_title="I can Retrieve Any SQL query")
# st.header("Gemini App To Retrieve SQL Data")

# question=st.text_input("Input: ",key="input")

# submit=st.button("Ask the question")

# # if submit is clicked
# if submit:
#     response=get_gemini_response(question,prompt)
#     print(response)
#     response=read_sql_query(response,"student.db")
#     st.subheader("The REsponse is")
#     for row in response:
#         print(row)
#         st.header(row)









import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI-Powered Text-to-SQL Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .info-box {
        background-color: #d1d5db;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
    }
</style>
""", unsafe_allow_html=True)

# Database functions
@st.cache_resource
def init_database():
    """Initialize the database with sample data"""
    conn = sqlite3.connect("enhanced_student.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STUDENT (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME VARCHAR(50),
            CLASS VARCHAR(50),
            SECTION VARCHAR(10),
            MARKS INTEGER,
            AGE INTEGER,
            GENDER VARCHAR(10),
            CITY VARCHAR(50),
            ENROLLMENT_DATE DATE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COURSES (
            COURSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            COURSE_NAME VARCHAR(50),
            INSTRUCTOR VARCHAR(50),
            CREDITS INTEGER,
            DEPARTMENT VARCHAR(50)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ENROLLMENTS (
            ENROLLMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            STUDENT_ID INTEGER,
            COURSE_ID INTEGER,
            GRADE VARCHAR(5),
            SEMESTER VARCHAR(20),
            FOREIGN KEY (STUDENT_ID) REFERENCES STUDENT(ID),
            FOREIGN KEY (COURSE_ID) REFERENCES COURSES(COURSE_ID)
        )
    """)
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM STUDENT")
    if cursor.fetchone()[0] == 0:
        # Insert sample data
        students_data = [
            ('Ali Ahmed', 'Data Science', 'A', 92, 22, 'Male', 'Karachi', '2023-01-15'),
            ('Sara Khan', 'Data Science', 'A', 88, 21, 'Female', 'Lahore', '2023-01-16'),
            ('Ahmed Hassan', 'Computer Science', 'B', 95, 23, 'Male', 'Islamabad', '2023-01-17'),
            ('Fatima Ali', 'Data Science', 'B', 87, 20, 'Female', 'Karachi', '2023-01-18'),
            ('Usman Malik', 'DevOps', 'A', 78, 24, 'Male', 'Lahore', '2023-01-19'),
            ('Ayesha Siddiq', 'Computer Science', 'A', 91, 22, 'Female', 'Islamabad', '2023-01-20'),
            ('Hassan Raza', 'DevOps', 'B', 65, 25, 'Male', 'Karachi', '2023-01-21'),
            ('Zainab Sheikh', 'Data Science', 'C', 94, 21, 'Female', 'Lahore', '2023-01-22'),
            ('Bilal Ahmad', 'Computer Science', 'C', 82, 23, 'Male', 'Islamabad', '2023-01-23'),
            ('Mariam Qureshi', 'DevOps', 'A', 89, 22, 'Female', 'Karachi', '2023-01-24')
        ]
        
        cursor.executemany("""
            INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, AGE, GENDER, CITY, ENROLLMENT_DATE)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, students_data)
        
        courses_data = [
            ('Introduction to Python', 'Dr. Smith', 3, 'Computer Science'),
            ('Machine Learning Basics', 'Dr. Johnson', 4, 'Data Science'),
            ('Database Management', 'Dr. Brown', 3, 'Computer Science'),
            ('Cloud Computing', 'Dr. Davis', 3, 'DevOps'),
            ('Statistics for Data Science', 'Dr. Wilson', 4, 'Data Science')
        ]
        
        cursor.executemany("""
            INSERT INTO COURSES (COURSE_NAME, INSTRUCTOR, CREDITS, DEPARTMENT)
            VALUES (?, ?, ?, ?)
        """, courses_data)
        
        conn.commit()
    
    conn.close()
    return "Database initialized successfully!"

def get_gemini_response(question, prompt):
    """Get response from Gemini AI model"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content([prompt, question])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

def execute_sql_query(sql, db_name="enhanced_student.db"):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(sql)
        
        if sql.strip().upper().startswith(('SELECT', 'WITH')):
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            return {"success": True, "data": rows, "columns": columns}
        else:
            conn.commit()
            conn.close()
            return {"success": True, "message": "Query executed successfully"}
            
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def get_table_schema():
    """Get database schema information"""
    try:
        conn = sqlite3.connect("enhanced_student.db")
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema_info[table_name] = columns
            
        conn.close()
        return schema_info
    except Exception as e:
        st.error(f"Error getting schema: {str(e)}")
        return {}

# AI Prompt
SQL_PROMPT = """
You are an expert in converting English questions to SQL queries!

The database contains the following tables:

1. STUDENT table with columns:
   - ID (INTEGER, PRIMARY KEY)
   - NAME (VARCHAR)
   - CLASS (VARCHAR) 
   - SECTION (VARCHAR)
   - MARKS (INTEGER)
   - AGE (INTEGER)
   - GENDER (VARCHAR)
   - CITY (VARCHAR)
   - ENROLLMENT_DATE (DATE)

2. COURSES table with columns:
   - COURSE_ID (INTEGER, PRIMARY KEY)
   - COURSE_NAME (VARCHAR)
   - INSTRUCTOR (VARCHAR)
   - CREDITS (INTEGER)
   - DEPARTMENT (VARCHAR)

3. ENROLLMENTS table with columns:
   - ENROLLMENT_ID (INTEGER, PRIMARY KEY)
   - STUDENT_ID (INTEGER, FOREIGN KEY)
   - COURSE_ID (INTEGER, FOREIGN KEY)
   - GRADE (VARCHAR)
   - SEMESTER (VARCHAR)

Instructions:
- Generate only valid SQLite SQL queries
- Do not include ``` or 'sql' in the response
- Use proper JOIN syntax when needed
- For aggregations, use appropriate GROUP BY clauses
- Return only the SQL query, nothing else

Examples:
- "How many students are there?" → SELECT COUNT(*) FROM STUDENT
- "Show all students in Data Science class" → SELECT * FROM STUDENT WHERE CLASS = 'Data Science'
- "Average marks by class" → SELECT CLASS, AVG(MARKS) as avg_marks FROM STUDENT GROUP BY CLASS
- "Students with marks above 90" → SELECT * FROM STUDENT WHERE MARKS > 90

"""

# Initialize the app
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Text-to-SQL Assistant</h1>', unsafe_allow_html=True)
    
    # Initialize database
    init_status = init_database()
    
    # Sidebar
    st.sidebar.title("🔧 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["Query Assistant", "Database Explorer", "Analytics Dashboard", "Query History", "Help & Examples"]
    )
    
    if page == "Query Assistant":
        query_assistant_page()
    elif page == "Database Explorer":
        database_explorer_page()
    elif page == "Analytics Dashboard":
        analytics_dashboard_page()
    elif page == "Query History":
        query_history_page()
    elif page == "Help & Examples":
        help_page()

def query_assistant_page():
    st.markdown('<h2 class="sub-header">💬 Natural Language Query Assistant</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <strong>How to use:</strong> Type your question in plain English and I'll convert it to SQL and execute it for you!
        </div>
        """, unsafe_allow_html=True)
        
        # Query input
        user_question = st.text_area(
            "Enter your question:",
            placeholder="e.g., Show me all students with marks above 90",
            height=100
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            execute_btn = st.button("🚀 Execute Query", type="primary")
        with col_btn2:
            clear_btn = st.button("🔄 Clear")
        
        if clear_btn:
            st.rerun()
        
        if execute_btn and user_question:
            with st.spinner("Converting to SQL and executing..."):
                # Get SQL from AI
                sql_query = get_gemini_response(user_question, SQL_PROMPT)
                
                if sql_query:
                    st.markdown("### Generated SQL Query:")
                    st.code(sql_query, language="sql")
                    
                    # Execute query
                    result = execute_sql_query(sql_query)
                    
                    if result["success"]:
                        if "data" in result:
                            st.markdown("### Query Results:")
                            if result["data"]:
                                df = pd.DataFrame(result["data"], columns=result["columns"])
                                st.dataframe(df, use_container_width=True)
                                
                                # Save to history
                                save_to_history(user_question, sql_query, len(result["data"]))
                                
                                # Download option
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    "📥 Download Results as CSV",
                                    csv,
                                    f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    "text/csv"
                                )
                            else:
                                st.info("Query executed successfully but returned no results.")
                        else:
                            st.success(result["message"])
                    else:
                        st.markdown(f"""
                        <div class="error-box">
                        <strong>Error executing query:</strong><br>
                        {result["error"]}
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quick Examples")
        examples = [
            "Show all students",
            "How many students are in each class?",
            "Students with marks above 85",
            "Average age of students by gender",
            "Top 5 students by marks",
            "Students from Karachi",
            "Count of students by city"
        ]
        
        for example in examples:
            if st.button(f"📝 {example}", key=f"ex_{example}"):
                st.session_state["example_query"] = example
                st.rerun()

def database_explorer_page():
    st.markdown('<h2 class="sub-header">🗄️ Database Explorer</h2>', unsafe_allow_html=True)
    
    # Get schema
    schema = get_table_schema()
    
    if schema:
        tab1, tab2, tab3 = st.tabs(["📋 Table Schema", "📊 Table Data", "📈 Quick Stats"])
        
        with tab1:
            for table_name, columns in schema.items():
                st.markdown(f"### {table_name} Table")
                col_df = pd.DataFrame(columns, columns=["Column ID", "Name", "Type", "Not Null", "Default", "Primary Key"])
                st.dataframe(col_df, use_container_width=True)
                st.divider()
        
        with tab2:
            selected_table = st.selectbox("Select table to view:", list(schema.keys()))
            if selected_table:
                result = execute_sql_query(f"SELECT * FROM {selected_table} LIMIT 100")
                if result["success"] and "data" in result:
                    df = pd.DataFrame(result["data"], columns=result["columns"])
                    st.dataframe(df, use_container_width=True)
                    st.info(f"Showing first 100 rows from {selected_table}")
        
        with tab3:
            # Quick statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                student_count = execute_sql_query("SELECT COUNT(*) FROM STUDENT")
                if student_count["success"]:
                    st.metric("Total Students", student_count["data"][0][0])
            
            with col2:
                course_count = execute_sql_query("SELECT COUNT(*) FROM COURSES")
                if course_count["success"]:
                    st.metric("Total Courses", course_count["data"][0][0])
            
            with col3:
                avg_marks = execute_sql_query("SELECT AVG(MARKS) FROM STUDENT")
                if avg_marks["success"]:
                    st.metric("Average Marks", f"{avg_marks['data'][0][0]:.1f}")

def analytics_dashboard_page():
    st.markdown('<h2 class="sub-header">📈 Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = execute_sql_query("SELECT COUNT(*) FROM STUDENT")
        if total_students["success"]:
            st.metric("👥 Total Students", total_students["data"][0][0])
    
    with col2:
        avg_marks = execute_sql_query("SELECT AVG(MARKS) FROM STUDENT")
        if avg_marks["success"]:
            st.metric("📊 Average Marks", f"{avg_marks['data'][0][0]:.1f}")
    
    with col3:
        top_performer = execute_sql_query("SELECT MAX(MARKS) FROM STUDENT")
        if top_performer["success"]:
            st.metric("🏆 Highest Marks", top_performer["data"][0][0])
    
    with col4:
        classes_count = execute_sql_query("SELECT COUNT(DISTINCT CLASS) FROM STUDENT")
        if classes_count["success"]:
            st.metric("🏫 Total Classes", classes_count["data"][0][0])
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Marks distribution by class
        marks_by_class = execute_sql_query("""
            SELECT CLASS, AVG(MARKS) as avg_marks, COUNT(*) as student_count 
            FROM STUDENT 
            GROUP BY CLASS
        """)
        
        if marks_by_class["success"]:
            df = pd.DataFrame(marks_by_class["data"], columns=["Class", "Average Marks", "Student Count"])
            fig = px.bar(df, x="Class", y="Average Marks", 
                        title="Average Marks by Class",
                        color="Average Marks",
                        color_continuous_scale="viridis")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gender distribution
        gender_dist = execute_sql_query("SELECT GENDER, COUNT(*) FROM STUDENT GROUP BY GENDER")
        if gender_dist["success"]:
            df = pd.DataFrame(gender_dist["data"], columns=["Gender", "Count"])
            fig = px.pie(df, values="Count", names="Gender", 
                        title="Student Distribution by Gender")
            st.plotly_chart(fig, use_container_width=True)
    
    # Additional charts
    col3, col4 = st.columns(2)
    
    with col3:
        # City distribution
        city_dist = execute_sql_query("SELECT CITY, COUNT(*) FROM STUDENT GROUP BY CITY")
        if city_dist["success"]:
            df = pd.DataFrame(city_dist["data"], columns=["City", "Count"])
            fig = px.bar(df, x="City", y="Count", 
                        title="Students by City",
                        color="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Age distribution
        age_dist = execute_sql_query("SELECT AGE, COUNT(*) FROM STUDENT GROUP BY AGE ORDER BY AGE")
        if age_dist["success"]:
            df = pd.DataFrame(age_dist["data"], columns=["Age", "Count"])
            fig = px.line(df, x="Age", y="Count", 
                         title="Age Distribution",
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)

def save_to_history(question, sql, result_count):
    """Save query to history"""
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "sql": sql,
        "result_count": result_count
    }
    
    st.session_state.query_history.insert(0, history_entry)
    
    # Keep only last 50 queries
    if len(st.session_state.query_history) > 50:
        st.session_state.query_history = st.session_state.query_history[:50]

def query_history_page():
    st.markdown('<h2 class="sub-header">📜 Query History</h2>', unsafe_allow_html=True)
    
    if "query_history" not in st.session_state or not st.session_state.query_history:
        st.info("No queries in history yet. Execute some queries to see them here!")
        return
    
    # Display history
    for i, entry in enumerate(st.session_state.query_history):
        with st.expander(f"🕐 {entry['timestamp']} - {entry['question'][:50]}..."):
            st.markdown(f"**Question:** {entry['question']}")
            st.code(entry['sql'], language="sql")
            st.markdown(f"**Results:** {entry['result_count']} rows returned")
            
            if st.button(f"Re-run Query", key=f"rerun_{i}"):
                result = execute_sql_query(entry['sql'])
                if result["success"] and "data" in result:
                    df = pd.DataFrame(result["data"], columns=result["columns"])
                    st.dataframe(df, use_container_width=True)
    
    # Clear history button
    if st.button("🗑️ Clear History", type="secondary"):
        st.session_state.query_history = []
        st.success("Query history cleared!")
        st.rerun()

def help_page():
    st.markdown('<h2 class="sub-header">❓ Help & Examples</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 How to Use", "💡 Example Queries", "🔧 Tips & Tricks"])
    
    with tab1:
        st.markdown("""
        ## How to Use This Application
        
        ### 1. Natural Language Queries
        Simply type your questions in plain English in the Query Assistant page. The AI will:
        - Convert your question to SQL
        - Execute the query
        - Display results in a table
        - Allow you to download results
        
        ### 2. Database Explorer
        - View table schemas and structures
        - Browse table data
        - See quick statistics about your database
        
        ### 3. Analytics Dashboard
        - View key metrics and KPIs
        - Explore data through interactive charts
        - Get insights about student performance
        
        ### 4. Query History
        - Review previously executed queries
        - Re-run past queries
        - Learn from SQL patterns
        """)
    
    with tab2:
        st.markdown("""
        ## Example Queries You Can Try
        
        ### Basic Queries
        - "Show me all students"
        - "How many students are there?"
        - "List students in Data Science class"
        
        ### Filtering & Conditions
        - "Students with marks above 90"
        - "Female students from Karachi"
        - "Students aged between 20 and 25"
        
        ### Aggregations & Statistics
        - "Average marks by class"
        - "Count of students by city"
        - "Highest marks in each section"
        - "Students grouped by gender"
        
        ### Advanced Queries
        - "Top 5 students by marks"
        - "Students enrolled after January 20, 2023"
        - "Class with the highest average marks"
        - "Age distribution of students"
        """)
    
    with tab3:
        st.markdown("""
        ## Tips for Better Results
        
        ### 🎯 Be Specific
        - Instead of "show students", try "show all students with their marks"
        - Use specific column names when possible
        
        ### 📊 For Analytics
        - Use words like "average", "count", "maximum", "minimum"
        - Ask for grouping: "by class", "by gender", "by city"
        
        ### 🔍 For Filtering
        - Use comparison words: "above", "below", "between", "equal to"
        - Be specific about conditions: "marks above 85", "age between 20 and 25"
        
        ### 📈 For Sorting
        - Use "top", "bottom", "highest", "lowest"
        - Specify number: "top 10 students", "bottom 5 performers"
        
        ### ⚠️ Common Issues
        - If query fails, try rephrasing your question
        - Check spelling of column names and values
        - Use the Database Explorer to understand table structure
        """)

if __name__ == "__main__":
    main()