
# 🤖 AI-Powered Text-to-SQL Assistant

An **AI-driven Streamlit application** that allows users to query a **SQLite database** in **natural language**.  
The app uses **Google Gemini (Generative AI)** to convert English questions into **valid SQL queries**, execute them, and present results with interactive charts and dashboards.

---

## ✨ Features

- 🔍 **Natural Language Query Assistant**
  - Ask questions in plain English
  - AI converts queries into **SQL**
  - View results in tables with CSV download option

- 🗄️ **Database Explorer**
  - Explore table schemas
  - Browse up to 100 rows of data
  - Quick stats on student, course, and enrollment data

- 📈 **Analytics Dashboard**
  - Interactive **Plotly charts**
  - KPIs like total students, average marks, top performer, etc.
  - Visuals for marks distribution, gender ratio, city-wise counts, age distribution

- 📜 **Query History**
  - Save executed queries with timestamps
  - Re-run queries directly from history
  - Clear history option

- ❓ **Help & Examples**
  - Guidance on query writing
  - Example queries
  - Tips for better results

---

## 🛠️ Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)  
- **Database:** SQLite (local file: `enhanced_student.db`)  
- **AI Model:** Google Gemini (via `google-generativeai`)  
- **Data Visualization:** Plotly (Express & Graph Objects)  
- **Language:** Python  

---

## 📂 Project Structure

```

.
├── enhanced_student.db      # SQLite database (auto-created with sample data)
├── app.py                   # Main Streamlit app file
├── .env                     # Environment variables (API keys)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

````

---

## ⚙️ Setup & Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/text-to-sql-assistant.git
cd text-to-sql-assistant
````

2. **Create virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Add API Key**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app will launch at **[http://localhost:8501](http://localhost:8501)**

---

## 📊 Sample Database Schema

### STUDENT

| Column          | Type    | Description        |
| --------------- | ------- | ------------------ |
| ID              | INTEGER | Primary Key        |
| NAME            | VARCHAR | Student name       |
| CLASS           | VARCHAR | Program/Class      |
| SECTION         | VARCHAR | Section identifier |
| MARKS           | INTEGER | Marks obtained     |
| AGE             | INTEGER | Student age        |
| GENDER          | VARCHAR | Gender             |
| CITY            | VARCHAR | City               |
| ENROLLMENT_DATE | DATE    | Enrollment date    |

### COURSES

| Column      | Type    | Description       |
| ----------- | ------- | ----------------- |
| COURSE_ID   | INTEGER | Primary Key       |
| COURSE_NAME | VARCHAR | Course title      |
| INSTRUCTOR  | VARCHAR | Course instructor |
| CREDITS     | INTEGER | Credit hours      |
| DEPARTMENT  | VARCHAR | Department name   |

### ENROLLMENTS

| Column        | Type    | Description                      |
| ------------- | ------- | -------------------------------- |
| ENROLLMENT_ID | INTEGER | Primary Key                      |
| STUDENT_ID    | INTEGER | Foreign Key → STUDENT(ID)        |
| COURSE_ID     | INTEGER | Foreign Key → COURSES(COURSE_ID) |
| GRADE         | VARCHAR | Grade obtained                   |
| SEMESTER      | VARCHAR | Semester name                    |

---

## 🧑‍💻 Example Queries

* "Show all students"
* "How many students are in each class?"
* "Students with marks above 90"
* "Average marks by class"
* "Top 5 students by marks"
* "Count of students by city"

---

## 📌 Future Improvements

* Support for **multiple databases**
* User authentication system
* Export results to **Excel / PDF**
* Deploy on **Streamlit Cloud / Hugging Face Spaces**

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* [Streamlit](https://streamlit.io/) for the web framework
* [Plotly](https://plotly.com/python/) for interactive charts
* [Google Gemini](https://ai.google.dev/) for natural language to SQL conversion

---

```

---


---

## 📬 Contact

**Hafiz Abdul Rehman**

- 📧 Email: hafizrehman3321@gmail.com
- 💼 LinkedIn: [Hafiz Abdul Rehman](https://linkedin.com/in/hafiz-abdul-rehman-9990ab329)
- 🐙 GitHub: [Abdul-Insighht](https://github.com/Abdul-Insighht)

---

## 🌟 Show Your Support

If you find this project helpful, please consider:

- ⭐ **Starring** this repository
- 🔄 **Sharing** with others
- 🐛 **Reporting** issues
- 💡 **Suggesting** improvements

---

<p align="center">Made with ❤️ by <b>Hafiz Abdul Rehman</b></p>
