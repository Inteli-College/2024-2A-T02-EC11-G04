from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException, FastAPIError

from utils import SessionManager
from schemas import TokenInput, TokenOutput
from services import AuthService
from utils import Logger

_logger = Logger(logger_name=__name__)._get_logger()


auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@auth_router.post("/create-token", response_model=TokenOutput)
async def create_token(data: TokenInput) -> TokenOutput:
    _logger.info("SignIn route called")
    _auth_service = AuthService(SessionManager())
    return _auth_service.create_token(data)
