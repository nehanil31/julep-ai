import os
import time
import yaml
from dotenv import load_dotenv
from julep import Julep

# Load environment variables
load_dotenv()

# Initialize Julep client
client = Julep(
    api_key=os.getenv("JULEP_API_KEY"),
    environment=os.getenv("JULEP_ENVIRONMENT", "production")
)

# Step 1: Create an Agent
agent = client.agents.create(
    name="Story Generator",
    model="claude-3.5-sonnet",
    about="A helpful AI assistant that specializes in writing and editing."
)

# Step 2: Define the Task using YAML
task_definition = yaml.safe_load("""
name: Write a short story
description: Write a short story about a magical garden
main:
- prompt:
  - role: system
    content: You are a creative story writer.
  - role: user
    content: $ f'Write a short story about {steps[0].input.topic}'
""")

# Step 3: Create the Task
task = client.tasks.create(
    agent_id=agent.id,
    **task_definition
)

# Step 4: Run the Task with input
execution = client.executions.create(
    task_id=task.id,
    input={"topic": "a magical garden"}
)

# Step 5: Wait for it to complete
while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
    print(f"⏳ Status: {result.status}")
    time.sleep(1)

# Step 6: Display result
if result.status == "succeeded":
    story = result.output["choices"][0]["message"]["content"]
    print("\n✅ Final Story:\n")
    print(story)
else:
    print(f"\n❌ Error: {result.error}")

