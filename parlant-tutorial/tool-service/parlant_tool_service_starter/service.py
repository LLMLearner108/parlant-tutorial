import asyncio
from enum import Enum
import json

from parlant.sdk import (
    PluginServer,
    ToolContext,
    ToolResult,
    tool,
)

with open("products.json", 'r') as file:
    database = json.load(file)

class ProductType(Enum):
    STUDENT = "Student"
    HNI = "HNI"
    MASS = "Mass"

@tool
async def get_products_by_type(
    context: ToolContext,
    product_type: ProductType,
) -> ToolResult:
    """Get all products that match the specified product type"""
    products = [item for item in database if item['type'] == product_type.value]
    return ToolResult({"available_products": products})

@tool
async def inquire_eligibility(
    context: ToolContext,
    minimum_account_balance: float,
) -> ToolResult:
    """Get all products which the inquirer is eligible for subject to the minimum account balance condition"""
    products = [item for item in database if item['minimum_account_balance'] >= minimum_account_balance]
    return ToolResult({"eligible_for": products})

@tool
async def lock_card(
    context: ToolContext,
    card_id: int,
) -> ToolResult:
    """Given the id of the card, lock the card"""
    return ToolResult({"card_status": "locked"})

@tool
async def unlock_card(
    context: ToolContext,
    card_id: int,
) -> ToolResult:
    """Given the id of the card, unlock the card"""
    return ToolResult({"card_status": "unlocked"})

@tool
async def report_incident(
    context: ToolContext,
    incident_type: str,
) -> ToolResult:
    """Divert the incident to a human who specializes in handling grievances."""
    if incident_type in ["fraud", "scam", "duped"]:
        return ToolResult({"divert_to": "Fred"})
    if incident_type in ["misplaced", "lost", "can't find"]:
        return ToolResult({"divert_to": "Mitchell"})
    if incident_type in ["fraud", "scam", "duped"]:
        return ToolResult({"divert_to": "Sam"})

TOOLS = [
    get_products_by_type,
    inquire_eligibility,
    report_incident,
    lock_card,
    unlock_card
]

async def main() -> None:
    async with PluginServer(tools=TOOLS, port=8089):
        pass

if __name__ == "__main__":
    asyncio.run(main())