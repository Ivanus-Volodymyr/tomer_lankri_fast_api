from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import logger
from app.db.database import get_db
from app.exc.exc import InvalidCredentialsForLoginException, UserAlreadyExistsException

from app.schemas import schemas

from app.services import crud

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.JWTTokenDTO)
async def signup(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
) -> schemas.JWTTokenDTO:
    try:
        logger.info(f"Creating user with email: {user.email}")
        _crud = crud.CRUD(db)
        result = await _crud.sign_up_user(user=user)
        logger.info(f"User with email: '{user.email}' created successfully")
        return result
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/login", response_model=schemas.JWTTokenDTO, status_code=status.HTTP_200_OK
)
async def login(
    _user: schemas.UserLogin,
    db: AsyncSession = Depends(get_db),
) -> schemas.JWTTokenDTO:
    try:
        logger.info(f"Try to logging in user with email: {_user.email}")
        _crud = crud.CRUD(db)
        result = await _crud.login_user(user=_user)
        logger.info(f"User with email: {_user.email} logged in  successfully")
        return result
    except InvalidCredentialsForLoginException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
