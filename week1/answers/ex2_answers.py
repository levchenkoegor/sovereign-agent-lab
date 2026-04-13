"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ['check_pub_availability', 'calculate_catering_cost', 'get_edinburgh_weather', 'generate_event_flyer']

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = ""

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Albanach+%7C+160+guests&id=4e065f03dfb0"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for AI Meetup, Edinburgh, professional at The Albanach, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The tool didn not return any error. It captures the issue internally and then return a structured
fallback response with success=True. Technically, the tool executed succesfully, and that's why the 
agents behaviour didnt change.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
After receiving the tool result showing The Bow Bar has capacity 80 and status
full (failing both constraints) the agent immediately called check_pub_availability tool
again for The Albanach without waiting for further instruction (it pivoted autonomously
to the next candidate)
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
Okay, let's see. The user is looking for a venue in Edinburgh that can accommodate 300 people with vegan options. 
They provided four known venues: The Albanach, The Haymarket Vaults, The Guilford Arms, and The Bow Bar. 
I checked each one using the check_pub_availability function.\n\nThe Albanach has a capacity of 180, which is under 300. 
Haymarket Vaults is 160, also too small. Guilford Arms can take 200, still not enough. The Bow Bar has 80 capacity and is already full. None of them meet the 300-person requirement. 
Even though some have vegan options, the capacity is the main issue here. The user might need to look for other venues outside the provided list or consider a different location. 
I should inform them that none of the known venues can handle the event as specified.

None of the provided Edinburgh venues can accommodate 300 people while meeting all requirements. 
The largest available space (The Guilford Arms) only holds 200 guests, and The Bow Bar is currently full. 
Would you like me to:
\n1. Suggest alternative venues outside this list?
\n2. Help adjust event parameters (e.g. split into multiple locations)?
\n3. Provide contact details for the closest matching venue?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = "Redirected to National Rail / Trainline with no tool call attempted"

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this is good behaviour. The agent correctly recognised it was out of scope,
made no hallucinated tool call, gave the user actionable alternatives (specific
websites and apps), and offered to return to tasks it can actually handle.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph graph has just three nodes (start -> agent <-> tools -> end).
Model decides at every step which tool to call next, so all routing logic is
implicit inside the LLM. 
The Rasa flows.yml is the opposite. Every possible path is written out explicitly as named flows with ordered steps, 
and the LLM only decides which flow to trigger. 

Probably, LangGraph is more flexible but more unpredictable.
Rasa CALM is auditable but rigid.
Id guess the right choice depends on the task.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
In Scenario 3 the agent inspected its own tool list, correctly concluded none applied, 
and declined without attempting a hallucinated tool call - thats cool!
Whats surprising is that this requires genuine self-awareness about capability boundaries: the model had to
reason - I have these four tools, none covers transport, therefore I must not
fabricate an answer. A naive agent would either invent a train time or try to
shoehorn the weather tool into the query. This one did neither.
"""