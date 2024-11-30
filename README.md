# Django and React Project

This project combines a Django backend with a React frontend to develop a spotify manipulation site so that you can share songs to your friends in a certain event. It is designed to be run locally or on a development server.

## Features

- Backend: Django (Python) with a REST API.
- Frontend: React (JavaScript) for the user interface.
- Database: SQLite (or any preferred database).
- Authentication and dynamic routing.

---

## Prerequisites

Make sure you have the following installed on your machine:

- Python (version 3.10+)
- Node.js (version 16+)
- npm or Yarn
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Setting Up the Backend (Django)

#### a. Create a virtual environment:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### b. Install required packages:

```bash
pip install -r requirements.txt
```

#### c. Set up environment variables:

Create a .env file in the backend directory.```
Add the following variables:

```
CLIENT_ID = your_spotify_client_id
CLIENT_SECRET = ypur_spotify_client_secret
REDIRECT_URI = ""
```

Note: Obtain the CLIENT_ID and CLIENT_SECRET by registering your app on the Spotify Developer Dashboard https://developer.spotify.com/dashboard.

#### d. Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### e. Run the Django server:

```bash
python manage.py runserver
```

The backend will be available at http://127.0.0.1:8000.

### 3. Setting up the frontend (React)

#### a. Navigate to the frontend directory:

```bash
cd frontend
```

#### b. Install dependencies:

```bash
npm install
# or
yarn install
```

#### c. Start the React development server:

```bash
npm start
# or
yarn start
```

## Running Tests

### 1. For the backend:

```bash
python manage.py test
```

### 2. For the frontend:

```bash
npm test
# or
yarn test
```

### 3. Building the React Frontend for Production

```bash
npm run build
# or
yarn build
```

The production build will be located in the build/ directory.

## Learn More

Django Documentation https://docs.djangoproject.com/
React Documentation https://reactjs.org/
Spotify API Documentation https://developer.spotify.com/documentation/web-api/
Django REST Framework Documentation https://www.django-rest-framework.org/