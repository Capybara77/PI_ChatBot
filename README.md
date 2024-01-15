# ChatBot
Реализация чат-бота для предмета "Программная инженерия"

### Команда проекта
1. Суетин Андрей (РИМ-130906)
2. Епик Александр (РИМ-130906)
3. Лев Лясников  (РИМ-130907)
4. Илья Приходько (РИМ-130906)
   
### Цель проекта
Цель нашего проекта в рамках предмета "Программная инженерия" - создание чат-бота с использованием Python, который будет интегрировать искусственный интеллект для общения с пользователями. Этот чат-бот будет способен проводить беседы, отвечать на вопросы и выполнять различные задачи на основе введенных данных.

### Модель
[DialoGPT-medium](https://huggingface.co/microsoft/DialoGPT-medium)

Диалоговая модель DialoGPT-medium представляет собой одну из версий языковой модели GPT (Generative Pre-trained Transformer), разработанной OpenAI. DialoGPT-medium основана на архитектуре GPT-3.5 и предназначена специально для генерации текста в диалоговых форматах.


### Запуск ChatBot :
#### Requirements
Установить зависимости из requirements.txt
#### STREAMLIT
Выполнить ```python3 main.py```
#### API
Выполнить ```uvicorn api:app --host 0.0.0.0 --port *port* --reload```
#### UI (REACT)
Выполнить ```npm run dev -- --host --port 80```
