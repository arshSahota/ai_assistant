# 🤖 Nova AI Assistant

A customer support chatbot built with Python, Flask, HTML, CSS, JavaScript, and JSON.

🔗 Live Demo: https://ai-assistant-z0jo.onrender.com

---

## Overview

Nova AI Assistant is a conversational customer support application designed for a fictional company called Nova Services.

The application allows users to:

- Track order status
- View customer information
- Check billing details
- Review customer order history
- View latest customer orders
- Ask support and FAQ questions

The project demonstrates full-stack web development concepts including frontend-backend communication, API design, JSON data processing, intent recognition, and entity extraction.

---

## Features

- Order Tracking

- Customer Lookup

- Billing Lookup

- Order History

- Latest Order Search

- FAQ Support

- Intent Recognition

- Entity Extraction

- Interactive Chat Interface

- Analytics Dashboard

- Responsive User Interface

---

## Technologies Used

### Backend

- Python
- Flask

### Frontend

- HTML
- CSS
- JavaScript

### Data Storage

- JSON

### Deployment

- Render

---

## Example Queries

Try the following in the chatbot:

```text
ORD102
```

```text
customer C001
```

```text
orders C001
```

```text
latest order C001
```

```text
balance C001
```

```text
refund policy
```

```text
help
```

---

## Project Architecture

Frontend (HTML/CSS/JavaScript)

↓ API Request

Flask Backend

↓ Intent Recognition

Chatbot Logic

↓ Data Retrieval

JSON Database

↓ Response Generation

User Interface

---

## How It Works

### Intent Recognition

The chatbot analyzes user messages and determines what the user wants.

Example:

```text
ORD102
```

Intent:

```text
Order Tracking
```

---

### Entity Extraction

The chatbot extracts useful information from messages.

Example:

```text
ORD102
```

Entity:

```text
Order ID = ORD102
```

Example:

```text
customer C001
```

Entity:

```text
Customer ID = C001
```

---

### Data Retrieval

After identifying the user's intent and extracting relevant entities, the application searches the JSON files and returns the appropriate response.

---

## Sample Data

The application uses fictional data including:

- Customers
- Orders
- Billing Records
- FAQ Information

No real customer information is used.

---

## Running Locally

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project:

```bash
cd Nova-AI-Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Live Demo

https://ai-assistant-z0jo.onrender.com

---

## Future Improvements

- Conversation memory
- Advanced NLP-based intent matching
- Customer authentication
- Sentiment analysis
- Database integration
- AI-powered response generation

---

## Author

Arshdeep Kaur

BCIT Computer Systems Technology Student

Built as a portfolio project to demonstrate Python, Flask, web development, and conversational AI concepts.
