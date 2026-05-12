from fastapi import FastAPI, HTTPException
from typing import List
from .models.customer import Customer
from .models.asset import SpaceAsset
from .models.policy import Policy, CoverageItem
from .services.underwriting import underwrite_policy, UnderwritingError

app = FastAPI(title="Space DMV Insurance API")

# In-memory demo store
CUSTOMERS = {}
POLICIES = {}

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    CUSTOMERS[customer.id] = customer
    return customer

@app.post("/policies/quote")
def quote_policy(
    customer_id: str,
    assets: List[SpaceAsset],
    coverage: List[CoverageItem]
):
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        uw_result = underwrite_policy(customer_id, assets, coverage)
    except UnderwritingError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return uw_result

@app.post("/policies", response_model=Policy)
def bind_policy(policy: Policy):
    # In real life: verify quote, payment, etc.
    POLICIES[policy.id] = policy
    return policy
