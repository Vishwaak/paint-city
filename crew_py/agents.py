from crewai import Agent, LLM
from env_tools import model_tools
from dotenv import load_dotenv
load_dotenv()
import os


# my_llm = LLM(
#               model='gemini/gemini-2.5-pro',
#               api_key=os.getenv("GOOGLE_API_KEY"),
#               temperature=0.0,
#             )

my_llm = LLM(
    model="openrouter/openai/gpt-4o",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.0,
)

food_researcher=Agent(
    role="Senior Chef",
    goal='Figure out if its an good idea to cook {food} at home or to order it from a restaurant',
    verbose=True,
    memory=True,
    backstory=(
        "Compare the cost of cooking {} at home with ordering it from a restaurant."
        "decide it based on time to cook and time to reach from a restaurant."
        "you are optimized searcher for the ingredients and cost of cooking {} at home."
        "you like shopping for ingredients and you search very quickly."


    ),
    tools=[model_tools],
    llm=my_llm,
    allow_delegation=False

)

food_critic = Agent(
  role='Food purchaser',
  goal='You are a food critic who is going to order {food} from a with least price from a fast food restaurant',
  verbose=True,
  memory=True,
  backstory=(
    "you like to order food from restaurants"
    "you order the food from restarants that are known for their quality and service."
  ),
  tools=[model_tools],
  llm=my_llm,
  allow_delegation=False
)