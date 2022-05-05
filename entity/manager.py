

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

    @classmethod
    def clear(cls):
        for entity in cls.ENTITIES_TABLE.items():
            del entity
        cls.ENTITIES_TABLE.clear()
        cls.ID = 0


    @classmethod
    def find_instance(cls,instance_class):
        instances = cls.ENTITIES_TABLE.values()
        return list(filter(lambda i:isinstance(i,instance_class),instances))


