from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import logging
from fastapi.middleware.cors import CORSMiddleware

logging.set_verbosity_error()

app = FastAPI()

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
step = 0

# Initialize chat history
messages = []
tokens = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/clear")
def clear():
    messages = []
    tokens = None

# Endpoint для обработки пользовательского ввода
@app.get("/chat")
async def chat(input_data):
    global tokens

    user_input = input_data
    if not user_input:
        raise HTTPException(status_code=400, detail="User input is required")

    # Display user message in chat message container
    messages.append({"role": "user", "content": user_input})

    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([tokens, new_user_input_ids], dim=-1) if tokens is not None else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    tokens = chat_history_ids

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    # Display assistant response in chat message container
    messages.append({"role": "assistant", "content": response})

    return JSONResponse(content={"response": response, "messages": messages})
