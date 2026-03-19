# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it appeared to work on the surface but quickly fell apart during play. The most obvious issue was that the hints were backwards, guessing a number too high would tell me to go higher, and too low would tell me to go lower, making it impossible to narrow in on the answer. After winning or losing a round, clicking New Game had no effect at all; the game stayed frozen, showing the previous result, and would not accept new guesses. I also noticed the attempt counter was already at 1 before I even submitted a guess, and switching difficulty never updated the displayed guess range from "1 and 100."

---

## 2. How did you use AI as a teammate?

I used Claude (Claude Code) as my primary AI tool throughout this project. One example of a correct suggestion was when I reported the hint direction bug. Claude read the `check_guess` function, identified that the "Go HIGHER" and "Go LOWER" messages were attached to the wrong branches, and swapped them. I verified this by playing the game and confirming the hints now pointed in the right direction, and also by running the `test_hint_go_lower_when_too_high` and `test_hint_go_higher_when_too_low` tests, which both passed. An example of a suggestion I pushed back on was when Claude initially added code to regenerate the secret number on every submission to address the README's claim about changing secrets. I rejected that change because it would make the game unwinnable in practice, and we agreed the README's description was simply inaccurate.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by both playing through the relevant scenario manually and by running `pytest app.py` to confirm the corresponding test passed. For example, after fixing the scoring bug (even-numbered wrong guesses were adding 5 instead of subtracting), I wrote `test_too_high_even_attempt_subtracts` which called `update_score(100, "Too High", 2)` and asserted the result was 95. Before the fix, the test would have returned 105; after removing the even/odd condition, it correctly returned 95. Claude helped design the edge case tests, suggesting boundary checks like guessing exactly 1 above or below the secret, testing the score floor on late-game wins, and testing that score can go negative, cases I might not have thought to cover on my own.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number kept changing because Streamlit reruns the entire script from top to bottom on every user interaction. Without `session_state`, variables like the secret get reassigned a new random value on each rerun. Streamlit "reruns" means the whole Python file re-executes every time you click a button or change an input, imagine refreshing a webpage, except your Python code runs again each time. `session_state` is like a notebook that persists between those reruns, so values you store there survive instead of being reset. The fix that gave the game a stable secret was wrapping the initial assignment in `if "secret" not in st.session_state`, so it only generates a new number the very first time the app loads.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is writing tests alongside fixes rather than after each time we identified a bug, we immediately wrote a test that would have caught it, which made it easy to confirm the fix and prevent regressions. Next time I work with AI on a coding task, I would be more deliberate about verifying each suggestion against the actual running app before accepting it, rather than trusting that a plausible-sounding fix is correct. This project changed the way I think about AI-generated code because it showed me that AI can write code that looks completely reasonable and even passes a basic review, yet still contain several subtle logic bugs that only reveal themselves through actual use.
