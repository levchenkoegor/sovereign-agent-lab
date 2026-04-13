"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                             
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                               
And how many of those guests will need vegan meals?
Your input ->  ~50 vegan                                                                                                                                
2026-04-13 12:53:37 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user\'s last message is "~50 vegan". The current flow is confirm_booking, and the current step is asking for vegan_count. The guest_count is already set to 160. So the user is responding to the question about how many vegan meals are needed.

First, I need to extract the slot value. The user says "~50", which is approximately 50. The slot vegan_count is of type float, so I should convert that to a number. Even though it\'s approximate, the system expects a numerical value. So I\'ll set vegan_count to 50.0. 

Since the user is providing the vegan count, the next step would be to check if there are any other slots needed in the confirm_booking flow. The remaining slot is deposit_amount_gbp, which is still undefined. But the user hasn\'t mentioned the deposit yet. The AI hasn\'t asked about it yet either. Wait, the current step is only asking for vegan_count. Once that\'s set, maybe the next step in the flow is to ask about the deposit. But according to the current state, the active flow is confirm_booking, and the current step is requesting vegan_count. After that, the next step would be to ask about the deposit. But the user hasn\'t provided that info yet. So after setting vegan_count, the AI should proceed to ask about the deposit. But the task here is to generate the action list for the user\'s last message, which is "~50 vegan". So the action is to set the vegan_count to 50.0 and then continue with the flow. However, the AI\'s next action would be to prompt for the deposit amount. But according to the instructions, the action list should only include the necessary actions based on the user\'s input. Since the user provided the vegan count, the AI should set that slot and then move to the next step in the flow, which is asking for deposit_amount_gbp. But the example in the instructions shows that when a slot is set, you just set it and start the flow if needed. Wait, the current flow is already active (confirm_booking), so the AI just needs to set the slot. The next step would be handled by the system\'s next prompt. So the correct action here is to set the vegan_count to 50.0. The user hasn\'t mentioned the deposit, so no action on that yet. Therefore, the action list should be:

set slot vegan' message='No commands were parsed from the LLM actions.'
2026-04-13 12:53:37 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  50                                                                                                                                       
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                             
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                             

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                               

And how many of those guests will need vegan meals?
Your input ->  50  

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £550  

I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £550 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?

"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "The deposith is too high: it exceeds the limit of 300 pounds"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                                             

How many guests are you confirming for tonight's event?
Your input ->  160      

And how many of those guests will need vegan meals?
Your input ->  50                                  

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  Whats about the parking lot?  

I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?

"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The agent said it could help only with venue booking. And for anything else Id have to contact the directly.
Finished with the question if Id like to go back to the main conversation about booking the venue.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
I think both of them did well. The langgraph gave some recommendations on national rail website or trainline app.
And the Rasa CALMs directly said it couldnt handle the request and suggested to contact the venue directly. 
Both of them didnt hallucinate. And I think did a good job providing suggestions to find solutions.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ['actions.py']

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I changed now datetime variable to match the condition (later than 16:45 pm)
and then run the whole conversation again.
Agent reply in the end:

I need to check one thing with the organiser before I can confirm. 
The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. 
Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now handles intent classification, entity extraction, and natural
language understanding that previously required hundreds of NLU examples,
regex validators, and hand-written rules. We gain dramatically less
maintenance overhead and the ability to handle paraphrases never
anticipated ("160-ish" just works)

Old Rasas Python validators were unit-testable,
version-controlled, and behaved identically on every run. Business rules
(minimum deposit, guest count thresholds) stay in Python precisely because
we cannot afford an LLM to occasionally interpret "£50 deposit" as
acceptable when your constraint says £200 minimum.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The setup cost bought us behavioural guarantees.
The CALM agent cannot improvise a response outside its defined flows
It cannot call a tool that wasnt declared in flows.yml

For the confirmation use case, this is a feature, not a limitation. A
booking confirmation call has a known, finite set of outcomes. You want the
agent to collect exactly three slots and run exactly one validation action (no detours)

LangGraph could handle the same call,
but I would have no guarantee it wouldnt invent a fourth question 
or skip one.
"""
