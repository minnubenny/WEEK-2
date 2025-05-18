import asyncio
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get the Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please check your env.txt file.")

# Gemini LLM configuration
llm_config = {
    "config_list": [
        {
            "model": "gemini-1.5-flash",  # or "gemini-pro"
            "api_key": api_key,
            "api_type": "google"
        }
    ]
}

# Define Agents
planner = AssistantAgent(
    name="Planner",
    system_message="You are a helpful planner who creates travel plans based on user requests. Ask the Researcher for information as needed.",
    llm_config=llm_config,
)

researcher = AssistantAgent(
    name="Researcher",
    system_message="You are a researcher who provides detailed information about travel destinations.",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config=False,
)

# Group chat and manager
groupchat = GroupChat(
    agents=[user_proxy, planner, researcher],
    messages=[],
    max_round=5,
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

# Main function
async def main():
    await asyncio.sleep(1)
    user_proxy.initiate_chat(
        manager,
        message="I want to plan a 3-day trip to Paris. Can you help?",
    )
    await asyncio.sleep(1)

# Run it
if __name__ == "__main__":
    asyncio.run(main())
