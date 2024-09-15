import tkinter as tk
import random

# Initialize the main window
root = tk.Tk()
root.title("Math Game for Primary School")

# Global variables to keep track of the game state
current_answer = None
current_player = None
scores = {1: 0, 2: 0}
buzzed_in = False
WIN_SCORE = 12  # The score needed to win the game
countdown_in_progress = False  # Indicates if countdown is happening

# Function to generate a new question
def generate_question():
    global current_answer, buzzed_in, current_player, countdown_in_progress
    buzzed_in = False
    current_player = None
    # Disable choice buttons
    for btn in choice_buttons:
        btn.config(state=tk.DISABLED, bg="SystemButtonFace")
    # Clear feedback message
    feedback_label.config(text="")
    # Generate two random numbers
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    # Randomly choose an operation
    operation = random.choice(['+', '-', '×', '÷'])
    # Compute the correct answer
    if operation == '+':
        current_answer = num1 + num2
    elif operation == '-':
        current_answer = num1 - num2
    elif operation == '×':
        current_answer = num1 * num2
    elif operation == '÷':
        # Ensure division is exact
        num1 = num1 * num2  # Make num1 a multiple of num2
        current_answer = num1 // num2
    # Update the question label
    question_text = f"{num1} {operation} {num2} = ?"
    question_label.config(text=question_text)
    # Generate two incorrect answers
    wrong_answers = set()
    while len(wrong_answers) < 2:
        wrong_answer = current_answer + random.randint(-10, 10)
        if wrong_answer != current_answer:
            wrong_answers.add(wrong_answer)
    all_answers = list(wrong_answers) + [current_answer]
    random.shuffle(all_answers)
    # Assign answers to choice buttons
    for i, btn in enumerate(choice_buttons):
        btn.config(text=str(all_answers[i]))
    # Start countdown before players can buzz in
    countdown_in_progress = True
    countdown(3)  # Start countdown from 3

# Countdown function
def countdown(count):
    global countdown_in_progress
    if count > 0:
        status_label.config(text=f"Get ready... {count}")
        root.after(1000, countdown, count - 1)
    else:
        countdown_in_progress = False
        status_label.config(text="Press 'Q' (Player 1) or 'P' (Player 2) to buzz in.")

# Function to handle buzz-in
def buzz_in(player):
    global buzzed_in, current_player
    if not buzzed_in and not countdown_in_progress:
        buzzed_in = True
        current_player = player
        # Enable choice buttons
        for btn in choice_buttons:
            btn.config(state=tk.NORMAL)
            # Change button background color based on the player
            if current_player == 1:
                btn.config(bg="light blue")
            else:
                btn.config(bg="light coral")
        # Update status label
        status_label.config(text=f"Player {current_player} buzzed in! Choose your answer.")

# Function to handle answer selection
def select_choice(index):
    global scores
    selected_answer = int(choice_buttons[index].cget('text'))
    if selected_answer == current_answer:
        # Correct
        feedback_label.config(text=f"Player {current_player} is correct!", fg="green")
        scores[current_player] += 1
    else:
        # Incorrect
        feedback_label.config(text=f"Player {current_player} is incorrect!", fg="red")
    # Update scores
    score_label.config(text=f"Player 1: {scores[1]}    Player 2: {scores[2]}")
    # Check for win condition
    if scores[current_player] >= WIN_SCORE:
        root.after(1000, celebrate_winner, current_player)
    else:
        # Prepare next question after a short delay
        root.after(2000, generate_question)

# Function to celebrate the winner
def celebrate_winner(winner):
    # Disable choice buttons
    for btn in choice_buttons:
        btn.config(state=tk.DISABLED)
    # Create a new window for celebration
    celebration_window = tk.Toplevel(root)
    celebration_window.title("Congratulations!")
    celebration_window.geometry("400x300")
    # Display celebration message
    celebration_label = tk.Label(celebration_window, text=f"Player {winner} Wins!", font=("Arial", 30), fg="green")
    celebration_label.pack(pady=30)
    # Create confetti effect using Canvas
    canvas = tk.Canvas(celebration_window, width=400, height=200, bg="white")
    canvas.pack()
    # Generate confetti
    for _ in range(100):
        x = random.randint(0, 400)
        y = random.randint(0, 200)
        size = random.randint(5, 15)
        color = random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
        canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
    # Close the main game window
    root.destroy()

# Key press event handler
def on_key_press(event):
    key = event.keysym.upper()
    if key == 'Q':
        buzz_in(1)
    elif key == 'P':
        buzz_in(2)

# Question label
question_label = tk.Label(root, text="", font=("Arial", 24))
question_label.pack(pady=20)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 14))
status_label.pack(pady=10)

# Feedback label
feedback_label = tk.Label(root, text="", font=("Arial", 16))
feedback_label.pack(pady=10)

# Choice buttons
choices_frame = tk.Frame(root)
choices_frame.pack(pady=20)

choice_buttons = []
for i in range(3):
    btn = tk.Button(
        choices_frame,
        text="",
        command=lambda i=i: select_choice(i),
        font=("Arial", 18),
        state=tk.DISABLED,
        width=5,
    )
    btn.pack(side=tk.LEFT, padx=10)
    choice_buttons.append(btn)

# Score label
score_label = tk.Label(root, text="Player 1: 0    Player 2: 0", font=("Arial", 18))
score_label.pack(pady=20)

# Bind key events
root.bind('<KeyPress>', on_key_press)

# Start the game
generate_question()

# Run the main loop
root.mainloop()
