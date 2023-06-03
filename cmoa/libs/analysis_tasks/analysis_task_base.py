from abc import abstractmethod, ABC

class AnalysisTaskBase(ABC):
    """
    The base class of analysis tasks
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def preprocess(self) -> bool:
        """
        The preprocess function
        """
        pass

    @abstractmethod
    def process(self) -> bool:
        """
        The main process function
        """
        pass

    @property
    def result(self):
        """
        The result property, use this to return the task result
        """
        pass
