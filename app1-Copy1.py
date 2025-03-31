import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API Key missing! Please add it to the .env file.")
    st.stop()

# Initialize OpenAI Chat Model
try:
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7, openai_api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"❌ OpenAI Initialization Error: {str(e)}")
    st.stop()



# Workout Plan Prompt Template
workout_prompt = PromptTemplate(
    input_variables=["age", "weight", "fitness_level", "goal", "duration", "equipment"],
    template=(
        "Create a personalized workout plan for a {age}-year-old individual weighing {weight} kg "
        "with a {fitness_level} fitness level. Their goal is {goal}, and they have {duration} minutes "
        "for each session using {equipment}. Provide step-by-step exercises with sets, reps, and rest intervals."
    ),
)

# Function to Generate Workout Plan
def generate_workout(age, weight, fitness_level, goal, duration, equipment):
    prompt = workout_prompt.format(
        age=age, weight=weight, fitness_level=fitness_level, goal=goal, duration=duration, equipment=equipment
    )
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to Create PDF
def create_pdf(workout_plan, age, weight, fitness_level, goal, duration, equipment):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Personalized Workout Plan", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Age: {age} years", ln=True)
    pdf.cell(200, 10, txt=f"Weight: {weight} kg", ln=True)
    pdf.cell(200, 10, txt=f"Fitness Level: {fitness_level}", ln=True)
    pdf.cell(200, 10, txt=f"Goal: {goal}", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {duration} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Equipment: {equipment}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, workout_plan)
    filename = f"Workout_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# AI Fitness Coach Chatbot
def fitness_chatbot(user_query):
    try:
        response = llm.invoke(f"You are a fitness coach. Answer this: {user_query}")
        return response.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit App
def main():
    st.title("🏋️‍♂️ AI-Powered Fitness Coach")
    st.sidebar.header("Enter Your Details")
    
    # User Inputs
    age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
    weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    fitness_level = st.sidebar.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    goal = st.sidebar.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"])
    duration = st.sidebar.number_input("Workout Duration (minutes)", min_value=10, max_value=120, value=30, step=5)
    equipment = st.sidebar.selectbox("Equipment Available", ["Bodyweight", "Dumbbells", "Gym Equipment", "Resistance Bands"])
    generate_button = st.sidebar.button("Generate Workout Plan")
    
    # Workout Plan Generation
    if generate_button:
        with st.spinner("Generating your workout plan..."):
            workout_plan = generate_workout(age, weight, fitness_level, goal, duration, equipment)
            st.subheader("Your Workout Plan")
            st.write(workout_plan)
            pdf_file = create_pdf(workout_plan, age, weight, fitness_level, goal, duration, equipment)
            with open(pdf_file, "rb") as file:
                st.download_button("Download as PDF", data=file, file_name=pdf_file, mime="application/pdf")
    
    # AI Chatbot
    st.subheader("💬 Chat with Your AI Fitness Coach")
    user_query = st.text_input("Ask a fitness-related question:")
    if st.button("Ask Coach"):
        with st.spinner("Fetching AI response..."):
            response = fitness_chatbot(user_query)
            st.write(response)

if __name__ == "__main__":
    main()
