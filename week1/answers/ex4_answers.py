"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = """
<think>\nOkay, the user is looking for a venue in Edinburgh that can hold 300 people and has vegan options. 
I first tried using the search_venues function with min_capacity 300 and requires_vegan set to true. 
The first error was about the input not being a valid dictionary, so I adjusted the extra parameter from null to an empty object. 
But the response came back with zero matches.\n\nHmm, maybe there are no venues that meet both the capacity and vegan requirements.
 But I should check if the parameters were correct. The min_capacity is 300, which is a fairly large number. 
 Perhaps the venues in Edinburgh don't have any that can accommodate that many people with a vegan menu. 
 Alternatively, maybe the requires_vegan filter is too strict. Let me think if there's another approach.\n\n
 Wait, the user might be okay with a venue that has vegan options available, even if it's not the primary menu. 
 But according to the function description, requires_vegan=True only returns venues with a vegan menu. 
 Maybe there's a mistake in the function's parameters. Or perhaps the data just doesn't have any venues meeting those criteria.\n\n
 I should inform the user that there are no available venues matching their request. 
 But before concluding, maybe I should check if there's a lower capacity that could work. 
 However, the user specifically asked for 300 people. 
 If the system's data doesn't have any venues that can handle that size with vegan options, then the answer is that there are no matches. 
 I'll need to present this to the user clearly.\n</think>\n\nIt seems there are no Edinburgh venues currently available that can accommodate 300 guests with vegan menu options.
   Would you like me to:\n\n
   1. Suggest venues with lower capacity (e.g., 200-250 guests)?\n
   2. Show venues without vegan requirements but with other dietary options?\n
   3. Check availability for a different date?\n\nLet me know how you'd like to proceed!
"""

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Since in my first output the agent gave me Haymarket Vaults, I changed to full for that venue in mcp_venue_server file to experiment.

During query 1, the agent found the Albanach as the main venue, which is correct since the Haymarket is not available anymore.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 4   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 40   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP decouples the tool implementation from the agent entirely. The agent
doesnt import, version, or even know about the tools source code. It
discovers whatever the server exposes at runtime. 
Which meams: we can update venue data or add a new tool in mcp_venue_server.py without touching
the agent. Moreover, both the LangGraph agent and the Rasa action server can
connect to the same MCP server (logic lives in one place). I think it even allows us that
the server can run on a different machine or be maintained by a different
team.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.


WEEK_5_ARCHITECTURE = """
- The Planner: Qwen3-32B with thinking enabled.
  It takes a raw booking task and decomposes it into an ordered list of subgoals. 
  It lives upstream of the ReAct loop in the autonomous-loop half.
  The Executor always receives an unambiguous subtask rather than a vague brief.

- The Executor: research_agent.py from Exercise 2/4, grown to include real web
  search and file operations. It lives in the autonomous-loop half and runs the
  Think → Tool Call → Observe cycle against MCP-served tools. It never sees the
  raw user request — only the Planners output.

- The MCP Venue Server: mcp_venue_server.py is the shared data
  layer between both halves. Both the Executors LangGraph tools and the Rasa
  action server connect to it, so venue state is never duplicated — a status
  change in one place is immediately visible to the other.

- The Handoff Bridge: the component that transfers a confirmed venue decision
  from the autonomous loop to the Rasa CALM agent. It packages the Executors
  result (venue name, guest count, catering cost) as structured slots and injects
  them into the confirm_booking flow, so Rasa starts the call already knowing
  what was decided rather than re-collecting slots from scratch.

- The Memory Store: a shared key-value layer sitting between the Planner, Executor, and Rasa halves. 
It holds session state — which venues were checked, what the weather was, what the
  Planner originally decided, so that if the Rasa call surfaces a constraint
  the Executor missed, the Planner can be re-invoked without starting from zero.

- The Rasa MCP Gateway: action in actions.py that calls mcp_venue_server.py
  directly during a confirm_booking flow step, rather than trusting slot values
  passed from the Executor. This is the safety check: business rules (deposit
  minimum, capacity validation) run in Python even when the upstream autonomous
  loop already made a recommendation.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph agent (research_agent.py) is right for the research half and the
Rasa CALM agent is right for the phone call

In exercise 2 (Task A), I saw how the agent decide its own tool order.
That autonomy is exactly what you need when the research task is
open-ended and the number of tool calls isnt known in advance.

The Rasa agent is the opposite: in flows.yml every step is explicit, and the
LLM only picks which flow to start. That rigidity is correct for a live phone
call with a pub manager, where you cannot afford the agent to improvise a
fourth question or skip the deposit slot because it "seemed unnecessary."

Task C Scenario 3 I saw the LangGraph agent correctly refuse an out-of-scope
request, but that refusal was still a model decision, not a guarantee.
"""