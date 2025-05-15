from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError

from app.api.docs.errors import unauthorized_response
from app.api.v1.dto.auth_dtos import AuthResponse, LoginInput, RefreshRequest
from app.factories.auth_factory import get_auth_use_case
from app.models.exception import NotFoundException
from app.use_cases.auth_usecase import AuthUseCase

router = APIRouter()


@router.post("/login", response_model=AuthResponse, responses=unauthorized_response)
def login(login_data: LoginInput, use_case: AuthUseCase = Depends(get_auth_use_case)):
    try:
        auth = use_case.authenticate_user(login_data.username, login_data.password)
        return AuthResponse(
            access_token=auth.access_token, refresh_token=auth.refresh_token
        )
    except NotFoundException as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/refresh", response_model=AuthResponse, responses=unauthorized_response)
def refresh_token(
    dto: RefreshRequest, use_case: AuthUseCase = Depends(get_auth_use_case)
):
    try:
        auth = use_case.refresh_token(dto.refresh_token)
        return AuthResponse(
            access_token=auth.access_token, refresh_token=auth.refresh_token
        )
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
    except NotFoundException as e:
        raise HTTPException(status_code=401, detail=e.message)
