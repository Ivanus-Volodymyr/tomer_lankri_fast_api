from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.auth import get_current_user
from app.core.settings import logger
from app.exc.exc import PostToLargeException, PostNotFound
from app.schemas import schemas
from app.db.database import get_db
from app.schemas.schemas import PostCreatedDTO
from app.services import crud
from app.utils.checks import check_size_of_a_post

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post("/add", response_model=PostCreatedDTO, status_code=status.HTTP_201_CREATED)
async def add_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
) -> PostCreatedDTO:
    try:
        logger.info(f"Adding post for user: {current_user.email}")
        check_size_of_a_post(post)
        _crud = crud.CRUD(db)
        result = await _crud.create_post(post=post, user_id=current_user.id)
        logger.info(f"Post added successfully with ID: {result}")
        return PostCreatedDTO(id=result)
    except PostToLargeException as e:
        logger.error(f"Post is too large: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=schemas.PostsDTO)
async def get_posts(
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    try:
        logger.info(f"Fetching posts for user: {current_user.email}")
        _crud = crud.CRUD(db)
        posts = await _crud.get_posts(user_id=current_user.id)
        return posts
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{post_id}", response_model=schemas.Post)
async def delete_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    try:
        logger.info(f"Deleting post with ID: {post_id} for user: {current_user.email}")
        _crud = crud.CRUD(db)
        result = await _crud.delete_post(post_id=post_id, user_id=current_user.id)
        logger.info(f"Post with ID: {post_id} deleted successfully")
        return result
    except PostNotFound as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
