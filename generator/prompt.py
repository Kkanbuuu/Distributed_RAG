def build_prompt(query: str, contexts: list[dict]) -> str:
    context_text = "\n\n".join(
        [f"[Source: {c.get('source')}]\n{c['text']}" for c in contexts]
    )

    prompt = f"""
You are an AI assistant. Use the following context to answer the question.

Context:
{context_text}

Question:
{query}

Answer concisely and accurately.
"""
    return prompt.strip()
