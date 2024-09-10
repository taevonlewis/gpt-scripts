import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('config.env')

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# File to store problem history and multi-part progress
HISTORY_FILE = "problem_history.json"
PROGRESS_FILE = "multipart_progress.json"

# Initialize the history and progress files if they don't exist
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({}, f)

def save_problem(problem, problem_type, part_type, style):
    """Saves the generated problem to the history file."""
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    history.append({
        "problem": problem,
        "problem_type": problem_type,
        "part_type": part_type,
        "style": style,
        "date": str(datetime.now())
    })

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def save_progress(problem_type, part_type, style, current_part, problem_statement=""):
    """Saves the current multi-part problem progress."""
    with open(PROGRESS_FILE, 'r') as f:
        progress = json.load(f)

    progress.update({
        "problem_type": problem_type,
        "part_type": part_type,
        "style": style,
        "current_part": current_part,
        "problem_statement": problem_statement
    })

    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=4)

def load_progress():
    """Loads the current multi-part problem progress."""
    with open(PROGRESS_FILE, 'r') as f:
        progress = json.load(f)
    return progress

def clear_progress():
    """Clears the current multi-part problem progress."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({}, f)

def get_problem_count(problem_type):
    """Returns the number of problems completed for a specific difficulty level."""
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    return len([entry for entry in history if entry['problem_type'] == problem_type])

def generate_problem(prompt):
    """Generates a problem using the OpenAI API based on the provided prompt."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in data structures and algorithms, generating real world technical interview problems focused on accessibility in iOS applications. The problem should use Swift syntax and should not include a solution."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def generate_new_problem():
    """Generates a new problem, saves it, and prints it out."""
    current_level = 'easy'
    levels = ['easy', 'medium', 'hard']

    while True:
        if get_problem_count(current_level) >= 5:
            next_level = levels[levels.index(current_level) + 1]
            if input(f"You've completed 5 {current_level} problems. Move to {next_level}? (y/n): ").lower() == 'y':
                current_level = next_level

        problem_type = current_level
        part_type = input("Enter problem type (single-part leetcode, multi-part leetcode, single-part real coding, multi-part real coding): ").lower()

        if part_type == "multi-part leetcode" or part_type == "multi-part real coding":
            current_part = 1
            prompt = f"Please create the first part of a real world {part_type} problem focused on {problem_type} challenges using data structures and algorithms related to accessibility in iOS applications. The problem should use Swift syntax and should not include a solution."
            problem = generate_problem(prompt)
            print(f"\nGenerated Problem:\n{problem}\n")
            save_problem(problem, problem_type, part_type, part_type)
            save_progress(problem_type, part_type, part_type, current_part, problem_statement=problem)
            multipart_menu()
        else:
            prompt = f"Please create a real world {part_type} problem focused on data structures and algorithms related to accessibility in iOS applications. The problem should use Swift syntax and should not include a solution."
            problem = generate_problem(prompt)
            print(f"\nGenerated Problem:\n{problem}\n")
            save_problem(problem, problem_type, part_type, part_type)

        if part_type == "single-part leetcode" or part_type == "single-part real coding" and input("Generate another problem? (y/n): ").lower() != 'y':
            break

def review_problems():
    """Displays a list of previously generated problems."""
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    if not history:
        print("No problems found in history.")
        return

    for i, entry in enumerate(history, 1):
        print(f"\nProblem {i}:")
        print(f"Type: {entry['problem_type']}, Part: {entry['part_type']}, Style: {entry['style']}, Date: {entry['date']}")
        print(f"Problem:\n{entry['problem']}\n")

def generate_next_part():
    """Generates the next part of the current multi-part problem."""
    progress = load_progress()
    if not progress:
        print("No multi-part problem in progress.")
        return

    current_part = progress["current_part"] + 1
    problem_type = progress["problem_type"]
    part_type = progress["part_type"]

    prompt = f"Please create part {current_part} of a real world {part_type} problem focused on {problem_type} challenges using data structures and algorithms related to accessibility in iOS applications. The problem should use Swift syntax and should not include a solution."
    problem = generate_problem(prompt)
    print(f"\nNext Part of the Problem:\n{problem}\n")

    save_problem(problem, problem_type, part_type, part_type)
    save_progress(problem_type, part_type, part_type, current_part, problem_statement=problem)

def multipart_menu():
    """Displays the multi-part problem menu and handles user input."""
    while True:
        print("\nMulti-Part Problem Menu")
        print("1. Generate the next part of the current problem")
        print("2. Exit to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            generate_next_part()
        elif choice == "2":
            break
        else:
            print("Invalid selection, please try again.")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\nMain Menu")
        print("1. Generate a New Problem")
        print("2. Review Past Problems")
        print("3. Continue Multi-Part Problem")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            generate_new_problem()
        elif choice == "2":
            review_problems()
        elif choice == "3":
            multipart_menu()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid selection, please try again.")

if __name__ == "__main__":
    main_menu()