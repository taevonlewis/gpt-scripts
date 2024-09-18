import openai
import os
from dotenv import load_dotenv

load_dotenv('config.env')

openai.api_key = os.getenv('OPENAI_API_KEY')

def evaluate_swift_code(problem_statement: str, swift_code: str):
    """Evaluates the provided Swift code based on the given problem statement, code correctness, optimality, and complexity."""
    
    messages = [
        {"role": "system", "content": "You are a coding assistant with expertise in Swift."},
        {"role": "user", "content": (
            "I will provide you with a Swift function and a problem statement. Please evaluate it based on the following: \n"
            "1. Solution Correctness: Is the solution correct according to the problem statement? If incorrect, provide a detailed explanation of why it's wrong.\n"
            "2. Optimization: If the solution is correct, evaluate if it is the most optimal in terms of time and space complexity. If not, suggest improvements.\n"
            "3. Complexity Analysis: Provide a clear time and space complexity analysis.\n"
            "4. Suggestions: If the solution is incorrect, provide alternative approaches to improve it without revealing the full solution.\n"
            "Avoid giving the full solution unless explicitly requested.\n\n"
            f"Problem Statement:\n{problem_statement}\n\nSwift Code:\n{swift_code}\n\n"
            "Please provide your evaluation in a structured format, with headers like 'Solution Correctness:', 'Optimization:', and 'Complexity Analysis:'."
        )}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    feedback = response.choices[0].message.content
    
    # print("\nFull API Response (for debugging):\n", feedback)

    feedback_lines = feedback.split('\n')
    filtered_feedback = []

    for line in feedback_lines:
        if ('Solution Correctness:' in line or 
            'Optimization:' in line or 
            'Complexity Analysis:' in line or 
            'Suggested improvements:' in line):
            filtered_feedback.append(line)

    return "\n".join(filtered_feedback)

def main():
    """Main function to run the evaluator."""
    
    with open('problem_statement.txt', 'r') as problem_file:
        problem_statement = problem_file.read()

    with open('swift_code.txt', 'r') as code_file:
        swift_code = code_file.read()

    while True:
        feedback = evaluate_swift_code(problem_statement, swift_code)
        print("\nFeedback:\n", feedback)
        
        print("\nOptions:")
        print("1. Do you have anything to ask?")
        print("2. Exit")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            question = input("What would you like to ask? ")
            print("\n")
            
            messages = [
                {"role": "system", "content": "You are a coding assistant."},
                {"role": "user", "content": question}
            ]
            
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