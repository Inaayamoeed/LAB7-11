class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, size_bytes: int, 
                 rows: int, source: str):
        self.__id = dataset_id
        self.__name = name
        self.__size_bytes = size_bytes
        self.__rows = rows
        self.__source = source
    
    def get_id(self) -> int:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name
    
    def get_rows(self) -> int:
        return self.__rows
    
    def get_source(self) -> str:
        return self.__source
    
    def calculate_size_mb(self) -> float:
        """Calculate dataset size in megabytes."""
        return self.__size_bytes / (1024 * 1024)
    
    def calculate_size_gb(self) -> float:
        """Calculate dataset size in gigabytes."""
        return self.calculate_size_mb() / 1024
    
    def __str__(self) -> str:
        size_mb = self.calculate_size_mb()
        return f"Dataset {self.__id}: {self.__name} ({size_mb:.2f} MB, {self.__rows} rows)"
    
    def __repr__(self) -> str:
        return self.__str__()