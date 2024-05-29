class UserAlreadyExistsException(Exception):
    def __init__(self, message: str = "User with this email already exists."):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsForLoginException(Exception):
    def __init__(
        self, message: str = "Invalid credentials were provided. Can't login."
    ):
        self.message = message
        super().__init__(self.message)


class PostToLargeException(Exception):
    def __init__(self, message: str = "Post is to large."):
        self.message = message
        super().__init__(self.message)


class PostNotFound(Exception):
    def __init__(self, message: str = "Post not found."):
        self.message = message
        super().__init__(self.message)