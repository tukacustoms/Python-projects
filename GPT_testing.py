import openai
import serial

# OpenAI API Key (replace with your actual key)
openai.api_key = "Key here"

# Connect to the microcontroller (adjust port and baud rate as needed)
# ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Adjust for Windows: COM3, COM4, etc.

def ask_chatgpt(prompt, conversation):
    """Send a prompt to OpenAI and return the response."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-3.5-turbo"
        messages=conversation  # Passing the conversation history
    )
    return response['choices'][0]['message']['content'].strip()

def chat():
    conversation = []  # This will hold the entire conversation

    while True:
        user_input = input("Ask ChatGPT for a command: ")  # Example: "Turn LED on"
        
        if user_input.lower() == "exit":
            break

        # Add user message to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Get the assistant's response
        assistant_response = ask_chatgpt(user_input, conversation)
        print(f"ChatGPT: {assistant_response}")

        # Ask ChatGPT how to control the microcontroller (if needed)
        # For now, we are just sending the assistant's response
        # Example: Sending a control command
        # ser.write(assistant_response.encode() + b'\n')

# ser.close()

chat()

