

class EntityManager:
    ID = 0
    ENTITITS_TABLE = {}

    @classmethod
    def regist(cls,entity):
        entity.id = cls.ID
        cls.ENTITITS_TABLE[entity.id] = entity
        cls.ID += 1