class AnalysisTaskBase(object):
    """
    The base class of analysis tasks
    """

    def __init__(self) -> None:
        pass

    def preprocess(self) -> None:
        pass

    def process(self) -> None:
        pass

    @property
    def result(self):
        pass
