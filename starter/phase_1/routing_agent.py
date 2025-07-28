
# TODO: 1 - Import the KnowledgeAugmentedPromptAgent and RoutingAgent
import os
from dotenv import load_dotenv
from workflow_agents.base_agents import RoutingAgent,KnowledgeAugmentedPromptAgent

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

persona = "You are a college professor"

knowledge = "You know everything about Texas"
# TODO: 2 - Define the Texas Knowledge Augmented Prompt Agent
Texas_Agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,persona=persona,knowledge=knowledge)

knowledge = "You know everything about Europe"
# TODO: 3 - Define the Europe Knowledge Augmented Prompt Agent
Europe_Agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,persona=persona,knowledge=knowledge)

persona = "You are a college math professor"
knowledge = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"

# TODO: 4 - Define the Math Knowledge Augmented Prompt Agent
Math_Agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,persona=persona,knowledge=knowledge)

routing_agent = RoutingAgent(openai_api_key, {})
agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: Texas_Agent.respond(x) # TODO: 5 - Call the Texas Agent to respond to prompts
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: Europe_Agent.respond(x) # TODO: 6 - Define a function to call the Europe Agent
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: Math_Agent.respond(x)# TODO: 7 - Define a function to call the Math Agent
    }
]

routing_agent.agents = agents

# TODO: 8 - Print the RoutingAgent responses to the following prompts:
#           - "Tell me about the history of Rome, Texas"
#           - "Tell me about the history of Rome, Italy"
#           - "One story takes 2 days, and there are 20 stories"

prompt = "Tell me about the history of Rome, Texas"
print(routing_agent.evaluate(prompt))

prompt = "Tell me about the history of Rome, Italy"
print(routing_agent.evaluate(prompt))

prompt = "One story takes 2 days, and there are 20 stories"
print(routing_agent.evaluate(prompt))