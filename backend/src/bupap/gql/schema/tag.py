import strawberry


@strawberry.type
class Tag:
    text: str
    color: str
