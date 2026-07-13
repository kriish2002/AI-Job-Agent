from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def fetch_jobs(self):
        pass