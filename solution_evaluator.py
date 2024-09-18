import openai
import os
from dotenv import load_dotenv

# Load the OpenAI API key from the environment variable
load_dotenv('config.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

def evaluate_swift_code(problem_statement: str, swift_code: str):
    """
    Evaluates the provided Swift code based on the given problem statement,
    checking for correctness, optimality, and complexity.
    """
    # Define the messages for the assistant
    messages = [
        {
            "role": "system",
            "content": "You are an expert coding assistant proficient in Swift and algorithm analysis."
        },
        {
            "role": "user",
            "content": (
                "I will provide you with a Swift function and a problem statement. Evaluate it based on the following criteria:\n\n"
                "1. **Correctness**: Is the solution correct based on the problem statement? If it is correct, state 'Correct solution.'. If the solution is incorrect, start with 'The solution is incorrect.' and then explain in detail why it is not correct based on the problem requirements.\n\n"
                "2. **Optimality**: If the solution is correct, evaluate whether it has the most optimal time and space complexity. If it is optimal, state 'The solution is optimal.'. If it is not, explain why it is not optimal and suggest potential improvements without revealing the full solution.\n\n"
                "3. **Time and Space Complexity**: Provide a time and space complexity analysis and suggest improvements if necessary.\n\n"
                "Please structure your evaluation using the following headings:\n"
                "- **Correctness**\n"
                "- **Optimality**\n"
                "- **Time and Space Complexity**\n\n"
                f"**Problem Statement**:\n{problem_statement}\n\n**Swift Code**:\n{swift_code}\n\nProvide your evaluation:"
            )
        }
    ]
    
    # Call the OpenAI API with deterministic settings
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0  # Setting temperature to 0 for deterministic output
    )
    
    # Extract the assistant's reply
    feedback = response.choices[0].message.content.strip()
    
    # Parse the assistant's feedback
    evaluation = parse_feedback(feedback)
    
    return evaluation

def parse_feedback(feedback: str):
    """
    Parses the assistant's feedback and extracts information about correctness,
    optimality, and time/space complexity.
    """
    evaluation = {
        'Correctness': '',
        'Optimality': '',
        'Time and Space Complexity': ''
    }
    
    # Split the feedback into lines
    lines = feedback.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('**Correctness**'):
            current_section = 'Correctness'
            continue
        elif line.startswith('**Optimality**'):
            current_section = 'Optimality'
            continue
        elif line.startswith('**Time and Space Complexity**'):
            current_section = 'Time and Space Complexity'
            continue
        elif line.startswith('**'):
            current_section = None  # Unknown section
            continue
        
        if current_section and line:
            evaluation[current_section] += line + ' '
    
    # Trim extra spaces
    for key in evaluation:
        evaluation[key] = evaluation[key].strip()
    
    return evaluation

def main():
    """Main function to run the evaluator."""
    
    # Read problem statement from file
    with open('problem_statement.txt', 'r') as problem_statement:
        problem_statement = problem_statement.read()

    # Read Swift code from file
    with open('swift_code.txt', 'r') as swift_code:
        swift_code = swift_code.read()

    while True:
        # Pass both the problem statement and the Swift code to the evaluator
        evaluation = evaluate_swift_code(problem_statement, swift_code)
        
        # Display the evaluation results
        print("\nEvaluation Results:")
        print("\n**Correctness**\n")
        print(evaluation['Correctness'])
        print("\n**Optimality**\n")
        print(evaluation['Optimality'])
        print("\n**Time and Space Complexity**\n")
        print(evaluation['Time and Space Complexity'])
        
        # Provide user options
        print("\nOptions:")
        print("1. Ask a follow-up question")
        print("2. Exit")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            question = input("Please enter your question: ")
            print("\n")
            
            # Create a message for the question
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert coding assistant proficient in Swift and algorithm analysis."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
            
            # Get the response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0  # Deterministic output
            )
            
            answer = response.choices[0].message.content.strip()
            print(f"\nAnswer:\n{answer}\n")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()