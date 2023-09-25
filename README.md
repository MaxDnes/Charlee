# Charlee
Telegram Bot

This README provides an overview of the Python Telegram bot project, including its functionality and how to set it up and run it.
Project Overview

This Python Telegram bot is a versatile and user-friendly bot that offers various features, including task management, temporary email management, AI-based commands, and a feedback system. Users can interact with the bot through a menu of buttons to perform different actions and access various functionalities.
Features:

1. Task Management: Users can create, manage, and track their tasks using the bot. They can add tasks, set due dates, and mark tasks as completed.

2. Temporary Email Management: Users can generate temporary email addresses, receive emails sent to those addresses, and perform actions like refreshing the inbox and deleting email addresses. It supports both temp-mail.org and secmail.pro services.

3. AI Commands: The bot can interact with an AI model to perform actions like answering questions, generating text, and creating images based on prompts. It utilizes the OpenAI API.

4. Feedback System: Users can report bugs and leave reviews through the bot, helping improve its functionality. Feedback is stored in a MySQL database.

Project Structure

handlers.py: Contains the core functionality of the bot, including handling user interactions and executing various actions.
database: Contains modules for managing user data, tasks, emails, and feedback in the bot. It uses mysql.connector to interact with a MySQL database.
handlers: Includes modules for handling different bot functionalities, such as AI interactions and email management.
buttons: Provides button layouts used for navigation within the bot.
help_messages: Contains help and informational messages displayed to users.

Getting Started

Follow these steps to set up and run the Telegram bot:
Prerequisites

    Python 3.7 or higher
    python-telegram-bot library
    mysql-connector-python library
    OpenAI Python library
    A MySQL database for storing user data, feedback, and tasks.
    OpenAI API credentials for AI-related functionality.
    Secmail.pro API credentials for temporary email functionality.

Installation

    Clone the repository to your local machine:

    bash

git clone <repository-url>
cd <repository-directory>

Install the required Python packages:

bash

    pip install python-telegram-bot mysql-connector-python openai secmail-pro

    Configure your MySQL database connection in the appropriate location in the code.

    Configure your OpenAI API credentials in the appropriate location in the code.


Running the Bot

Run the bot by executing the following command:

bash

python main.py

The bot should now be active and ready to respond to user interactions on Telegram.
Usage

    Start a conversation with the bot on Telegram.

    Use the provided buttons to navigate through the different functionalities, including task management, email management, AI interactions, and more.

    Follow the on-screen prompts and instructions to perform specific actions within each functionality.

    Enjoy using the bot to manage tasks, interact with AI, and more.

Support and Feedback

If you encounter any issues with the bot or have suggestions for improvement, please feel free to create an issue in the GitHub repository or contact the bot's developers for assistance.
Credits

    python-telegram-bot: Python library for interacting with the Telegram Bot API.
    mysql-connector-python: MySQL connector library for Python.
    OpenAI Python: Python client for the OpenAI API.
    Secmail: Python library for interacting with the Secmail API.