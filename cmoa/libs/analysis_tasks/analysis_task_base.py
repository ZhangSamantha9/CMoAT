from abc import abstractmethod, ABC

class AnalysisTaskBase(ABC):
    """
    The base class of analysis tasks
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def preprocess(self) -> None:
        """
        The preprocess function
        """
        pass

    @abstractmethod
    def process(self) -> None:
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

    def run_task(self):
        self.preprocess()
        self.process()
        return self.result

class PreprocessError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ProcessError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message