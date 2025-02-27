
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
import streamlit as st

# Load the text data
file_path = 'official_ chatbot.csv'
text_data = pd.read_csv(file_path)

# Initialize the OpenAI model
# Set your OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize the LLM
llm = OpenAI(api_key=api_key)

# Define the prompt template for health statistics data
prompt_template = PromptTemplate(
    input_variables=["data_description", "question"],
    template="""
    You are a chatbot for Sir Lester Bird Medical Center, who is very empathetic and professional.You complete all your sentences. You keep all your answers four lines long. You give information concerning only Antigua and Barbuda.You have access to the following surgery data:
    {data_description}

    Question: {question}

    Please provide a detailed answer based on the data.
    """
)

# Create the LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Function to generate data description for the health statistics
def generate_data_description():
    sample_entries = text_data.sample(min(len(text_data), 5))  # Get up to 5 random rows
    description = "The dataset contains various info on the SLBMC surgery types over different years. It includes data points such as Surgery options, Surgery pricing, Preparation for surgeries, and Reasons why surgeries are done. The data is structured with the following columns:\n"
    description += "- Keywords: The word which provides the info on surgeries .\n"
    description += "- Responses: The info on surgeries.\n"
    description += "Example entries:\n"
    description += "\n".join(f"Keywords {row['Keywords:']}, Responses {row['Responses:']}," for _, row in sample_entries.iterrows())
    return description

def get_response(question):
    data_description = generate_data_description()
    response = chain.run(data_description=data_description, question=question)
    return response

# Allow for dynamic input via user prompt
if __name__ == "__main__":
    while True:
        user_question = input("Please enter your question or type 'exit' to quit: ")
        if user_question.lower() == 'exit':
            break
        answer = get_response(user_question)
        print("Answer:", answer)
