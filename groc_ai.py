
import os
from groq import Groq

def reporting(input,message): 

    api="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"

    #set GROQ_API_KEY in the secrets

    # Create the Groq client
    client = Groq(api_key=api )

    # Set the system prompt
    system_prompt = {
        "role": "system",
        "content":
        "You are a helpful assistant. You reply with very short answers."
    }

    # Initialize the chat history
    chat_history = [system_prompt]

# while True:
    # Get user input from the console
    user_input = f"{message} \n {input}"

    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(model="llama3-70b-8192",
                                            messages=chat_history,
                                            max_tokens=8192,
                                            temperature=1.2)
    # Append the response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    # Print the response
    return response.choices[0].message.content