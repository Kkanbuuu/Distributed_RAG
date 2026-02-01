class BaseRAGException(Exception):
    """ Base exception for RAG module """
    def __init__(
        self,
        message: str,
        error_code: str = None,       
        details: dict = None,         # Additional context
        cause: Exception = None,      # Original exception
        is_retryable: bool = False    # Can this be retried?
    ):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        self.is_retryable = is_retryable

class RetrieverException(BaseRAGException):
    """ Exception for retriever module """
    pass

class GeneratorException(BaseRAGException):
    """ Exception for generator module """
    pass

class OrchestratorException(BaseRAGException):
    """ Exception for orchestrator module """
    pass