import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret
        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")


# --- tests ---

# Bug 2: guess above secret should tell player to go lower
def test_hint_go_lower_when_too_high():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

# Bug 2: guess below secret should tell player to go higher
def test_hint_go_higher_when_too_low():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

# Bug 2: outcome label is "Too High" when guess exceeds secret
def test_outcome_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

# Bug 2: outcome label is "Too Low" when guess is under secret
def test_outcome_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug 2: exact match returns Win outcome
def test_outcome_win():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

# Bug 3: Easy difficulty returns range 1–20
def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

# Bug 3: Normal difficulty returns range 1–100
def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

# Bug 3: Hard difficulty returns range 1–50
def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 50

# Scoring: even-numbered attempt with wrong guess subtracts points
def test_too_high_even_attempt_subtracts():
    score = update_score(100, "Too High", 2)
    assert score == 95

# Scoring: odd-numbered attempt with wrong guess also subtracts points
def test_too_high_odd_attempt_subtracts():
    score = update_score(100, "Too High", 3)
    assert score == 95

# Scoring: Too Low always subtracts points
def test_too_low_subtracts():
    score = update_score(100, "Too Low", 1)
    assert score == 95

# Scoring: winning adds points to score
def test_win_adds_points():
    score = update_score(0, "Win", 1)
    assert score > 0

# check_guess edge cases

# Guess exactly 1 above secret is still Too High
def test_guess_one_above_secret():
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High" and "LOWER" in message

# Guess exactly 1 below secret is still Too Low
def test_guess_one_below_secret():
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low" and "HIGHER" in message

# Secret at boundary value 1 can still be guessed correctly
def test_guess_wins_at_boundary_low():
    outcome, _ = check_guess(1, 1)
    assert outcome == "Win"

# Secret at boundary value 100 can still be guessed correctly
def test_guess_wins_at_boundary_high():
    outcome, _ = check_guess(100, 100)
    assert outcome == "Win"

# update_score edge cases

# Win on attempt 1 gives full points (100 - 10 * 2 = 80)
def test_win_attempt_1_score():
    score = update_score(0, "Win", 1)
    assert score == 80

# Win on a late attempt floors at 10 points minimum
def test_win_late_attempt_floor():
    score = update_score(0, "Win", 20)
    assert score == 10

# Score can go negative after a wrong guess on a low score
def test_score_goes_negative():
    score = update_score(3, "Too Low", 1)
    assert score == -2