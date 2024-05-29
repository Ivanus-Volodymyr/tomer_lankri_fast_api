from app.exc.exc import PostToLargeException
from app.schemas import schemas


def check_size_of_a_post(post: schemas.PostCreate) -> None:
    if len(post.text.encode('utf-8')) > 1024 * 1024:
        raise PostToLargeException()