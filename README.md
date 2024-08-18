# Learning Management Portal app

## Overview

Welcome to the Learning Management Portal, where Artificial Intelligence enhances the learning experience. Engage with course materials, submit various assignments, and get AI-powered support. This README will guide you through the installation, setup, and usage of the application.

## Features

- **Course Content Access:** Read and interact with diverse educational materials.
- **Assignment Submissions:** Submit MCQs, MSQs, numeric problems, and coding tasks.
- **AI Assistance:** Get material summaries, contextual hints, and interactive document chat.
- **Coding Support:** Receive hints and guidance for coding assignments.

## Technologies Used

The app leverages the following technologies and frameworks:

- **Python 3**: The primary programming language for the application.
- **FastAPI**: Used for building the backend of the application, providing fast and efficient API endpoints with built-in validation and documentation.
- **React**: A JavaScript library for building user interfaces, used in the frontend of the application.
- **MongoDB**: A NoSQL database used for storing and managing application data.
- **LangChain**: A framework for building applications with LLMs (Large Language Models)

## Prerequisites

To run the app on your local device, you will need to have the following installed:

- Python 3
- Pip (Python package manager)
- Node.js
- Npm (Node package manager)
- Java
- MongoDB (ensure MongoDB server is running)

## Installation

Follow these steps to get your development environment set up:

### 1. Clone the Repository

```
git clone https://github.com/De-Sagnik/soft-engg-project-may-2024-se-may-22.git
```

### 2. Installed Required Packages

- Create a virtual environment and install the dependencies

```
python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt
```

### 3. Set up Environment Variables

- Create a .env file in the root directory of the project and add the following environment variables

```
DATABASE = "se_project"
DATABASE_USERNAME = "user"
DATABASE_PASSWORD = "password"
SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
GOOGLE_CLIENT_ID = google_client_id
GOOGLE_CLIENT_SECRET = google_client_secret
GOOGLE_REDIRECT_URI = "http://localhost:8000/oauth/callback"
```

> ```If you want to use the local database, replace the uri with "mongodb://localhost:27017" in db.py which is located in database folder```

## Running the app

### 1. Starting the application

- For Backend

```python
python3 main.py
```

- For Frontend

```js
npm run dev
```

### 2. Access the app

- Open your web browser and navigate to http://localhost:8000 


