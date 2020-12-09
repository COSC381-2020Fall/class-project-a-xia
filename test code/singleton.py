class Singleton:
    __instance = None

    def __new__(cls, name):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        
        cls.__instance.name = name
        return cls.__instance
