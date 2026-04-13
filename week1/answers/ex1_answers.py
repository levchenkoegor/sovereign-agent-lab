"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults" # (180 tokens)
PART_A_XML_ANSWER      = "The Albanach" # (251 tokens)
PART_A_SANDWICH_ANSWER = "The Albanach" # (289 tokens)

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True  
PART_A_SANDWICH_CORRECT = True  

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
The PLAIN condition returned The Haymarket Vaults (last venue
satisfying all constraints), while XML and SANDWICH returned The Albanach (first
satisfying venue), suggesting mild primacy bias when structure draws attention to
the top of the list.
Another thing: seems like the PLAIN condition has less tokens.
The prompt length is different between conditions (PLAIN, XML, SANDWICH)
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults" # (213 tokens)
PART_B_XML_ANSWER      = "The Albanach" # (302 tokens)
PART_B_SANDWICH_ANSWER = "The Albanach" # (340 tokens)

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The model still returns all corrects answers. However, The Holyrood Arms is the more
dangerous distractor. It has right capacity (160) and menu (vegan) but not available (full).
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults" # (188 tokens)
PART_C_XML_ANSWER      = "The Haymarket Vaults" # (278 tokens)
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults" # (316 tokens)

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Even the smaller 8B model answered correctly in all three conditions. Interestingly, the
8B model consistently chose The Haymarket Vaults (no primacy bias toward The
Albanach), unlike the 70B model. I guess the dataset is too small so far to cause
any problems for models.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the SNR is low:
the document set is large, distractors closely resemble the correct answer, or the
model is small and less robust. In our case the dataset is too small to significantly affect SNR.
I think, clean datasets with good models, structure (XML, sandwich) provides little measurable benefit.
The real effect would be observed better on large datasets.
"""
