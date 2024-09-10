# from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv('config.env')

openai.api_key = os.getenv('OPENAI_API_KEY')

def evaluate_swift_code(swift_code: str):
    messages = [
        {"role": "system", "content": "You are a coding assistant."},
        {"role": "user", "content": (
            "I will provide you with a Swift function. Evaluate it based on the following criteria: \n"
            "1. Is the solution correct? If it is, simply state 'Correct solution'. If the solution is incorrect, start with 'The solution is incorrect.' and then explain why it is not correct.\n"
            "2. If the solution is correct, evaluate if it is the most optimal time and space complexity solution. If it is, simply state 'The solution is optimal.' If it is not, explain why it is not optimal.\n"
            "If the solution is incorrect, indicate if the approach is moving towards an optimal  time and space complexity solution or not, and suggest the time and space complexity that should be aimed for if it is not.\n"
            "Do not provide the solution or examples unless explicitly requested.\n\n"
            f"Swift Code:\n{swift_code}\n\nProvide your evaluation:"
        )}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    feedback = response.choices[0].message.content
    
    # Post-process the feedback to trim unnecessary details
    feedback_lines = feedback.split('\n')
    filtered_feedback = []

    for line in feedback_lines:
        if 'Correct solution.' in line or 'The solution is incorrect.' in line or 'The solution is optimal.' in line:
            filtered_feedback.append(line)

    return "\n".join(filtered_feedback)

def main():
    with open('swift_code.txt', 'r') as file:
        swift_code = file.read()

    while True:
        feedback = evaluate_swift_code(swift_code)
        print("\nFeedback:\n", feedback)
        
        # Provide user options
        print("\nOptions:")
        print("1. Do you have anything to ask?")
        print("2. Exit")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            question = input("What would you like to ask? ")
            print("\n")
            
            # Create a message for the question
            messages = [
                {"role": "system", "content": "You are a coding assistant."},
                {"role": "user", "content": question}
            ]
            
            # Get the response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            answer = response.choices[0].message.content
            print(f"\nAnswer:\n{answer}\n")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()