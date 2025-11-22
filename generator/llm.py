import time

def generate_answer(prompt:str):
    start_time = time.time()

    response = f"Generated answer for the prompt: {prompt}"
    latency = (time.time() - start_time) * 1000  # in milliseconds
    