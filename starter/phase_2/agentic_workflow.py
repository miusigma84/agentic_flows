# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
import os
from dotenv import load_dotenv
load_dotenv()

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
api_key = os.getenv("OPENAI_API_KEY")
# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open('Product-Spec-Email-Router.txt', 'r', encoding='utf-8') as file:
    product_spec = file.read()
# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key=api_key,knowledge=knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    + product_spec
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=api_key,persona=persona_product_manager,knowledge=knowledge_product_manager)
# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_evaluation = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = EvaluationAgent(openai_api_key=api_key,persona=persona_evaluation, evaluation_criteria=evaluation_criteria, worker_agent=product_manager_knowledge_agent, max_interactions=10)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=api_key,persona=persona_program_manager,knowledge=knowledge_program_manager)
# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
evaluation_criteria =  """
                      "The answer should be product features that follow the following structure: " \
                      "Feature Name: A clear, concise title that identifies the capability\n" \
                      "Description: A brief explanation of what the feature does and its purpose\n" \
                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
                      "User Benefit: How this feature creates value for the user"
"""
program_manager_evaluation_agent = EvaluationAgent(openai_api_key=api_key,persona=persona_program_manager_eval, evaluation_criteria=evaluation_criteria, worker_agent=program_manager_knowledge_agent, max_interactions=10)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=api_key,persona=persona_dev_engineer,knowledge=knowledge_dev_engineer)
# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
evaluation_criteria =  """
                      "The answer should be tasks following this exact structure: " \
                      "Task ID: A unique identifier for tracking purposes\n" \
                      "Task Title: Brief description of the specific development work\n" \
                      "Related User Story: Reference to the parent user story\n" \
                      "Description: Detailed explanation of the technical work required\n" \
                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
                      "Estimated Effort: Time or complexity estimation\n" \
                      "Dependencies: Any tasks that must be completed first"
"""
development_engineer_evaluation_agent = EvaluationAgent(openai_api_key=api_key,persona=persona_dev_engineer_eval, evaluation_criteria=evaluation_criteria, worker_agent=development_engineer_knowledge_agent, max_interactions=10)

# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routing_agent = RoutingAgent(api_key, {})
agents = [
    {
        "name": "Product Manager",
        "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories",
        "func": lambda x: product_manager_support_function(x)
    },
    {
        "name": "Program Manager",
        "description": "Responsible for defining the features for a product.",
        "func": lambda x: program_manager_support_function(x)
    },
    {
        "name": "Development Engineer",
        "description": "Responsible for defining the development tasks for a product.",
        "func": lambda x: development_engineer_support_function(x)
    }
]

routing_agent.agents = agents
# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.
def product_manager_support_function(query):

    validated_response = product_manager_evaluation_agent.evaluate(query)
    if not validated_response or validated_response["final_response"] is None:
        raise ValueError("No valid response from the Product Manager agent.")

    return validated_response["final_response"]

def program_manager_support_function(query):

    validated_response = program_manager_evaluation_agent.evaluate(query)
    if not validated_response or validated_response["final_response"] is None:
        raise ValueError("No valid response from the Program Manager agent.")

    return validated_response["final_response"]

def development_engineer_support_function(query):

    validated_response = development_engineer_evaluation_agent.evaluate(query)
    if not validated_response or validated_response["final_response"] is None:
        raise ValueError("No valid response from the Development Engineer agent.")

    return validated_response["final_response"]

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "What would the development tasks for this product be?"
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).

import logging
import os

# Set up logging
log_filename = os.path.join(os.path.dirname(__file__), 'workflow_log_v1.txt')
logging.basicConfig(
    filename=log_filename,
    filemode='w',  # Overwrite each run; use 'a' to append
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

completed_steps = []
steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

print(f"Extracted workflow steps: {len(steps)}")
logging.info(f"Extracted workflow steps: {len(steps)}")
for s,step in enumerate(steps):
    print(f"{s}")
    print(f"\nExecuting step: {step}")

    try:

        context = "\n\n".join(completed_steps)

        prompt_task_with_context = f"Task: {step} \n\n Context: {context}"
        print(f"Prompt for routing agent: {prompt_task_with_context}")
        logging.info(f"Prompt for routing agent: {prompt_task_with_context}")

        result = routing_agent.evaluate(prompt_task_with_context)

        completed_steps.append(result)
        print(f"Result of step '{step}': {result}")
        logging.info(f"Result of step '{step}': {result}")

    except ValueError as e:
        print(f"Error processing step '{step}': {e}")
        logging.error(f"Error processing step '{step}': {e}")
        completed_steps.append(f"Error: {e}")

print("\n*** Workflow execution completed ***\n")
# Print the final output of the workflow
if completed_steps:
    print("Final output of the workflow:", completed_steps[-1])
    logging.info(f"Final output of the workflow: {completed_steps[-1]}")
else:
    print("No steps were completed in the workflow.")
    logging.info("No steps were completed in the workflow.")
print("\n*** End of workflow execution ***\n")
logging.info("*** End of workflow execution ***")