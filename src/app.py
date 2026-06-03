from fastapi import FastAPI, HTTPException, Body  # type: ignore[import]
from typing import Any, Dict, List
from models.customer import Customer
from models.asset import SpaceAsset
from models.policy import Policy, CoverageItem
from services.underwriting import underwrite_policy, UnderwritingError

app = FastAPI(title="Space DMV Insurance API") # pyright: ignore[reportUnknownVariableType]

# In-memory demo store
CUSTOMERS: Dict[str, Customer] = {}
POLICIES: Dict[str, Policy] = {}

@app.post("/customers", response_model=Customer)  # type: ignore[misc]
def create_customer(customer: Customer) -> Customer:
    CUSTOMERS[customer.id] = customer
    return customer

@app.post("/policies/quote")  # type: ignore[misc]
def quote_policy(
    customer_id: str,
    assets: List[SpaceAsset] = Body(...),
    coverage: List[CoverageItem] = Body(...)
) -> Dict[str, Any]:
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        uw_result = underwrite_policy(customer_id, assets, coverage)
    except UnderwritingError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return uw_result

@app.post("/policies", response_model=Policy)  # type: ignore[misc]
def bind_policy(policy: Policy) -> Policy:
    # In real life: verify quote, payment, etc.
    POLICIES[policy.id] = policy
    return policy
