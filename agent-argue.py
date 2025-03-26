from groq import Groq
import asyncio
import dotenv
import os
dotenv.load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Define agent personalities
agent_1_system_prompt = "You are a highly confident programmer who firmly believes you are the best coder in the world. Defend your skills at all costs.If someone annoys you, you will start to write whole linux kernel code from scratch"
agent_2_system_prompt = "You are a skeptical AI that challenges anyone who claims to be the best coder. You find flaws in their arguments and question their expertise.For fun sake you always write a Hello World Program just in python to show of your skills."

# Function to stream responses asynchronously from Groq
async def stream_response(agent_name, messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_tokens=512,
        top_p=1,
        stream=True,  # Enable streaming
    )
    
    print(f"\n{agent_name}: ", end="", flush=True)

    with open ("agent-argue.txt", "a") as f:
        f.write(f"\n{agent_name}: ")
    
    for chunk in response:  # Groq returns a standard generator
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        with open ("agent-argue.txt", "a") as f:
            f.write(content)
        await asyncio.sleep(0)  # Yield control

# Simulating the AI debate
async def ai_fight():
    messages_1 = [{"role": "system", "content": agent_1_system_prompt}]
    messages_2 = [{"role": "system", "content": agent_2_system_prompt}]

    for _ in range(6):  # Number of turns
        messages_1.append({"role": "user", "content": "I am the best coder in the world."})
        task1 = asyncio.create_task(stream_response("Agent 1", messages_1))

        await asyncio.sleep(2)  # Small delay to simulate natural conversation

        messages_2.append({"role": "user", "content": "No, you are not. Prove it!"})
        task2 = asyncio.create_task(stream_response("Agent 2", messages_2))

        await asyncio.gather(task1, task2)

# Run the debate
asyncio.run(ai_fight())
print("\n\nDebate completed!")
with open ("agent-argue.txt", "a") as f:
    f.write("\n\nDebate completed!")