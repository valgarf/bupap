import strawberry


@strawberry.type
class Tag:
    key: str | None = None
    text: str
    color: str
