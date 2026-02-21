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

            for tx in transactions:

                if tx.date in seen_dates:
                    invalid.append({**tx.model_dump(), "message": "Duplicate timestamp"})
                    continue

                if tx.remanent < 0:
                    invalid.append({**tx.model_dump(), "message": "Negative remanent"})
                    continue

                seen_dates.add(tx.date)
                valid.append(tx)

            return valid, invalid
        except Exception as e :
            raise e