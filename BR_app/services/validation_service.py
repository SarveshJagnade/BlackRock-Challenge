from typing import List 
from BR_app.dataclasses.transaction import Transaction


class ValidationService:
    def __init__(self):
        pass
        
    async def validate_transactions(self, wage: float, transactions: List[Transaction]):
        try : 
            valid = []
            invalid = []

            seen_dates = set() 
            total = 0
            for tx in transactions: 
                if tx.date in seen_dates:
                    invalid.append({**tx.model_dump(), "message": "Duplicate timestamp"})
                    continue

                if tx.amount < 0 or tx.remanent < 0 or tx.ceiling < 0:
                    invalid.append({**tx.model_dump(), "message": "Negative amount pass"})
                    continue
                total += tx.amount
                if total > wage :
                    invalid.append({**tx.model_dump(), "message": "Amount exceed wage"})
                    continue

                seen_dates.add(tx.date)
                valid.append(tx)
            return {
                "valid" : valid,
                "invalid" : invalid
            }
        except Exception as e :
            raise e