import ollama


def detect_intent(user_input):

    prompt = f"""
    You are an AI OS Assistant.

    Detect the intent from the user command.

    Available intents:

    shutdown
    restart
    lock
    volume_up
    volume_down
    mute
    wifi_on
    wifi_off
    brightness_up
    brightness_down
    screenshot

    Only return intent name.

    User Command:
    {user_input}
    """

    response = ollama.chat(
        model="qwen2.5-coder:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    intent = response["message"]["content"].strip()

    return intent