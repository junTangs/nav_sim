

class EntityManager:
    ID = 0
    ENTITIES_TABLE = {}

    @classmethod
    def regist(cls,entity):
        entity.id = cls.ID
        cls.ENTITIES_TABLE[entity.id] = entity
        cls.ID += 1