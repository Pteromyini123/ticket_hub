import httpx
from src.models import Ticket
from src.utils.cache import get_cache, set_cache
from src.utils.logger import logger

# URLs where we get the data from
todos_url = "https://dummyjson.com/todos"
users_url = "https://dummyjson.com/users"

# this function gets all tickets from the external API
async def fetch_tickets() -> list[Ticket]:
    cached = get_cache("tickets")

    if cached:
        logger.info("Returning tickets from cache")
        return cached

    async with httpx.AsyncClient() as client:
        logger.info("Fetching tickets from DummyJSON...")

        # get todos
        todos_response = await client.get(todos_url)
        todos_data = todos_response.json()
        todos = todos_data["todos"]

        # get users
        users_response = await client.get(users_url)
        users_data = users_response.json()
        users = users_data["users"]

    # make a dictionary to find username by user id
    user_map = {}
    for user in users:
        user_map[user["id"]] = user["username"]

    # this function decides priority level
    def calculate_priority(todo_id: int) -> str:
        number = todo_id % 3
        if number == 0:
            return "low"
        elif number == 1:
            return "medium"
        else:
            return "high"

    tickets = []

    # make list of tickets from todos
    for todo in todos:
        ticket = Ticket(
            id=todo["id"],
            title=todo["todo"],
            status="closed" if todo["completed"] == True else "open",
            priority=calculate_priority(todo["id"]),
            assignee=user_map.get(todo["userId"], "unknown")
        )
        tickets.append(ticket)

    set_cache("tickets", tickets, ttl=60)

    return tickets
