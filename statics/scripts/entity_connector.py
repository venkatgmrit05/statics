from abc import ABC, abstractmethod


class EntityConnect(ABC):

    @abstractmethod
    def connect_entities(self, mode):
        pass

    @abstractmethod
    def update_connections(self):
        pass

    @abstractmethod
    def update_entity_forces(self):
        pass

    @abstractmethod
    def update_entity_moments(self):
        pass
