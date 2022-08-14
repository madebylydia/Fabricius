from abc import ABC, abstractmethod

from fabricius.template import Template


class IntegrityCheckerContract(ABC):
    @abstractmethod
    def check(self, template: Template):
        pass
