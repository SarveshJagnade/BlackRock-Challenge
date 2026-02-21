from typing import List
from BR_app.dataclasses.periods import QPeriod, PPeriod, KPeriod
from BR_app.dataclasses.transaction import Transaction


class TemporalService:
    def __init__(self):
        pass

    async def apply_temporal_rules(self,transactions: List[Transaction], q_periods: List[QPeriod], p_periods: List[PPeriod]):
        try :  
            for tx in transactions: 
                applicable_q = [
                    q for q in q_periods
                    if q["start"] <= tx["date"] <= q["end"]
                ] 
                if applicable_q:
                    latest_q = sorted(applicable_q, key=lambda x: x["start"], reverse=True)[0]
                    tx["remanent"] = latest_q["fixed"]
 
                applicable_p = [
                    p for p in p_periods
                    if p["start"] <=  tx["date"] <= p["end"]
                ] 
                for p in applicable_p:
                    tx["remanent"] += p.extra

            return transactions
        except Exception as e : 
            raise e

    async def group_by_k(self,transactions: List[Transaction], k_periods: List[KPeriod]):
        try: 
            results = [] 
            for k in k_periods:
                total = sum(
                    tx["remanent"]
                    for tx in transactions
                    if k["start"] <= tx["date"] <= k["end"]
                )

                results.append({
                    "start": k.start,
                    "end": k.end,
                    "amount": total
                }) 
            return results
        except Exception as e :
            raise e