from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

@app.post("/chat")
async def chat_api(message: Message):
    user_input = message.content

    # Add user message to chat history
    bot_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Generate a response while limiting the total chat history to 1000 tokens
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    response_content = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return {"role": "assistant", "content": response_content}

class Message(BaseModel):
    content: str

class Response(BaseModel):
    role: str
    content: str

@app.post("/chat")
async def chat(message: Message):
    user_input = message.content
    # Your existing chat processing logic here
    return {"role": "assistant", "content": "This is a dummy response."}

# Create a Flask app
flask_app = Flask(__name__)
run_with_ngrok(flask_app)  # starts ngrok when the app is run

# Define a Flask route
@flask_app.route("/")
def home():
    return "<h1>Running FastAPI on Google Colab with ngrok!</h1>"

app_thread = threading.Thread(target=run_app)
app_thread.start()

# Allow some time for the FastAPI app to start
time.sleep(2)

# Run the Flask app with ngrok
flask_app.run()
