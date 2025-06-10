import streamlit as st
from langchain_community.utilities import SQLDatabase
import pyodbc
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

# Streamlit page configuration
st.set_page_config(page_title="SQL Chat Assistant", layout="wide")
st.title("Chat Assistant")
st.markdown("Ask questions about database get Answers")

# Define the connection string for pyodbc
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-HAC0TP3\\SQLEXPRESS;"
    "Database=emp;"
    "UID=sa;"
    "PWD=7825992918;"
    "TrustServerCertificate=yes;"
)

# Define the SQLAlchemy URI for LangChain
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:7825992918@DESKTOP-HAC0TP3\\SQLEXPRESS/Emp?driver=ODBC+Driver+17+for+SQL+Server"

# Initialize database connection
@st.cache_resource
def init_db():
    try:
        db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
        return db
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        print(f"Error connecting to the database: {e}")
        return None

# Initialize LLM
llm = ChatOllama(model="llama3")

# Function to get database schema
def get_database_schema(db):
    try:
        return db.get_table_info()
    except Exception as e:
        return f"Error retrieving schema: {e}"

# Function to generate SQL query from user question
def get_query_from_llm(question, schema):
    template = """Below is the schema of a SQL Server database. Read the schema carefully, paying attention to table and column names, and respect case sensitivity. Answer the user's question with a SQL query.

    {schema}

    Provide only the SQL query, nothing else.

    Examples:
    question: How many employees are in the database?
    SQL query: SELECT COUNT(*) FROM Employee
    question: How many employees are in the Production department?
    SQL query: SELECT COUNT(*) FROM Employee WHERE Dept = 'Production'
    Question: How many employees are in the Sales department?
    SQL query: SELECT COUNT(*) FROM Employee WHERE Dept = 'Sales'
    Question: Max Salary of employees in the database?
    SQL query: SELECT MAX(Salary) FROM Employee;
    Question: Who are earning more than 5000 in the database? 
    SQL query: SELECT * FROM Employee WHERE Salary > 5000;  
    Question: How many employees are in the Marketing department?
    SQL query: SELECT COUNT(*) FROM Employee WHERE Dept = 'Marketing';
    Your turn:
    question: {question}
    SQL query:
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "schema": schema
    })
    return response.content

# Function to generate natural language response and follow-up questions
def get_response_and_followup(question, query, result, schema):
    template = """Below is the schema of a SQL Server database. Read the schema carefully, paying attention to table and column names. Write a natural language response based on the user's question and the query result. Additionally, provide 2 follow-up questions that the user might be interested in to encourage further exploration of the database.

    {schema}

    Examples:
    question: How many employees are in the database?
    SQL query: SELECT COUNT(*) FROM Employee;
    Result: [(50,)]
    Response: There are 50 employees in the database.
    Follow-up questions:
    1. Would you like to know how many employees are in a specific department?
    2. Are you interested in the total salary of all employees?

    question: How many employees are in the Sales department?
    SQL query: SELECT COUNT(*) FROM Employee WHERE Dept='Sales';
    Result: [(10,)]
    Response: There are 10 employees in the Sales department.
    Follow-up questions:

    Question: Max Salary of employees in the database?
    SQL query: SELECT MAX(Salary) FROM Employee;
    Result: [(5000,)]
    Response: The maximum salary of employees in the database is 5000.

    Question: Who are earning more than 5000 in the database? 
    SQL query: SELECT * FROM Employee WHERE Salary > 5000; 
    Result: [(1, 'John', 'Sales', 6000), (2, 'Jane', 'Marketing', 7000), (3, 'Doe', 'Production', 8000)]
    Response: There are several employees earning more than 5000 in the database, including John, Jane, and Doe. 

    Question: How many employees are in the Marketing department?
    SQL query: SELECT COUNT(*) FROM Employee WHERE Dept = 'Marketing';
    Result: [(10,)]
    Response: There are 10 employees in the Marketing department.

    Follow-up questions:
    1. Would you like to know the names of employees in the Sales department?
    2. Are you interested in the average salary for these employees?
    3. Would you like to see the details of employees earning more than 5000?
    4. Are you interested in the total salary of all employees earning more than 5000?
    5. Would you like to know how many employees are in each department?
    

    Your turn:
    question: {question}
    SQL query: {query}
    Result: {result}
    Response:
    Follow-up questions:
    1.
    2.
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "schema": schema,
        "query": query,
        "result": result
    })
    return response.content

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main app logic
def main():
    db = init_db()
    if not db:
        return

    # Get database schema
    schema = get_database_schema(db)
    if "Error" in schema:
        st.error(schema)
        return

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input via chat input
    if question := st.chat_input("Ask a question about the Employee database (e.g., How many employees are in the Sales department?)"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate and process response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Generate SQL query
                    sql_query = get_query_from_llm(question, schema)

                    # Execute query
                    result = db.run(sql_query)

                    # Generate natural language response and follow-up questions
                    response = get_response_and_followup(question, sql_query, result, schema)

                    # Display response
                    st.markdown(response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = f"Sorry, I couldn't process that request. Error: {str(e)}"
                    st.markdown(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()