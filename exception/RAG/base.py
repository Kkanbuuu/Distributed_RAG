class BaseRAGException(Exception):
    """ Base exception for RAG module """
    pass

class RetrieverException(BaseRAGException):
    """ Exception for retriever module """
    pass

class GeneratorException(BaseRAGException):
    """ Exception for generator module """
    pass

class OrchestratorException(BaseRAGException):
    """ Exception for orchestrator module """
    pass