import json
import os
import random
import solution_evaluator
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

# Expanded lists for structures and algorithms
data_structures = [
    'arrays & hashing', 'two pointers', 'sliding window', 'stack', 'binary search', 
    'linked list', 'trees', 'heap/priority queue', 'tries', 'graphs', 'advanced graphs'
]

algorithms = [
    'recursion', 'dynamic programming', 'backtracking', 'sorting', 'searching', 
    'greedy', 'intervals', 'math & geometry', 'bit manipulation'
]

difficulty_levels = ['easy', 'medium', 'hard']

def clean_terminal_output(problem_text):
    """Cleans up problem text for terminal display by removing markdown formatting."""
    # Remove Markdown-specific syntax such as ```swift and math notations
    clean_text = problem_text.replace('```swift', '').replace('```', '').replace('\\(', '').replace('\\)', '')
    return clean_text

def save_problem_to_file(problem, problem_type, part_type, complexity):
    """Saves the generated problem to a markdown (.md) file."""
    file_name = f"generated_problem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(file_name, 'w') as f:
        f.write(f"# Problem: {part_type.capitalize()} Problem ({complexity.capitalize()})\n\n")
        f.write(f"**Problem Type**: {problem_type.capitalize()}\n\n")
        f.write(f"**Complexity**: {complexity.capitalize()}\n\n")
        f.write(f"**Generated Problem**:\n\n{problem}\n\n")

    print(f"Problem saved to file: {file_name}")

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
            {"role": "system", "content": "You are an expert in Apple iOS accessibility engineering. Create real-world technical interview problems covering all aspects of accessibility, including VoiceOver, Dynamic Type, color contrast, haptics, gestures, keyboard navigation, and other assistive technologies. The problem should use Swift syntax and should not include a solution."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def generate_new_problem(manual_difficulty=None):
    """Generates a new problem, saves it, and prints it out."""
    current_level = manual_difficulty if manual_difficulty else 'easy'

    if get_problem_count(current_level) >= 5 and not manual_difficulty:
        next_level = difficulty_levels[difficulty_levels.index(current_level) + 1]
        move_to_next = input(f"You've completed 5 {current_level} problems. Move to {next_level}? (y/n): ").lower()
        if move_to_next == 'y':
            current_level = next_level

    part_type = input("Enter problem type (single-part leetcode, multi-part leetcode, single-part real coding, multi-part real coding): ").lower()

    if "multi-part" in part_type:
        current_part = 1
        prompt = f"Please create the first part of a real-world {part_type} {current_level} problem focused on accessibility challenges in iOS applications. The problem should use or require {random.choice(data_structures)} and/or {random.choice(algorithms)} to solve a challenge related to accessibility. The problem should use Swift syntax and should not include a solution nor what data structure and/or algorithm to use since the interviewee has to infer on what to use."
        problem = generate_problem(prompt)
        clean_problem = clean_terminal_output(problem)
        print(f"\nGenerated Problem (Complexity: {current_level}):\n{clean_problem}\n")
        save_problem(problem, current_level, part_type, part_type)
        save_problem_to_file(problem, current_level, part_type, current_level)
        save_progress(current_level, part_type, part_type, current_part, problem_statement=problem)
        multipart_menu()
    else:
        prompt = f"Please create a real-world {part_type} {current_level} problem focused on accessibility challenges in iOS applications. The problem should use or require {random.choice(data_structures)} and/or {random.choice(algorithms)} to solve a challenge related to accessibility. The problem should use Swift syntax and should not include a solution nor what data structure and/or algorithm to use since the interviewee has to infer on what to use."
        problem = generate_problem(prompt)
        clean_problem = clean_terminal_output(problem)
        print(f"\nGenerated Problem (Complexity: {current_level}):\n{clean_problem}\n")
        save_problem(problem, current_level, part_type, part_type)
        save_problem_to_file(problem, current_level, part_type, current_level)

    if "single-part" in part_type and input("Generate another problem? (y/n): ").lower() != 'y':
        return

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

    prompt = f"Please create part {current_part} of a real-world {part_type} problem focused on {problem_type} challenges using data structures and algorithms related to accessibility in iOS applications. The problem should use Swift syntax and should not include a solution nor what data structure and/or algorithm to use since the interviewee has to infer on what to use."
    problem = generate_problem(prompt)
    clean_problem = clean_terminal_output(problem)
    print(f"\nNext Part of the Problem:\n{clean_problem}\n")

    save_problem(problem, problem_type, part_type, part_type)
    save_progress(problem_type, part_type, part_type, current_part, problem_statement=problem)
    save_problem_to_file(problem, problem_type, part_type, "multi-part")

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

def evaluate_swift_solution():
    """Submits a Swift solution from a .txt file for evaluation."""
    file_name = input("Enter the path to your Swift code .txt file: ")
    
    if not os.path.exists(file_name):
        print("File not found.")
        return

    with open(file_name, 'r') as file:
        swift_code = file.read()

    # Use the evaluate_swift_code function from the evaluator script
    feedback = solution_evaluator.evaluate_swift_code(swift_code)
    print("\nFeedback on your solution:\n", feedback)

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\nMain Menu")
        print("1. Generate a New Problem")
        print("2. Review Past Problems")
        print("3. Continue Multi-Part Problem")
        print("4. Submit a Swift Solution for Feedback")
        print("5. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            use_manual_difficulty = input("Do you want to manually choose a difficulty level? (y/n): ").lower()
            if use_manual_difficulty == 'y':
                difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
                generate_new_problem(difficulty)
            else:
                generate_new_problem()
        elif choice == "2":
            review_problems()
        elif choice == "3":
            multipart_menu()
        elif choice == "4":
            evaluate_swift_solution()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid selection, please try again.")

if __name__ == "__main__":
    main_menu()