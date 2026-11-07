# RecallDesk – AI-Powered Customer Support Agent

## Overview
RecallDesk is an AI-powered customer support agent that uses persistent memory to provide continuous and personalized customer support.

Unlike traditional chatbots that treat every conversation as new, RecallDesk uses Hindsight to remember previous customer issues, troubleshooting steps, and outcomes. This helps the AI provide more relevant responses when customers return.

## Problem Statement
Traditional customer support chatbots often forget previous conversations. Customers have to explain their problems repeatedly, resulting in a frustrating support experience.

## Solution
RecallDesk addresses this problem by combining a Large Language Model with long-term memory. It retrieves relevant past conversations and uses them to generate context-aware responses.

## Key Features
- AI-powered customer support using Groq.
- Persistent memory using Hindsight.
- Retrieves previous customer conversations.
- Remembers reported problems and attempted solutions.
- Provides context-aware troubleshooting suggestions.
- Simple web-based chat interface.

## Technologies Used
- Python
- Flask
- HTML
- CSS
- JavaScript
- Groq API
- Hindsight Memory

## How It Works
1. The customer enters their Customer ID and message.
2. The Flask backend receives the request.
3. Hindsight retrieves relevant previous conversations.
4. Groq generates a response using the retrieved context.
5. The conversation is stored in Hindsight for future reference.
6. The frontend displays the AI response and retrieved memories.

## Project Structure
```text
hackthon/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_LINK
   ```

2. Open the project folder:
   ```bash
   cd hackthon
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file and configure your API credentials:
   ```text
   HINDSIGHT_API_KEY=your_hindsight_api_key
   HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
   HINDSIGHT_BANK_ID=recall-desk
   GROQ_API_KEY=your_groq_api_key
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Open your browser and visit:
   ```text
   http://127.0.0.1:5000
   ```

## Limitations
- The current prototype uses a shared Hindsight memory bank, so customer-level memory isolation is not yet implemented.
- Memory retrieval may return duplicate or overlapping information.
- The application requires an internet connection and valid API credentials.

## Future Enhancements
- Implement secure customer-specific memory isolation.
- Improve memory filtering and summarization.
- Add customer authentication.
- Improve memory management and analytics.

## Team
Tech Squad – RecallDesk Project

