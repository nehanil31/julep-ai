import os
import time
import yaml
from dotenv import load_dotenv
from julep import Julep

# Load your environment variables from .env
load_dotenv()

# Initialize Julep client
client = Julep(api_key=os.getenv('JULEP_API_KEY'))

# Step 1: Create your Agent (you can skip if already created)
agent = client.agents.create(
    name="Foodie Tour Agent",
    model="claude-3.5-sonnet",
    about="An AI chef and travel planner that creates city-based foodie experiences."
)

# Step 2: Define Task YAML with dietary preferences and markdown formatting request
task_yaml = """
name: City Foodie Tour
description: Generate a food itinerary for a given city based on weather, cuisine, and dietary preferences
main:
  - prompt:
      - role: system
        content: |
          You are a local food expert and trip planner. Given a city, its weather, and dietary preferences, do the following:
          1. List exactly 3 iconic local dishes.
          2. Decide indoor or outdoor dining based on the weather.
          3. Recommend breakfast, lunch, and dinner — each based on those iconic dishes.
          4. Mention top-rated restaurants for those dishes.
          5. Describe each meal's experience like a narrative.
          6. Do not use Markdown or special formatting like #, *, or ** — keep the output plain and clean.
          7. Consider dietary preferences when recommending dishes and restaurants.
      - role: user
        content: |
          City: ${steps[0].input.city}
          Weather: ${steps[0].input.weather}
          Dietary Preferences: ${steps[0].input.dietary_preferences}
"""


# Load YAML into Python dict
task_definition = yaml.safe_load(task_yaml)

# Step 3: Create the Task on Julep
task = client.tasks.create(agent_id=agent.id, **task_definition)

# Helper: Simple function to fetch weather (stub, replace with real API)
def get_weather_for_city(city):
    # For demo, static or simple logic:
    weather_map = {
        "Kochi": "Partly cloudy, 22°C",
        "Kolkata": "Rainy, 15°C",
        "Mumbai": "Sunny, 28°C",
        # Add more if needed
    }
    return weather_map.get(city, "Clear, 25°C")

# Step 4: Get cities and dietary prefs from user input
cities_input = input("Enter city names separated by commas (e.g., Kochi,Kolkata,Mumbai): ")
dietary_preferences = input("Enter dietary preferences (e.g., vegetarian, vegan, none): ").strip() or "none"

cities = [city.strip() for city in cities_input.split(",") if city.strip()]

# Step 5: Loop over cities, get weather, execute task, print markdown output
for city in cities:
    weather = get_weather_for_city(city)
    city_input = {
        "city": city,
        "weather": weather,
        "dietary_preferences": dietary_preferences
    }
    print(f"\n--- Foodie Tour for {city} ---")
    execution = client.executions.create(task_id=task.id, input=city_input)
    
    # Poll status until done
    while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
        print(f"⏳ Status for {city}: {result.status}")
        time.sleep(2)

    if result.status == "succeeded":
        print("✅ Final Foodie Tour (Markdown formatted):\n")
        print(result.output['choices'][0]['message']['content'])
    else:
        print(f"❌ Error: {result.error}")
