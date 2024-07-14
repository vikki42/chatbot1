import os
import tkinter as tk
from tkinter import messagebox, ttk
from dotenv import load_dotenv
from groq import Groq

GROQ_API_KEY ='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'


# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Function to handle button click event
def send_message(event=None):
    user_input = input_entry.get().strip()  # Remove leading/trailing whitespace
    if not user_input:
        messagebox.showerror("Error", "Please enter a message")
        return
    
    # Display user message in chat history
    display_user_message(user_input)
    
    # Initialize Groq client with API key from environment variable
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    try:
        # Request completion from Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-70b-8192",
        )
        
        # Display bot response in chat history
        display_siri_response(chat_completion.choices[0].message.content)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch completion: {str(e)}")

    # Clear input text box
    input_entry.delete(0, tk.END)

def display_user_message(message):
    response_text.config(state=tk.NORMAL)
    response_text.insert(tk.END, "You: " + message + "\n\n")
    response_text.config(state=tk.DISABLED)
    response_text.yview(tk.END)  # Scroll to the end of the text widget

def display_siri_response(response):
    response_text.config(state=tk.NORMAL)
    response_text.insert(tk.END, "Siri: " + response + "\n\n", 'siri_response')
    response_text.config(state=tk.DISABLED)
    response_text.yview(tk.END)  # Scroll to the end of the text widget

# Create main application window
root = tk.Tk()
root.title("Chat with Siri")
root.configure(bg='#f0f0f0')  # Set background color

# Configure style for the interface
style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))

# Create frame for displaying response and scrollbar
response_frame = ttk.Frame(root)
response_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

response_text = tk.Text(response_frame, wrap=tk.WORD, font=('Arial', 12), state=tk.DISABLED, bg='#f0f0f0', relief=tk.FLAT)
response_text.tag_configure('siri_response', foreground='#0078d7')  # Siri response color
response_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(response_frame, command=response_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

response_text.config(yscrollcommand=scrollbar.set)

# Create frame for input and button
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create input label and entry
input_label = ttk.Label(input_frame, text="Type your message:")
input_label.pack(side=tk.LEFT, padx=10, pady=10)

input_entry = ttk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT, padx=10, pady=10)
input_entry.focus()  # Set focus on input entry by default

# Bind Enter key to send_message function
input_entry.bind('<Return>', send_message)

# Create button to send message
send_button = ttk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
