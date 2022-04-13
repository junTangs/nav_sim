

class EntityManager:
    ID = 0
    ENTITIES_TABLE = {}

    @classmethod
    def register(cls,entity):
        entity.id = cls.ID
        cls.ENTITIES_TABLE[entity.id] = entity
        cls.ID += 1
        
    @classmethod
    def get(cls,id):
        return cls.ENTITIES_TABLE[id]