import random
import threading

QUESTION_PAIRS = [
    (
        "What's the fastest thing you can do?",
        "What's the slowest thing you can do?",
    ),
    (
        "What's the most exciting thing you've ever done?",
        "What's the least exciting thing you've ever done?",
    ),
    (
        "What would you do with 1 million dollars in one day?",
        "What would you do with 1 million dollars in the worst possible way?",
    ),
    (
        "What's the best food you can eat right now?",
        "What's the worst food you can eat right now?",
    ),
    (
        "What is the most useful skill to have?",
        "What is the least useful skill to have?",
    ),
]


def choose_imposter(players):
    return random.choice(players)


def get_question_for_player(player, imposter, question_pair):
    if player == imposter:
        return question_pair[1]
    return question_pair[0]


def parse_timer_input(prompt_text):
    while True:
        value = input(prompt_text).strip().lower()
        try:
            if value.endswith("m"):
                minutes = float(value[:-1])
                if minutes > 0:
                    return int(minutes * 60)
            elif value.endswith("s"):
                seconds = float(value[:-1])
                if seconds > 0:
                    return int(seconds)
            else:
                seconds = float(value)
                if seconds > 0:
                    return int(seconds)
        except ValueError:
            pass

        print("Please enter a valid time like 30s, 2m, or 45.")


def get_answer_with_timer(player, question, seconds):
    print(f"\n{player}, answer this: {question}")
    print(f"You have {seconds} seconds to answer.")

    answer_holder = []

    def read_input():
        answer_holder.append(input("Your answer: ").strip())

    thread = threading.Thread(target=read_input, daemon=True)
    thread.start()
    thread.join(seconds)

    if thread.is_alive():
        print("\nTime's up! No answer recorded.")
        return "TIME UP"

    if not answer_holder:
        return "TIME UP"

    return answer_holder[0]


def ask_guess(players, imposter):
    print("\n--- Guess who the imposter is ---")
    votes = {}

    for player in players:
        while True:
            guess = input(f"{player}, who do you think is the imposter? ({', '.join(players)}): ").strip()
            if guess in players:
                break
            print("Invalid name. Please choose one of the players.")

        votes[player] = guess

    print("\n--- Vote Results ---")
    for player in players:
        guess = votes[player]
        if guess == imposter:
            print(f"{player} guessed correctly! {imposter} was the imposter.")
        else:
            print(f"{player} guessed {guess}, but the imposter was {imposter}.")

    correct_voters = [player for player, guess in votes.items() if guess == imposter]
    if correct_voters:
        print(f"\nCorrect guesses: {', '.join(correct_voters)}")
    else:
        print("\nNo one guessed the imposter correctly.")


def main():
    print("=== Imposter Question Game ===")
    print("Everyone answers under one shared timer, then all players can see answers and guess.")

    timer_seconds = parse_timer_input("Set the overall answer timer (example: 30s, 2m, or 45): ")

    player_names = []
    while True:
        name = input("Enter a player's name (or press Enter to start the game): ").strip()
        if not name:
            if len(player_names) >= 2:
                break
            print("Please add at least 2 players.")
            continue
        player_names.append(name)

    imposter = choose_imposter(player_names)
    question_pair = random.choice(QUESTION_PAIRS)

    print(f"\nThe imposter is secretly: {imposter}")
    print("The question pair is ready. Everyone answers under the same timer.")
    print("\n--- Round begins ---")

    answers = {}
    for player in player_names:
        question = get_question_for_player(player, imposter, question_pair)
        answers[player] = get_answer_with_timer(player, question, timer_seconds)

    print("\n--- Final Answers ---")
    for player in player_names:
        print(f"{player}: {answers[player]}")

    print("\nEveryone can now see the answers and guess who the imposter is.")
    ask_guess(player_names, imposter)

    print("\nThe imposter was:", imposter)
    print("Question pair:")
    print(f"Normal: {question_pair[0]}")
    print(f"Opposite: {question_pair[1]}")


if __name__ == "__main__":
    main()
