from julep import Julep
import os
from dotenv import load_dotenv

load_dotenv()

client = Julep(
    api_key=os.getenv('JULEP_API_KEY'),
    environment=os.getenv('JULEP_ENVIRONMENT', 'production')
)

# Test connection
agent = client.agents.create(
    name="Test Agent",
    model="claude-3.5-haiku",
    about="A test agent"
)
print(f"Successfully created agent: {agent.id}")
