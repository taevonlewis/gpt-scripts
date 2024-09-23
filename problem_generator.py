import solution_evaluator 
import json
import os
import random
import sys
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('config.env')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

HISTORY_FILE = "history-progress/problem_history.json"
PROGRESS_FILE = "history-progress/multipart_progress.json"
PROBLEMS_DIR = "problems"

for filename in [HISTORY_FILE, PROGRESS_FILE]:
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([] if filename == HISTORY_FILE else {}, f)

DATA_STRUCTURES = [
    'Arrays & Hashing', 'Two Pointers', 'Sliding Window', 'Stack', 'Binary Search',
    'Linked List', 'Trees', 'Heap/Priority Queue', 'Tries', 'Graphs', 'Advanced Graphs'
]

ALGORITHMS = [
    'Recursion', 'Dynamic Programming', 'Backtracking', 'Sorting', 'Searching',
    'Greedy', 'Intervals', 'Math & Geometry', 'Bit Manipulation'
]

DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard']

class ProblemGenerator:
    def __init__(self):
        self.history = self.load_history()
        self.progress = self.load_progress()
        self.current_difficulty = 'Easy'
    
        if not os.path.exists(PROBLEMS_DIR):
            os.makedirs(PROBLEMS_DIR)
        
    def load_history(self):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    
    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=4)
    
    def load_progress(self):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    
    def save_progress(self):
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, f, indent=4)
    
    def clear_progress(self):
        self.progress = {}
        self.save_progress()
    
    def generate_problem_prompt(self, part='single', style='leetcode', difficulty='Easy', part_number=1):
        data_structure = random.choice(DATA_STRUCTURES)
        algorithm = random.choice(ALGORITHMS)
        base_prompt = (
            f"Create a {difficulty} {style} {part}-part problem focusing on iOS accessibility. "
            f"The problem should involve {data_structure} and {algorithm}, and be relevant to real-world scenarios. "
            f"Use Swift syntax and do not provide a solution."
        )
        if part == 'multi' and part_number > 1:
            base_prompt += f" This is part {part_number} of the problem, building upon the previous parts."
        return base_prompt
    
    def call_openai_api(self, prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": (
                        "You are an expert in Apple iOS accessibility engineering. "
                        "Create real-world technical interview problems covering all aspects of accessibility, "
                        "including VoiceOver, Dynamic Type, color contrast, haptics, gestures, keyboard navigation, "
                        "and other assistive technologies. Use Swift syntax and do not include a solution."
                        "**Format the problem description in markdown, following LeetCode's style, including code blocks for code snippets and proper headings.**"
                    )},
                    {"role": "user", "content": prompt}
                ],
                # max_tokens=1000,
                n=1,
                stop=None,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
    
    # def clean_text(self, text):
    #     return text.replace('```swift', '').replace('```', '').replace('\\(', '').replace('\\)', '')
    
    def save_problem_to_file(self, problem, filename):
        try:
            difficulty_dir = os.path.join(PROBLEMS_DIR, self.current_difficulty.lower())
            if not os.path.exists(difficulty_dir):
                os.makedirs(difficulty_dir)
            
            file_path = os.path.join(difficulty_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(problem)
            print(f"Problem saved to file: {file_path}")
        except Exception as e:
            print(f"Error saving problem to file: {e}")
    
    def add_problem_to_history(self, problem_entry):
        self.history.append(problem_entry)
        self.save_history()
    
    def generate_new_problem(self):
        manual_choice = input("Do you want to select a difficulty level? (y/n): ").strip().lower()
        if manual_choice == 'y':
            difficulty = input("Choose difficulty (Easy, Medium, Hard): ").strip().capitalize()
            if difficulty not in DIFFICULTY_LEVELS:
                print("Invalid difficulty level selected. Defaulting to Easy.")
                difficulty = 'Easy'
            self.current_difficulty = difficulty
        else:
            problem_counts = {level: 0 for level in DIFFICULTY_LEVELS}
            for entry in self.history:
                problem_counts[entry['difficulty']] += 1
            if problem_counts[self.current_difficulty] >= 5:
                next_index = DIFFICULTY_LEVELS.index(self.current_difficulty) + 1
                if next_index < len(DIFFICULTY_LEVELS):
                    self.current_difficulty = DIFFICULTY_LEVELS[next_index]
                    print(f"Moving to {self.current_difficulty} problems.")
        
        part_type = input("Select problem type (single-part, multi-part): ").strip().lower()
        style = input("Select style (leetcode, real-world): ").strip().lower()
        
        if part_type not in ['single-part', 'multi-part'] or style not in ['leetcode', 'real-world']:
            print("Invalid selection. Please try again.")
            return
        
        part = 'single' if part_type == 'single-part' else 'multi'
        part_number = 1
        
        prompt = self.generate_problem_prompt(part=part, style=style, difficulty=self.current_difficulty, part_number=part_number)
        problem = self.call_openai_api(prompt)
        
        if problem:
            # clean_problem = self.clean_text(problem)
            clean_problem = problem
            
            print(f"\nGenerated Problem ({self.current_difficulty}):\n{clean_problem}\n")
            
            title = self.extract_problem_title(clean_problem)
            formatted_title = self.format_title_for_filename(title)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{formatted_title}_{timestamp}.md"
            
            self.save_problem_to_file(clean_problem, filename)
            
            problem_entry = {
                "problem": clean_problem,
                "difficulty": self.current_difficulty,
                "part_type": part_type,
                "style": style,
                "timestamp": timestamp,
                "filename": filename
            }
            self.add_problem_to_history(problem_entry)
            
            if part == 'multi':
                self.progress = {
                    "current_part": part_number,
                    "part_type": part_type,
                    "style": style,
                    "difficulty": self.current_difficulty,
                    "problem_history": [problem_entry]
                }
                self.save_progress()
                self.multi_part_menu()
        else:
            print("Failed to generate problem. Please try again.")
    
    def generate_next_part(self):
        if not self.progress:
            print("No multi-part problem in progress.")
            return
        
        self.progress['current_part'] += 1
        part_number = self.progress['current_part']
        prompt = self.generate_problem_prompt(
            part='multi',
            style=self.progress['style'],
            difficulty=self.progress['difficulty'],
            part_number=part_number
        )
        problem = self.call_openai_api(prompt)
        
        if problem:
            clean_problem = self.clean_text(problem)
            
            print(f"\nGenerated Part {part_number}:\n{clean_problem}\n")
            
            title = self.extract_problem_title(clean_problem)
            formatted_title = self.format_title_for_filename(f"{title}-part-{part_number}")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{formatted_title}_{timestamp}.md"
            
            self.save_problem_to_file(clean_problem, filename)
            
            problem_entry = {
                "problem": clean_problem,
                "difficulty": self.progress['difficulty'],
                "part_type": self.progress['part_type'],
                "style": self.progress['style'],
                "timestamp": timestamp,
                "filename": filename
            }
            self.progress['problem_history'].append(problem_entry)
            self.add_problem_to_history(problem_entry)
            self.save_progress()
        else:
            print("Failed to generate the next part. Please try again.")
    
    def multi_part_menu(self):
        while True:
            print("\nMulti-Part Problem Menu")
            print("1. Generate Next Part")
            print("2. Return to Main Menu")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.generate_next_part()
            elif choice == '2':
                break
            else:
                print("Invalid selection. Please try again.")
    
    def review_problems(self):
        if not self.history:
            print("No problems to review.")
            return
        for idx, entry in enumerate(self.history, 1):
            print(f"\nProblem {idx} ({entry['difficulty']} - {entry['part_type']} - {entry['style']}):")
            print(f"Timestamp: {entry['timestamp']}")
            print(f"Filename: {entry['filename']}")
            print(f"Problem:\n{entry['problem']}\n")
    
    def extract_problem_title(self, problem_content):
        lines = problem_content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                title = line.strip('#').strip()
                return title
        return 'Untitled Problem'

    def format_title_for_filename(self, title):
        title = title.lower()
        title = re.sub(r'[^a-z0-9]+', '-', title)
        title = title.strip('-')
        return title
    
    def evaluate_solution(self):
        file_name = input("Enter the path to your Swift code .txt file: ")
        
        if not os.path.exists(file_name):
            print("File not found.")
            return
    
        with open(file_name, 'r') as file:
            swift_code = file.read()
            
        feedback = solution_evaluator.evaluate_swift_code(swift_code)
        print("\nFeedback oon your solution:\n", feedback)
    
    def main_menu(self):
        while True:
            print("\nMain Menu")
            print("1. Generate New Problem")
            print("2. Review Past Problems")
            print("3. Continue Multi-Part Problem")
            print("4. Evaluate Solution")
            print("5. Exit")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.generate_new_problem()
            elif choice == '2':
                self.review_problems()
            elif choice == '3':
                self.multi_part_menu()
            elif choice == '4':
                self.evaluate_solution()
            elif choice == '5':
                print("Exiting. Good luck with your preparation!")
                sys.exit()
            else:
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    generator = ProblemGenerator()
    generator.main_menu()