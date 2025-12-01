import time
#from huggingface_hub import InferenceClient
from groq import Groq
import config

client = Groq(api_key = config.GROQ_API_KEY)

def generate_answer(prompt: str):
    print("CONFIG" + config.GROQ_API_KEY)
    start = time.time()

    completion = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.2
    )

    answer = completion.choices[0].message.content
    latency = (time.time() - start) * 1000
    return answer, latency