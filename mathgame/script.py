from js import document, window
import random
import asyncio
from pyodide.ffi import create_proxy
import math

# Variables to keep track of the game state
current_answer = None
current_player = None
scores = {1: 0, 2: 0}
buzzed_in = False
WIN_SCORE = 12
countdown_in_progress = False

# DOM Elements
question_element = document.getElementById('question')
status_element = document.getElementById('status')
feedback_element = document.getElementById('feedback')
choices_element = document.getElementById('choices')
score_element = document.getElementById('score')
celebration_modal = document.getElementById('celebration-modal')
winner_message = document.getElementById('winner-message')
confetti_canvas = document.getElementById('confetti-canvas')
confetti_ctx = confetti_canvas.getContext('2d')

# Start the game
async def main():
    await generate_question()

async def generate_question():
    global buzzed_in, current_player, current_answer, countdown_in_progress
    buzzed_in = False
    current_player = None
    feedback_element.innerHTML = ''
    choices_element.innerHTML = ''
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operations = ['+', '-', '×', '÷']
    operation = random.choice(operations)
    
    if operation == '+':
        current_answer = num1 + num2
    elif operation == '-':
        current_answer = num1 - num2
    elif operation == '×':
        current_answer = num1 * num2
    elif operation == '÷':
        num1 = num1 * num2  # Ensure division is exact
        current_answer = num1 // num2
    
    question_element.innerHTML = f"{num1} {operation} {num2} = ?"
    
    wrong_answers = set()
    while len(wrong_answers) < 2:
        wrong_answer = current_answer + random.randint(-10, 10)
        if wrong_answer != current_answer:
            wrong_answers.add(wrong_answer)
    
    all_answers = list(wrong_answers) + [current_answer]
    random.shuffle(all_answers)
    
    for answer in all_answers:
        btn = document.createElement('button')
        btn.innerHTML = str(answer)
        btn.className = 'choice-button'
        btn.disabled = True
        btn.onclick = create_proxy(lambda e, ans=answer: select_choice(ans))
        choices_element.appendChild(btn)
    
    countdown_in_progress = True
    await countdown(3)

async def countdown(count):
    global countdown_in_progress
    if count > 0:
        status_element.innerHTML = f"Get ready... {count}"
        await asyncio.sleep(1)
        await countdown(count - 1)
    else:
        countdown_in_progress = False
        status_element.innerHTML = "Press 'Q' (Player 1) or 'P' (Player 2) to buzz in."

def buzz_in(player):
    global buzzed_in, current_player
    if not buzzed_in and not countdown_in_progress:
        buzzed_in = True
        current_player = player
        buttons = choices_element.getElementsByTagName('button')
        for btn in buttons:
            btn.disabled = False
            btn.style.backgroundColor = 'lightblue' if current_player == 1 else 'lightcoral'
        status_element.innerHTML = f"Player {current_player} buzzed in! Choose your answer."

def select_choice(selected_answer):
    global scores
    buttons = choices_element.getElementsByTagName('button')
    for btn in buttons:
        btn.disabled = True
    if int(selected_answer) == current_answer:
        feedback_element.innerHTML = f"Player {current_player} is correct!"
        feedback_element.style.color = 'green'
        scores[current_player] += 1
    else:
        feedback_element.innerHTML = f"Player {current_player} is incorrect!"
        feedback_element.style.color = 'red'
    
    score_element.innerHTML = f"Player 1: {scores[1]} &nbsp;&nbsp; Player 2: {scores[2]}"
    
    if scores[current_player] >= WIN_SCORE:
        asyncio.ensure_future(celebrate_winner(current_player))
    else:
        asyncio.ensure_future(next_question())

async def next_question():
    await asyncio.sleep(2)
    await generate_question()

async def celebrate_winner(winner):
    await asyncio.sleep(1)
    winner_message.innerHTML = f"Player {winner} Wins!"
    celebration_modal.style.display = 'block'
    generate_confetti()

def generate_confetti():
    confetti_particles = []
    for _ in range(100):
        confetti_particles.append({
            'x': random.uniform(0, confetti_canvas.width),
            'y': random.uniform(0, confetti_canvas.height),
            'r': random.randint(2, 6),
            'color': random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange']),
            'speed': random.uniform(2, 7),
            'angle': random.uniform(0, 2 * math.pi),
        })
    
    def draw(*args):
        confetti_ctx.clearRect(0, 0, confetti_canvas.width, confetti_canvas.height)
        for p in confetti_particles:
            confetti_ctx.beginPath()
            confetti_ctx.arc(p['x'], p['y'], p['r'], 0, 2 * math.pi)
            confetti_ctx.fillStyle = p['color']
            confetti_ctx.fill()
            p['x'] += p['speed'] * math.cos(p['angle'])
            p['y'] += p['speed'] * math.sin(p['angle']) + 2  # gravity effect
            if p['y'] > confetti_canvas.height:
                p['y'] = 0
            if p['x'] > confetti_canvas.width:
                p['x'] = 0
            if p['x'] < 0:
                p['x'] = confetti_canvas.width
        window.requestAnimationFrame(create_proxy(draw))
    
    draw()

# Event listener for key presses
def on_keydown(event):
    key = event.key.upper()
    if key == 'Q':
        buzz_in(1)
    elif key == 'P':
        buzz_in(2)

document.addEventListener('keydown', create_proxy(on_keydown))

# Start the main function
asyncio.ensure_future(main())
