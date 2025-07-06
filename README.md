# TicketHub API

FastAPI project for managing and viewing support tickets.  
Tickets are fetched from DummyJSON

## Features

- Fetch all tickets
- Search tickets by keyword
- Filter by status and priority
- View ticket by ID
- See basic stats (authentification needed)
- JWT-based login (uses DummyJSON)
- Basic caching and logging

## How to run it

1. Clone the project  
2. Make sure you have Python 3.11+
3. Install all dependencies from requirements.txt (pip install -r requirements.txt)
4. Run the server
Terminal: uvicorn src.main:app --reload
5. Open: http://127.0.0.1:8000/docs
6. Log in:
{
  "username": "emilys",
  "password": "emilyspass"
}
7. In the top right corner click "Authorize" and enter only the token you got after the login
(eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWlseXMifQ.TUK15RDccXZP_-v4Z-plLMdJ66M0sT2lWXaQPESdeJw)

## Notes
Chat GPT was used to layout general structure of the project and to help find and correct errors in code