from typing import  Dict
from datetime import datetime 
import math


class ReturnService:
    def __init__(self):
        self.NPS_RATE = 0.0711
        self.INDEX_RATE = 0.1449
   
    async def calculate_compound(self,P, r, t):
        return P * ((1 + r) ** t)
 
    async def adjust_inflation(self,amount, inflation, t):
        return amount / ((1 + inflation) ** t)
 
    async def calculate_returns(self,amount, age, inflation, rate):
        try : 
            years = max(60 - age, 5)

            final_value = self.calculate_compound(amount, rate, years)
            real_value = self.adjust_inflation(final_value, inflation, years)

            return real_value
        except Exception as e :
            raise e
    
    
    async def calculate_nps_tax(self,wage, invested):
        try : 
            deduction = min(invested, wage * 0.10, 200000) 
            if wage <= 700000:
                return 0 
            taxable_before = wage
            taxable_after = wage - deduction

            tax_before = max(taxable_before - 700000, 0) * 0.10
            tax_after = max(taxable_after - 700000, 0) * 0.10

            return tax_before - tax_after
        except Exception as e :
            raise e
        




    async def calculate_ceiling_remanent(self, amount: float):
        ceiling = math.ceil(amount / 100) * 100
        remanent = ceiling - amount
        return ceiling, remanent

    async def compound_interest(self, principal: float, rate: float, years: int):
        return principal * ((1 + rate) ** years)

    async def adjust_inflation(self, amount: float, inflation: float, years: int):
        return amount / ((1 + inflation / 100) ** years)
 
    async def calculate_tax(self, income: float):

        if income <= 700000:
            return 0

        tax = 0

        if income > 1500000:
            tax += (income - 1500000) * 0.30
            income = 1500000

        if income > 1200000:
            tax += (income - 1200000) * 0.20
            income = 1200000

        if income > 1000000:
            tax += (income - 1000000) * 0.15
            income = 1000000

        if income > 700000:
            tax += (income - 700000) * 0.10

        return tax
 
    async def process_transactions(self, data: Dict):

        age = data["age"]
        wage = data["wage"]
        inflation = data["inflation"]
        q_periods = data.get("q", [])
        p_periods = data.get("p", [])
        k_periods = data.get("k", [])
        transactions = data["transactions"]

        processed_transactions = []

        total_amount = 0
        total_ceiling = 0
 
        for tx in transactions:

            amount = tx["amount"]
            timestamp = datetime.strptime(tx["date"], "%Y-%m-%d %H:%M:%S")
 
            if amount < 0:
                continue

            ceiling, remanent = await self.calculate_ceiling_remanent(amount)

            total_amount += amount
            total_ceiling += ceiling
 
            matched_q = None
            for q in q_periods:
                start = datetime.strptime(q["start"], "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(q["end"], "%Y-%m-%d %H:%M:%S")

                if start <= timestamp <= end:
                    if not matched_q or start > datetime.strptime(matched_q["start"], "%Y-%m-%d %H:%M:%S"):
                        matched_q = q

            if matched_q:
                remanent = matched_q["fixed"]
 
            for p in p_periods:
                start = datetime.strptime(p["start"], "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(p["end"], "%Y-%m-%d %H:%M:%S")

                if start <= timestamp <= end:
                    remanent += p["extra"]

            processed_transactions.append({
                "timestamp": timestamp,
                "remanent": remanent
            })
 
        savings_by_dates = []

        years = max(60 - age, 5)

        for k in k_periods: 
            start = datetime.strptime(k["start"], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(k["end"], "%Y-%m-%d %H:%M:%S")

            period_amount = 0

            for tx in processed_transactions:
                if start <= tx["timestamp"] <= end:
                    period_amount += tx["remanent"]

            savings_by_dates.append({
                "start": k["start"],
                "end": k["end"],
                "amount": period_amount
            })

        return {
            "total_amount": total_amount,
            "total_ceiling": total_ceiling,
            "savings_by_dates": savings_by_dates,
            "years": years,
            "wage": wage,
            "inflation": inflation
        }
 
    async def calculate_index_returns(self, data: Dict):

        result = await self.process_transactions(data)

        final_response = []

        for item in result["savings_by_dates"]:

            amount = item["amount"]

            future_value = await self.compound_interest(amount, 0.1449, result["years"])
            real_value = await self.adjust_inflation(future_value, result["inflation"], result["years"])

            final_response.append({
                "start": item["start"],
                "end": item["end"],
                "amount": round(amount, 2),
                "profit": round(real_value - amount, 2),
                "taxBenefit": 0.0
            })

        return {
            "transactionsTotalAmount": round(result["total_amount"], 2),
            "transactionsTotalCeiling": round(result["total_ceiling"], 2),
            "savingsByDates": final_response
        }
    
 