from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from src.models import Ticket
from src.services import fetch_tickets
from httpx import AsyncClient
from src.utils.logger import logger
from src.utils.cache import get_cache, set_cache
from src.routes.auth import get_current_user

router = APIRouter()

# return list of tickets, filtered if needed
@router.get("/", response_model=List[Ticket])
async def list_tickets(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
):
    logger.info("GET /tickets")

    all_tickets = await fetch_tickets()
    filtered = []

    for ticket in all_tickets:
        if status and ticket.status != status.lower():
            continue
        if priority and ticket.priority != priority.lower():
            continue
        filtered.append(ticket)

    return filtered[skip: skip + limit]

# search tickets by keyword in title
@router.get("/search", response_model=List[Ticket])
async def search_tickets(search: str = Query(..., description="Keyword to search in title")):
    logger.info(f"Searching tickets for keyword: {search}")

    all_tickets = await fetch_tickets()
    results = []

    for ticket in all_tickets:
        if search.lower() in ticket.title.lower():
            results.append(ticket)

    return results

# show stats (JWT protected)
@router.get("/stats")
async def ticket_stats(user=Depends(get_current_user)):
    print("CURRENT USER:", user)
    all_tickets = await fetch_tickets()

    status_count = {"open": 0, "closed": 0}
    priority_count = {"low": 0, "medium": 0, "high": 0}

    for ticket in all_tickets:
        status_count[ticket.status] += 1
        priority_count[ticket.priority] += 1

    return {
        "user": user["username"],
        "status": status_count,
        "priority": priority_count
    }


# get single ticket by ID
@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int):
    logger.info(f"GET /tickets/{ticket_id}")

    cache_key = f"ticket:{ticket_id}"
    cached_ticket = get_cache(cache_key)

    if cached_ticket:
        logger.info(f"Returning ticket {ticket_id} from cache")
        return cached_ticket

    async with AsyncClient() as client:
        todos_response = await client.get(f"https://dummyjson.com/todos/{ticket_id}")
        if todos_response.status_code != 200:
            logger.warning(f"Ticket {ticket_id} not found")
            return {"error": f"Ticket with id {ticket_id} not found"}, 404

        todo = todos_response.json()

        user_response = await client.get(f"https://dummyjson.com/users/{todo['userId']}")
        if user_response.status_code == 200:
            user = user_response.json()
        else:
            user = {}

    ticket_data = {
        "id": todo["id"],
        "title": todo["todo"],
        "status": "closed" if todo["completed"] else "open",
        "priority": ["low", "medium", "high"][todo["id"] % 3],
        "assignee": user.get("username", "unknown")
    }

    result = {
        "ticket": ticket_data,
        "raw": todo
    }

    set_cache(cache_key, result, ttl=60)

    return result

