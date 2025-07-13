from crewai import Task
from env_tools import model_tools
from agents import food_researcher, food_critic



ingredient_task = Task(
  description=(
    "get the price of {ingredient} from walmart in sanfrancisco."
    "the total cost of the recipe. "
    "Ingredients should be listed in a markdown table with columns for name, quantity, and price."
    "The total cost should be displayed at the end of the table."
    "limit the number of ingredients to 10. "
    "No ingredient should be repeated." 
    "Don't use the tool more than 3 times for the same ingredient."
  ),
  expected_output='A markdown table listing ingredients with their prices and total cost.',
  tools=[model_tools],
  agent=food_researcher,
)

hotel_task = Task(
  description=(
   "list the  fast food restaurant example chick fil a for {food} in sanfransico."
   "pick the restaurant with least price for {food}."
   "list the restaurant with the price and distance"
   "don't use any other restaurant than fast food restaurant."
   "Don't take more than 5 restaurants."
  ),
  expected_output='A markdown table listing restaurants with their prices and distance.',
  tools=[model_tools],
  agent=food_critic,
)



compare_tasks = Task(
    description=(
        "Compare the cost of cooking {food} at home with ordering it from a restaurant in sanfrancisco."
        "Just the cost for now"
        "Also considering the closing time of the restaurant and walmart"
        ),
    expected_output='reasoning about the cost of cooking at home vs ordering from a restaurant and what would be the best option for today give the yes or no reasion in json format. with two fields reason and best_option',
    agent=food_critic,
)