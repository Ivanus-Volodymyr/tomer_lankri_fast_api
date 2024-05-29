from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth import create_access_token
from app.core.settings import logger
from app.exc.exc import InvalidCredentialsForLoginException, UserAlreadyExistsException, PostNotFound
from app.models import models
from app.schemas import schemas
from app.cache import  cache_user_posts, get_cached_user_posts


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> bool:
        result = await self.db.execute(
            select(models.User).filter(models.User.email == email)
        )
        return result.scalar()

    async def sign_up_user(self, user: schemas.UserCreate) -> schemas.JWTTokenDTO:
        if await self.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return schemas.JWTTokenDTO(access_token=create_access_token(data=user))

    async def login_user(self, user: schemas.UserLogin) -> schemas.JWTTokenDTO:
        db_user = await self.get_user_by_email(user.email)
        if not db_user or not pwd_context.verify(
            user.password, db_user.hashed_password
        ):
            raise InvalidCredentialsForLoginException()
        return schemas.JWTTokenDTO(access_token=create_access_token(data=user))

    async def create_post(self, post: schemas.PostCreate, user_id: UUID) -> UUID:
        db_post = models.Post(**post.dict(), owner_id=user_id)
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post.id

    async def get_posts(self, user_id: UUID) -> schemas.PostsDTO:
        cached_posts = get_cached_user_posts(user_id)
        if cached_posts:
            logger.info("Fetching posts from cache.")
            return schemas.PostsDTO(posts=cached_posts)
        logger.info(f"Cache is empty for user {user_id}. Fetching posts from db.")
        result = await self.db.execute(select(models.Post).filter(models.Post.owner_id == str(user_id)))
        posts = result.scalars().all()
        cache_user_posts(user_id, posts)
        return schemas.PostsDTO(posts=posts)

    async def delete_post(self, post_id: str, user_id: str) -> schemas.Post:
        result = await self.db.execute(select(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == str(user_id)))
        db_post = result.scalar()
        if not db_post:
            raise PostNotFound()
        await self.db.delete(db_post)
        await self.db.commit()
        return schemas.Post(**db_post.__dict__)