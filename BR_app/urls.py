from fastapi import APIRouter

from BR_app.controllers.health_check import HealthCheck
from BR_app.controllers.performance import Performance
from BR_app.controllers.returns import Returns
from BR_app.controllers.transaction import Transaction
from BR_app.controllers.validate_service import Validation


app_router = APIRouter()

app_router.add_api_route("/health/check",HealthCheck().health_check,methods=["GET"],dependencies=[])
app_router.add_api_route("/performance",Performance().performance,methods=["GET"],dependencies=[])
app_router.add_api_route("/returns:nps",Returns().calculate_nps,methods=["POST"],dependencies=[])
app_router.add_api_route("/transactions:parse",Transaction().parse_transactions,methods=["POST"],dependencies=[])
app_router.add_api_route("/transactions:validator",Validation().validate_transactions,methods=["POST"],dependencies=[])
