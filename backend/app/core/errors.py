class DomainError(Exception):
    status_code = 400

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.__name__.replace("Error", "").strip()
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail


class NotFoundError(DomainError):
    status_code = 404


class ConflictError(DomainError):
    status_code = 409


class ValidationError(DomainError):
    status_code = 400


class InsufficientStockError(ValidationError):
    pass


class CartItemAlreadyExistsError(ConflictError):
    pass


class EmptyCartError(ValidationError):
    pass


class InvalidOrderTransitionError(ValidationError):
    pass


class OrderCancellationError(ValidationError):
    pass


class UnauthorizedError(DomainError):
    status_code = 401


class ForbiddenError(DomainError):
    status_code = 403


class InternalServerError(DomainError):
    status_code = 500