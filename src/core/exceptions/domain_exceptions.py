from .base_exception import BaseAppException

class EntityNotFoundException(BaseAppException):
    pass

class VectorStoreOperationException(BaseAppException):
    pass

class InferenceException(BaseAppException):
    pass

class ValidationException(BaseAppException):
    pass