# ============================================================
# games.py — Games & Entertainment Module
# ============================================================
# This module provides fun games and entertainment:
#   - Number Guessing Game
#   - Trivia Quiz (General Knowledge)
#   - Rock Paper Scissors
#   - Tic-Tac-Toe
#   - Word Scramble
#   - Math Challenge
#   - Hangman
#   - Coin Flip & Dice Roll
#   - Jokes
#
# HOW IT WORKS:
#   Each game class stores its own state. The GUI creates a game
#   instance and sends player input through the play() method.
#   The game returns text responses to display in the chat.
#
# HOW TO CUSTOMIZE:
#   - Add more trivia questions to TRIVIA_QUESTIONS list
#   - Add more words to HANGMAN_WORDS and SCRAMBLE_WORDS lists
#   - Add more jokes to JOKES list
# ============================================================

import random
import math

# ============================================================
# TRIVIA_QUESTIONS: Add your own questions here!
# Format: {"question": "...", "options": ["A", "B", "C", "D"], "answer": 0}
# The "answer" is the index (0=A, 1=B, 2=C, 3=D)
# ============================================================
TRIVIA_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "London", "Madrid"],
        "answer": 1
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "answer": 2
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": 3
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
        "answer": 1
    },
    {
        "question": "What is the chemical symbol for Gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "answer": 2
    },
    {
        "question": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "answer": 2
    },
    {
        "question": "What programming language is named after a snake?",
        "options": ["Cobra", "Python", "Viper", "Anaconda"],
        "answer": 1
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": 2
    },
    {
        "question": "What is the speed of light approximately?",
        "options": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "100,000 km/s"],
        "answer": 0
    },
    {
        "question": "Which is the smallest country in the world?",
        "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
        "answer": 1
    },
    {
        "question": "What is the main component of the Sun?",
        "options": ["Helium", "Oxygen", "Hydrogen", "Carbon"],
        "answer": 2
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Newton", "Einstein", "Hawking", "Tesla"],
        "answer": 1
    },
    {
        "question": "What is the boiling point of water in Celsius?",
        "options": ["90°C", "100°C", "110°C", "120°C"],
        "answer": 1
    },
    {
        "question": "Which is the longest river in the world?",
        "options": ["Amazon", "Mississippi", "Yangtze", "Nile"],
        "answer": 3
    },
    {
        "question": "What does CPU stand for?",
        "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility"],
        "answer": 1
    },
]

# ============================================================
# WORD LISTS for Hangman and Word Scramble
# ============================================================
HANGMAN_WORDS = [
    "python", "arduino", "computer", "programming", "keyboard",
    "monitor", "software", "hardware", "internet", "database",
    "algorithm", "function", "variable", "electric", "circuit",
    "robotics", "sensor", "bluetooth", "wireless", "assistant",
    "terminal", "compiler", "debugger", "network", "security"
]

SCRAMBLE_WORDS = [
    "python", "coding", "robot", "laser", "pixel",
    "mouse", "screen", "data", "cloud", "logic",
    "bytes", "surge", "drone", "smart", "debug",
    "stack", "queue", "array", "class", "scope"
]

# ============================================================
# JOKES: Add your own jokes here!
# ============================================================
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself! 😄",
    "What's an Arduino's favorite food? Micro-chips! 🍟",
    "Why do Python programmers have low self-esteem? They're constantly comparing themselves to others using 'is'. 🐍",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?' 🍺",
    "Why did the computer go to the doctor? It had a virus! 🤒",
    "What do computers eat for a snack? Microchips! 🔌",
    "Why was the computer cold? It left its Windows open! ❄️",
    "What's a robot's favorite music genre? Heavy metal! 🤖",
    "Why did the programmer quit? Because they didn't get arrays (a raise)! 💰",
    "How does a computer get drunk? It takes screenshots! 📸",
    "What do you call 8 hobbits? A hobbyte! 🧙",
    "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25! 🎃",
    "I told my wife she was drawing her eyebrows too high. She looked surprised. 😲",
]


# ============================================================
# GAME CLASSES
# ============================================================

class NumberGuessingGame:
    """
    Number Guessing Game: Guess a number between 1 and 100.
    
    The computer picks a random number and you try to guess it.
    It tells you if your guess is too high or too low.
    """
    
    def __init__(self):
        """Start a new game with a random number."""
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        self.is_active = True
    
    def start(self) -> str:
        """Get the welcome message for this game."""
        return ("🎯 **Number Guessing Game**\n"
                f"I'm thinking of a number between 1 and 100.\n"
                f"You have {self.max_attempts} attempts. Type your guess!")
    
    def play(self, user_input: str) -> str:
        """
        Process a guess from the player.
        
        Args:
            user_input (str): Player's guess (should be a number)
        
        Returns:
            str: Game response (too high, too low, correct, etc.)
        """
        if not self.is_active:
            return "Game is over! Type 'play number guess' to play again."
        
        try:
            guess = int(user_input.strip())
        except ValueError:
            return "Please enter a valid number between 1 and 100."
        
        self.attempts += 1
        
        if guess == self.target:
            self.is_active = False
            return f"🎉 Correct! The number was {self.target}! You got it in {self.attempts} attempts!"
        elif self.attempts >= self.max_attempts:
            self.is_active = False
            return f"😔 Game over! The number was {self.target}. Better luck next time!"
        elif guess < self.target:
            remaining = self.max_attempts - self.attempts
            return f"⬆️ Too low! Try higher. ({remaining} attempts left)"
        else:
            remaining = self.max_attempts - self.attempts
            return f"⬇️ Too high! Try lower. ({remaining} attempts left)"


class TriviaQuiz:
    """
    Trivia Quiz: Answer multiple-choice questions.
    
    Questions are randomly selected from TRIVIA_QUESTIONS.
    """
    
    def __init__(self, num_questions: int = 5):
        """
        Start a new quiz.
        
        Args:
            num_questions (int): How many questions to ask (default: 5)
        """
        self.questions = random.sample(TRIVIA_QUESTIONS, min(num_questions, len(TRIVIA_QUESTIONS)))
        self.current_index = 0
        self.score = 0
        self.is_active = True
    
    def start(self) -> str:
        """Get the first question."""
        return f"🧠 **Trivia Quiz** — {len(self.questions)} Questions\n\n" + self._current_question()
    
    def _current_question(self) -> str:
        """Format the current question with options."""
        q = self.questions[self.current_index]
        text = f"**Q{self.current_index + 1}:** {q['question']}\n"
        for i, opt in enumerate(q['options']):
            letter = chr(65 + i)  # A, B, C, D
            text += f"  {letter}) {opt}\n"
        text += "\nType A, B, C, or D:"
        return text
    
    def play(self, user_input: str) -> str:
        """
        Process an answer from the player.
        
        Args:
            user_input (str): Player's answer (A, B, C, or D)
        
        Returns:
            str: Whether correct/wrong + next question or final score
        """
        if not self.is_active:
            return "Quiz is over! Type 'play quiz' to play again."
        
        # --- Parse answer ---
        answer = user_input.strip().upper()
        if answer not in ['A', 'B', 'C', 'D']:
            return "Please answer with A, B, C, or D."
        
        answer_index = ord(answer) - 65  # A=0, B=1, C=2, D=3
        q = self.questions[self.current_index]
        correct_index = q['answer']
        correct_letter = chr(65 + correct_index)
        
        if answer_index == correct_index:
            self.score += 1
            result = f"✅ Correct! "
        else:
            result = f"❌ Wrong! The answer was {correct_letter}) {q['options'][correct_index]}. "
        
        self.current_index += 1
        
        if self.current_index >= len(self.questions):
            self.is_active = False
            result += f"\n\n🏆 **Quiz Complete!** Score: {self.score}/{len(self.questions)}"
            if self.score == len(self.questions):
                result += " — PERFECT! 🌟"
            elif self.score >= len(self.questions) * 0.7:
                result += " — Great job! 👏"
            else:
                result += " — Keep practicing! 💪"
            return result
        else:
            result += f"(Score: {self.score}/{self.current_index})\n\n"
            result += self._current_question()
            return result


class RockPaperScissors:
    """
    Rock Paper Scissors: Play against the computer.
    Best of 5 rounds.
    """
    
    def __init__(self):
        """Start a new game."""
        self.choices = ["rock", "paper", "scissors"]
        self.emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.max_rounds = 5
        self.is_active = True
    
    def start(self) -> str:
        """Get the welcome message."""
        return ("✊📄✂️ **Rock Paper Scissors** — Best of 5!\n"
                "Type: rock, paper, or scissors")
    
    def play(self, user_input: str) -> str:
        """
        Process the player's choice.
        
        Args:
            user_input (str): "rock", "paper", or "scissors"
        
        Returns:
            str: Round result + scores
        """
        if not self.is_active:
            return "Game is over! Type 'play rps' to play again."
        
        choice = user_input.strip().lower()
        if choice not in self.choices:
            return "Please type: rock, paper, or scissors"
        
        computer_choice = random.choice(self.choices)
        self.rounds_played += 1
        
        result = f"You: {self.emojis[choice]} vs Computer: {self.emojis[computer_choice]}\n"
        
        if choice == computer_choice:
            result += "🤝 It's a tie!"
        elif (choice == "rock" and computer_choice == "scissors" or
              choice == "paper" and computer_choice == "rock" or
              choice == "scissors" and computer_choice == "paper"):
            self.player_score += 1
            result += "🎉 You win this round!"
        else:
            self.computer_score += 1
            result += "😔 Computer wins this round!"
        
        result += f"\nScore: You {self.player_score} — {self.computer_score} Computer"
        
        if self.rounds_played >= self.max_rounds:
            self.is_active = False
            if self.player_score > self.computer_score:
                result += "\n\n🏆 **You win the game!** 🎉"
            elif self.computer_score > self.player_score:
                result += "\n\n🤖 **Computer wins the game!**"
            else:
                result += "\n\n🤝 **It's a draw!**"
        else:
            result += f"\nRound {self.rounds_played + 1}/{self.max_rounds} — Type your choice:"
        
        return result


class TicTacToe:
    """
    Tic-Tac-Toe: Play against the computer (simple AI).
    
    Board positions are numbered 1-9:
      1 | 2 | 3
      ---------
      4 | 5 | 6
      ---------
      7 | 8 | 9
    """
    
    def __init__(self):
        """Start a new game."""
        self.board = [" "] * 9  # 9 cells, indexed 0-8
        self.player = "X"  # Player is X
        self.computer = "O"  # Computer is O
        self.is_active = True
    
    def start(self) -> str:
        """Get the welcome message with board."""
        return ("❌⭕ **Tic-Tac-Toe** — You are X!\n\n"
                + self._draw_board() +
                "\nType a number (1-9) to place your X:")
    
    def _draw_board(self) -> str:
        """Draw the current board state."""
        b = self.board
        lines = []
        for i in range(3):
            row = []
            for j in range(3):
                cell = b[i * 3 + j]
                if cell == " ":
                    row.append(str(i * 3 + j + 1))  # Show position number
                else:
                    row.append(cell)
            lines.append(" | ".join(row))
        return "\n-----------\n".join(lines)
    
    def _check_winner(self, mark: str) -> bool:
        """Check if a player has won."""
        b = self.board
        # All winning combinations (rows, columns, diagonals)
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)               # diagonals
        ]
        return any(b[a] == b[b_] == b[c] == mark for a, b_, c in wins)
    
    def _is_board_full(self) -> bool:
        """Check if the board is full (draw)."""
        return " " not in self.board
    
    def _computer_move(self) -> int:
        """
        Simple AI for computer's move.
        Priority: 1) Win if possible, 2) Block player, 3) Take center, 4) Random
        """
        # Try to win
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.computer
                if self._check_winner(self.computer):
                    self.board[i] = " "
                    return i
                self.board[i] = " "
        
        # Block player from winning
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.player
                if self._check_winner(self.player):
                    self.board[i] = " "
                    return i
                self.board[i] = " "
        
        # Take center if available
        if self.board[4] == " ":
            return 4
        
        # Take a corner
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if self.board[c] == " "]
        if available_corners:
            return random.choice(available_corners)
        
        # Take any available spot
        available = [i for i in range(9) if self.board[i] == " "]
        return random.choice(available) if available else -1
    
    def play(self, user_input: str) -> str:
        """
        Process the player's move.
        
        Args:
            user_input (str): Position number (1-9)
        
        Returns:
            str: Board state + result
        """
        if not self.is_active:
            return "Game is over! Type 'play tictactoe' to play again."
        
        try:
            pos = int(user_input.strip()) - 1  # Convert to 0-indexed
        except ValueError:
            return "Please enter a number between 1 and 9."
        
        if pos < 0 or pos > 8:
            return "Please enter a number between 1 and 9."
        
        if self.board[pos] != " ":
            return "That spot is taken! Choose another."
        
        # Player's move
        self.board[pos] = self.player
        
        if self._check_winner(self.player):
            self.is_active = False
            return self._draw_board() + "\n\n🎉 **You win!** Congratulations! 🏆"
        
        if self._is_board_full():
            self.is_active = False
            return self._draw_board() + "\n\n🤝 **It's a draw!**"
        
        # Computer's move
        comp_pos = self._computer_move()
        if comp_pos >= 0:
            self.board[comp_pos] = self.computer
        
        if self._check_winner(self.computer):
            self.is_active = False
            return self._draw_board() + "\n\n🤖 **Computer wins!** Better luck next time!"
        
        if self._is_board_full():
            self.is_active = False
            return self._draw_board() + "\n\n🤝 **It's a draw!**"
        
        return self._draw_board() + "\n\nYour turn! Type a number (1-9):"


class WordScramble:
    """
    Word Scramble: Unscramble letters to form a word.
    """
    
    def __init__(self):
        """Start a new game with a random word."""
        self.word = random.choice(SCRAMBLE_WORDS)
        self.scrambled = self._scramble(self.word)
        self.attempts = 3
        self.is_active = True
    
    def _scramble(self, word: str) -> str:
        """Scramble the letters of a word."""
        letters = list(word)
        for _ in range(10):  # Shuffle multiple times to ensure it's scrambled
            random.shuffle(letters)
        scrambled = ''.join(letters)
        # Make sure it's actually different from the original
        if scrambled == word:
            letters.reverse()
            scrambled = ''.join(letters)
        return scrambled
    
    def start(self) -> str:
        """Get the scrambled word prompt."""
        return (f"🔤 **Word Scramble**\n"
                f"Unscramble this word: **{self.scrambled.upper()}**\n"
                f"You have {self.attempts} attempts. Type your answer!")
    
    def play(self, user_input: str) -> str:
        """
        Process the player's guess.
        
        Args:
            user_input (str): Player's word guess
        
        Returns:
            str: Correct/wrong + hints
        """
        if not self.is_active:
            return "Game is over! Type 'play scramble' to play again."
        
        guess = user_input.strip().lower()
        
        if guess == self.word:
            self.is_active = False
            return f"🎉 Correct! The word was **{self.word.upper()}**! Well done!"
        else:
            self.attempts -= 1
            if self.attempts <= 0:
                self.is_active = False
                return f"😔 Game over! The word was **{self.word.upper()}**."
            else:
                hint = f"Hint: The word starts with '{self.word[0].upper()}' and has {len(self.word)} letters."
                return f"❌ Wrong! {hint}\n({self.attempts} attempts left)"


class MathChallenge:
    """
    Math Challenge: Solve random math problems.
    Get 5 problems right to win!
    """
    
    def __init__(self):
        """Start a new math challenge."""
        self.score = 0
        self.total = 5
        self.current = 0
        self.current_answer = 0
        self.is_active = True
        self._generate_problem()
    
    def _generate_problem(self) -> None:
        """Generate a random math problem."""
        self.current += 1
        op = random.choice(['+', '-', '*'])
        
        if op == '+':
            a, b = random.randint(10, 100), random.randint(10, 100)
            self.current_answer = a + b
        elif op == '-':
            a = random.randint(20, 100)
            b = random.randint(10, a)
            self.current_answer = a - b
        else:  # multiplication
            a, b = random.randint(2, 15), random.randint(2, 15)
            self.current_answer = a * b
        
        self.current_problem = f"{a} {op} {b}"
    
    def start(self) -> str:
        """Get the first problem."""
        return (f"🔢 **Math Challenge** — Solve {self.total} problems!\n\n"
                f"Problem {self.current}/{self.total}: What is **{self.current_problem}** ?")
    
    def play(self, user_input: str) -> str:
        """
        Process the player's answer.
        
        Args:
            user_input (str): Player's numeric answer
        
        Returns:
            str: Correct/wrong + next problem or final score
        """
        if not self.is_active:
            return "Challenge is over! Type 'play math' to play again."
        
        try:
            answer = int(user_input.strip())
        except ValueError:
            return "Please enter a number."
        
        if answer == self.current_answer:
            self.score += 1
            result = "✅ Correct! "
        else:
            result = f"❌ Wrong! The answer was {self.current_answer}. "
        
        if self.current >= self.total:
            self.is_active = False
            result += f"\n\n🏆 **Challenge Complete!** Score: {self.score}/{self.total}"
            if self.score == self.total:
                result += " — PERFECT! 🌟"
            return result
        else:
            self._generate_problem()
            result += f"(Score: {self.score})\n\n"
            result += f"Problem {self.current}/{self.total}: What is **{self.current_problem}** ?"
            return result


class Hangman:
    """
    Hangman: Guess the word one letter at a time.
    You have 6 wrong guesses before you lose.
    """
    
    def __init__(self):
        """Start a new hangman game."""
        self.word = random.choice(HANGMAN_WORDS)
        self.guessed = set()
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.is_active = True
    
    def _display_word(self) -> str:
        """Show the word with unguessed letters as underscores."""
        return " ".join(c.upper() if c in self.guessed else "_" for c in self.word)
    
    def _hangman_art(self) -> str:
        """ASCII art for the hangman based on wrong guesses."""
        stages = [
            "  +---+\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  O   |\n      |\n      |\n      |\n=========",
            "  +---+\n  O   |\n  |   |\n      |\n      |\n=========",
            "  +---+\n  O   |\n /|   |\n      |\n      |\n=========",
            "  +---+\n  O   |\n /|\\  |\n      |\n      |\n=========",
            "  +---+\n  O   |\n /|\\  |\n /    |\n      |\n=========",
            "  +---+\n  O   |\n /|\\  |\n / \\  |\n      |\n========="
        ]
        return stages[min(self.wrong_guesses, 6)]
    
    def start(self) -> str:
        """Get the initial hangman display."""
        return (f"🎯 **Hangman** — Guess the word!\n\n"
                f"{self._hangman_art()}\n\n"
                f"Word: {self._display_word()}\n"
                f"({len(self.word)} letters)\n\n"
                f"Type a letter to guess:")
    
    def play(self, user_input: str) -> str:
        """
        Process a letter guess.
        
        Args:
            user_input (str): A single letter
        
        Returns:
            str: Game state after the guess
        """
        if not self.is_active:
            return "Game is over! Type 'play hangman' to play again."
        
        letter = user_input.strip().lower()
        
        if len(letter) != 1 or not letter.isalpha():
            return "Please enter a single letter."
        
        if letter in self.guessed:
            return f"You already guessed '{letter.upper()}'. Try another letter."
        
        self.guessed.add(letter)
        
        if letter in self.word:
            result = f"✅ '{letter.upper()}' is in the word!\n\n"
        else:
            self.wrong_guesses += 1
            result = f"❌ '{letter.upper()}' is not in the word!\n\n"
        
        result += f"{self._hangman_art()}\n\n"
        result += f"Word: {self._display_word()}\n"
        result += f"Guessed: {', '.join(sorted(g.upper() for g in self.guessed))}\n"
        result += f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong}"
        
        # Check win
        if all(c in self.guessed for c in self.word):
            self.is_active = False
            result += f"\n\n🎉 **You win!** The word was **{self.word.upper()}**! 🏆"
            return result
        
        # Check loss
        if self.wrong_guesses >= self.max_wrong:
            self.is_active = False
            result += f"\n\n😔 **Game over!** The word was **{self.word.upper()}**."
            return result
        
        return result


# ============================================================
# QUICK FUN FUNCTIONS (no game state needed)
# ============================================================

def coin_flip() -> str:
    """Flip a coin — heads or tails."""
    result = random.choice(["Heads", "Tails"])
    emoji = "🪙"
    return f"{emoji} Coin flip result: **{result}**!"


def dice_roll(sides: int = 6) -> str:
    """
    Roll a dice.
    
    Args:
        sides (int): Number of sides (default: 6)
    
    Returns:
        str: Dice result
    """
    result = random.randint(1, sides)
    return f"🎲 Dice roll ({sides}-sided): **{result}**!"


def tell_joke() -> str:
    """Tell a random joke."""
    return f"😂 {random.choice(JOKES)}"


def random_number(min_val: int = 1, max_val: int = 100) -> str:
    """Generate a random number in range."""
    num = random.randint(min_val, max_val)
    return f"🔢 Random number ({min_val}-{max_val}): **{num}**"


def magic_8ball() -> str:
    """Ask the Magic 8-Ball a question."""
    responses = [
        "It is certain. ✅",
        "Without a doubt. ✅",
        "Yes, definitely! ✅",
        "Most likely. ✅",
        "Outlook good. ✅",
        "Signs point to yes. ✅",
        "Reply hazy, try again. 🤔",
        "Ask again later. 🤔",
        "Better not tell you now. 🤔",
        "Cannot predict now. 🤔",
        "Don't count on it. ❌",
        "My reply is no. ❌",
        "My sources say no. ❌",
        "Outlook not so good. ❌",
        "Very doubtful. ❌",
    ]
    return f"🎱 Magic 8-Ball says: {random.choice(responses)}"


def get_games_list() -> str:
    """
    Get a formatted list of all available games.
    
    Returns:
        str: List of games with commands
    """
    return """🎮 **Available Games & Entertainment:**

  🎯 play number guess  — Guess a number 1-100
  🧠 play quiz          — Trivia quiz (multiple choice)
  ✊ play rps           — Rock Paper Scissors
  ❌ play tictactoe     — Tic-Tac-Toe vs Computer
  🔤 play scramble      — Word Scramble
  🔢 play math          — Math Challenge
  🎯 play hangman       — Hangman (word guessing)
  🪙 flip coin          — Flip a coin
  🎲 roll dice          — Roll a dice
  😂 tell joke          — Hear a joke
  🔢 random number      — Get a random number
  🎱 magic 8ball        — Ask the Magic 8-Ball"""
