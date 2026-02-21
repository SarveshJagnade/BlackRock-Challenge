

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