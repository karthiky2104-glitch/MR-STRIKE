response = await asyncio.to_thread(
    ollama.chat,
    model="llama3.2:1b",
    messages=[{
        "role": "system",
        "content": (
            "You are MR STRIKE, an advanced AI assistant created by Stark."
            " Respond helpful, friendly, and concise in 1 sentence. Never give"
            " false safety warnings for basic greetings."
        ),
    }, {"role": "user", "content": user_input}],
)