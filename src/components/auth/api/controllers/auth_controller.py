from fastapi.exceptions import HTTPException, FastAPIError
from fastapi.routing import APIRouter

from typing import List, Optional

from utils import SessionManager
from schemas import TokenInput, TokenOutput
from services import AuthService
from utils import Logger

_logger = Logger(logger_name=__name__)._get_logger()

auth_router = APIRouter(prefix="/api/v1/token", tags=["Auth"])


@auth_router.post("/create", response_model=TokenOutput)
async def create_token(data: TokenInput) -> TokenOutput:
    try:
        _auth_service = AuthService(SessionManager())
        return _auth_service.create_token(data)
    except FastAPIError as e:
        _logger.error("Error on token creation: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@auth_router.get("/{token_id}", response_model=Optional[TokenOutput])
async def get_token_by_id(token_id: int) -> Optional[TokenOutput]:
    try:
        _auth_service = AuthService(SessionManager())
        return _auth_service.get_token_by_id(token_id)
    except FastAPIError as e:
        _logger.error("Erron on token retrieval: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@auth_router.get("/all/{user_id}", response_model=List[Optional[TokenOutput]])
async def get_all_tokens_by_user_id(user_id: int) -> List[Optional[TokenOutput]]:
    try:

        _auth_service = AuthService(SessionManager())
        return _auth_service.get_all_tokens_by_user_id(user_id)
    except FastAPIError as e:
        _logger.error(
            "Error on retrieving tokens for user: %s | Error: %s", 
            user_id,
            str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@auth_router.put("/revoke")
async def revoke_token(token_id: int) -> bool:
    try:
        _auth_service = AuthService(SessionManager())
        return _auth_service.revoke_token(token_id)
    except FastAPIError as e:
        _logger.error("Error on token revocation: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@auth_router.delete("/{token_id}")
async def delete_token_by_id(token_id: int) -> None:
    try:
        _auth_service = AuthService(SessionManager())
        return _auth_service.delete_token_by_id(token_id)
    except FastAPIError as e:
        _logger.error("Error on token deletion: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@auth_router.delete("/all/{user_id}")
async def delete_all_tokens_by_user_id(user_id: int) -> None:
    try:
        _auth_service = AuthService(SessionManager())
        return _auth_service.delete_all_tokens_by_user_id(user_id)
    except FastAPIError as e:
        _logger.error("Error on deleting tokens for user: %s | Error: %s", user_id, str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
