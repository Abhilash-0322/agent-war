from groq import Groq
import asyncio
import dotenv
import os
dotenv.load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": "You are the Best coder in the world"
            ,
            "role": "user",
            "content": "I am the best coder in the world"
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# for chunk in completion:
#     print(chunk.choices[0].delta.content or "", end="")
async def print_chunks_async(completion):
    for chunk in completion:
        await asyncio.sleep(0)  # Yield control to event loop
        print(chunk.choices[0].delta.content or "", end="")

asyncio.run(print_chunks_async(completion))