from abc import ABCMeta, abstractmethod


class Automaton(metaclass=ABCMeta):
    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    def set_input_sequence(self, input_sequence):
        pass

    @abstractmethod
    def start(self):
        pass

    def set_logger(self, logger):
        if logger is not None:
            self.logger = logger

    def _log(self, states):
        if states is not None and self.logger is not None:
            self.logger.log(states)
