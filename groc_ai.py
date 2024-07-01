import os
from groq import Groq

class groq:
    def __init__(self):
        self.count = 0
        self.api_keys = [
            "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",
            "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",
            "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"
        ]
        self.api_key_count = len(self.api_keys)

    def reporting(self, input, message): 
        # Cycle through the API keys
        api_key = self.api_keys[self.count % self.api_key_count]
        self.count += 1
        
        # Create the Groq client
        client = Groq(api_key=api_key)
        # Set the system prompt
        system_prompt = {
            "role": "system",
            "content": "You are a helpful assistant. You reply with very short answers."
        }

        # Initialize the chat history
        chat_history = [system_prompt]

        # Get user input from the console
        user_input = f"{message} \n {input}"

        # Append the user input to the chat history
        chat_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=chat_history,
            max_tokens=8192,
            temperature=1.2
        )

        # Append the response to the chat history
        chat_history.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

        # Print the response
        return response.choices[0].message.content


