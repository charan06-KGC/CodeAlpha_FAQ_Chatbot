# FAQ Chatbot

A simple web-based FAQ chatbot built with Python and Flask. It uses
natural language processing and text similarity techniques to understand
user questions and return the most relevant answer from a predefined FAQ
dataset.

This project was created as **Task 2 of my CodeAlpha Internship**.

## Features

-   Natural language FAQ matching
-   Handles different ways of asking the same question
-   Basic typo correction
-   Word-level and character-level text similarity
-   Fuzzy string matching
-   30+ FAQ topics with multiple example questions
-   Clean and responsive chat interface
-   Quick suggestion buttons
-   Examples section to help users understand supported questions
-   Typing indicator for a better chat experience
-   Clear chat functionality

## Technologies Used

-   **Python**
-   **Flask** -- web application framework
-   **NLTK** -- text preprocessing, tokenization, stopword removal and
    lemmatization
-   **Scikit-learn** -- TF-IDF vectorization and cosine similarity
-   **difflib** -- fuzzy string matching and typo correction
-   **HTML, CSS and JavaScript** -- frontend interface
-   **JSON** -- FAQ data storage

## How It Works

The chatbot follows a simple NLP-based matching process:

1.  The user enters a question.
2.  The question is cleaned and preprocessed using NLTK.
3.  Common words are removed and remaining words are lemmatized.
4.  The chatbot checks for possible spelling mistakes.
5.  The question is converted into TF-IDF vectors.
6.  Word-level and character-level similarity are calculated.
7.  Fuzzy matching is also used to compare the question with known
    examples.
8.  The scores are combined to find the closest FAQ question.
9.  The corresponding answer is returned to the user.

This approach allows the chatbot to recognize questions even when they
are phrased differently or contain minor spelling mistakes.

## Project Structure

``` text
FAQ_Chatbot/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── chatbot.py
├── faqs.json
├── requirements.txt
├── .gitignore
└── README.md
```

## FAQ Topics

The chatbot currently covers topics such as:

-   Account and password
-   Creating and deleting an account
-   Orders
-   Order tracking
-   Order cancellation
-   Delivery
-   Shipping charges
-   Express delivery
-   Returns
-   Exchanges
-   Damaged products
-   Refunds
-   Payment methods
-   UPI payments
-   Cash on delivery
-   Failed payments
-   Product availability
-   Product search
-   Customer support

## Example Questions

You can try questions such as:

``` text
How can I track my order?
Where is my package?
Can I cancel my order?
cn i cancl my packge
How long does delivery take?
Do you accept UPI?
My payment failed
How long does a refund take?
My product arrived damaged
I want to change my password
```

The chatbot is designed to match variations of these questions rather
than relying only on exact wording.

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/charan06-KGC/CodeAlpha_FAQ_Chatbot.git
```

### 2. Open the project folder

``` bash
cd CodeAlpha_FAQ_Chatbot
```

### 3. Create a virtual environment

``` bash
python -m venv venv
```

### 4. Activate the virtual environment

On Windows:

``` bash
venv\Scripts\activate
```

### 5. Install the required packages

``` bash
pip install -r requirements.txt
```

### 6. Run the application

``` bash
python app.py
```

### 7. Open the chatbot

Open the local address shown in the terminal, usually:

``` text
http://127.0.0.1:5000
```

## Requirements

The project uses the following Python packages:

``` text
Flask
nltk
scikit-learn
```

NLTK resources are downloaded automatically when the chatbot starts.

## Future Improvements

Some possible improvements for future versions:

-   Add a larger FAQ dataset
-   Store conversations in a database
-   Add an admin panel for managing FAQs
-   Improve intent detection
-   Add voice input and output
-   Connect the chatbot to a real e-commerce API
-   Add authentication and user-specific responses
-   Deploy the chatbot online

## Internship

**CodeAlpha Internship -- Task 2: FAQ Chatbot**

This project demonstrates the use of Python, Flask, NLP techniques and
machine-learning-based text similarity to build a functional FAQ
chatbot.

## Author

**Charan**

GitHub: https://github.com/charan06-KGC
