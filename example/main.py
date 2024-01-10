import os

from dotenv import load_dotenv

from tutor import PersonalTutor

# Use a pipeline as a high-level helper

pt = PersonalTutor()


load_dotenv()

from rich.console import Console
from rich.table import Table


def main_menu():
    # Implementation of main menu
    pass

def start_session():
    console.print("Starting Learning Session...", style="bold green")
    pt.start_session()
    q = pt.get_current_question()
    console.print("Question: "+ q.question, style="bold blue")
    for (index, choice) in enumerate(q.choices):
        letter = chr(ord('A') + index)
        console.print(letter + ") " + choice, style="bold blue")
    # prompt user for answer
    answer = input("Enter your answer: ")
    # check answer index
    answer_index = ord(answer.upper()) - ord('A')
    if q.choices[answer_index] == q.correct:
        console.print("Correct!", style="bold green")
    else:
        console.print("Incorrect!", style="bold red")


def review_progress():
    # Implementation of progress review
    pass

# Initialize Console
console = Console()

def main():
    # Main loop
    while True:
        console.print("Welcome to Ultimate Personal Tutor", style="bold blue")
        console.print("[1] Start Learning Session\n[2] Review Progress\n[3] Settings\n[q] Quit", style="bold green")

        choice = input("Enter your choice: ")
        if choice == '1':
            start_session()
        elif choice == '2':
            review_progress()
        elif choice == 'q':
            break
        else:
            console.print("Invalid choice. Please try again.", style="bold red")

if __name__ == "__main__":
    main()
