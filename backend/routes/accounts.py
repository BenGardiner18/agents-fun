from fastapi import APIRouter, HTTPException
from typing import List
from models import Account, AccountCreate, AccountUpdate, MessageResponse
from database import db_manager

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[Account])
def get_accounts():
    """Get all accounts"""
    rows, cur = db_manager.execute_query("SELECT * FROM accounts ORDER BY created_at DESC")
    
    accounts = []
    for row in rows:
        account = db_manager.row_to_dict(row, cur)
        accounts.append(Account(**account))
    return accounts

@router.get("/{account_id}", response_model=Account)
def get_account(account_id: int):
    """Get a specific account by ID"""
    row, cur = db_manager.execute_single("SELECT * FROM accounts WHERE id = %s", (account_id,))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account = db_manager.row_to_dict(row, cur)
    return Account(**account)

@router.post("/", response_model=Account)
def create_account(account: AccountCreate):
    """Create a new account"""
    row, cur = db_manager.execute_insert(
        "INSERT INTO accounts (name, industry, plan, status) VALUES (%s, %s, %s, %s) RETURNING *",
        (account.name, account.industry, account.plan, account.status)
    )
    
    created_account = db_manager.row_to_dict(row, cur)
    return Account(**created_account)

@router.put("/{account_id}", response_model=Account)
def update_account(account_id: int, account: AccountUpdate):
    """Update an existing account"""
    row, cur = db_manager.execute_update(
        "UPDATE accounts SET name = %s, industry = %s, plan = %s, status = %s WHERE id = %s RETURNING *",
        (account.name, account.industry, account.plan, account.status, account_id)
    )
    
    if row is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    updated_account = db_manager.row_to_dict(row, cur)
    return Account(**updated_account)

@router.delete("/{account_id}", response_model=MessageResponse)
def delete_account(account_id: int):
    """Delete an account"""
    row_count = db_manager.execute_delete("DELETE FROM accounts WHERE id = %s", (account_id,))
    
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return MessageResponse(message="Account deleted successfully") 