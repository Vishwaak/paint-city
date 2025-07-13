from crewai import Crew,Process
from tasks import ingredient_task, hotel_task, compare_tasks
from agents import food_researcher, food_critic 

import weave 


import requests
import json
import os
from dotenv import load_dotenv
import base64




load_dotenv()
OPENROUTER = os.getenv("OPENROUTER_API_KEY")
weave.init("hotel_agent")

from openai import OpenAI
import json


class run_agents:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=f"{OPENROUTER}",
        )

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_food_name(self, image_path):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        # Read and encode the image
        base64_image = self.encode_image_to_base64(image_path)
        data_url = f"data:image/jpeg;base64,{base64_image}"
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "just give me the food name one or two workds only"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url
                        }
                    }
                    
                ]
            }
        ]
        payload = {
            "model": "openai/gpt-4o",
            "messages": messages
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    
    def run_agents(self, food_name):
        completion = self.client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {
            "role": "user",
            "content": f" cook {food_name} tonight. Can you give me one list of ingredients with less than 10 ingredients and no steps.",
            }
        ]
        )

        ingredients = completion.choices[0].message.content

        print(ingredients)

        # Forming the tech focused crew with some enhanced configuration
        crew=Crew(
            tasks=[ingredient_task, hotel_task, compare_tasks],
            verbose=1,
            process=Process.sequential,

        )

        # ## starting the task execution process wiht enhanced feedback

        result = crew.kickoff(inputs={'food':'Grilled chicken','ingredient':f'{ingredients}'},)

        # Convert CrewOutput to dict before serializing
        result_dict = result.dict() if hasattr(result, "dict") else result if isinstance(result, dict) else {}
        
        result = result_dict["tasks_output"][2]["raw"]
     
        # convert the result to a dictionary if it is not already
        if not isinstance(result, dict):
            try:
                result = json.loads(result)
            except Exception:
                result = {"raw": result}

    
        # result_dict = result.dict() if hasattr(result, "dict") else dict(result)
        
        return result
