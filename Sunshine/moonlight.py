from Sunshine.sunshine import Sunshine

class Moonlight:
    """
    Sunshine plugin for asynchronous programming.
    """
    def __init__(self, filename: str) -> None:
        """
        Requires the path to the database-file.
        """
        self.database = Sunshine(filename)

    async def push(self, data_to_push: dict[str, any]) -> int:
        """
        (Async) Adds an object with the given fields to the database.
        Requires one argument:
            data_to_push (dictionary[string, any]) - the key-value dictionary to be added to the database.

        Returns ID.
        """
        return self.database.push(data_to_push)

    async def all(self) -> list[dict[str, any]]:
        """
        (Async) Returns all database objects.
        """
        return self.database.all()
    
    async def get(self, query: dict[str, any] = {}, count: int = 1) -> list[dict[str, any]]:
        """
        (Async) Returns a database object using a query, or returns the number of given elements in the first one up to the number specified in the `count` argument.
        Requires two arguments:
            query (dictionary[string, any]) - a key-value dictionary that will be used to select elements,
            count (integer)                 - the number of requested elements.

        You cannot use both arguments together.
        """
        return self.database.get(query = query, count = count)
    
    async def get_parameter(self, query, key) -> list[dict[str, any]]:
        """
        (Async) Returns a value from database object using a query.
        Requires two arguments:
            query (dictionary[string, any]) - a key-value dictionary that will be used to select elements,
            key   (string)                  - a key.
        """
        return self.database.get(query = query)[key]
    
    async def update(self, id: int, data_to_update: dict[str, any]) -> None:
        """
        (Async) Updates a database object with an ID.
        Requires two arguments:
            id             (14-digit integer)        - numeric identifier,
            data_to_update (dictionary[string, any]) - the key-value dictionary that will be updated in the database object.
        """
        self.database.update(id, data_to_update)

    async def contains(self, key: str, value: any) -> bool:
        """
        (Async) Checks by query, if an element is contained in the database.
        Requires two arguments:
            key   (string),
            value (any).
        These arguments will be searched in the database.

        Returns boolean.
        """
        return self.database.contains(key, value)
    
    async def delete(self, id: int) -> None:
        """
        (Async) Removes the object with the given ID from the database.
        Requires one argument:
            id (14-digit integer) - numeric identifier,
        """
        self.database.delete(id)
    
    async def drop(self) -> None:
        """
        (Async) Removes all objects from the database.
        """
        self.database.drop()

    async def backup(self, path: str) -> None:
        """
        (Async) Creates a database backup at the given path.
        Requires one argument:
            path (string) - path to the folder where the backup-file will be saved.
        """
        self.database.backup(path)