from enum import Enum

class PriorityFlag(Enum):
    MUITO_IMPORTANTE = "muito-importante"
    IMPORTANTE = "importante"
    MEDIA = "média"
    SIMPLES = "simples"
    
    @classmethod
    def from_string(cls, value):
        """Converte string para PriorityFlag"""
        for flag in cls:
            if flag.value == value or flag.name == value:
                return flag
        raise ValueError(f"'{value}' is not a valid PriorityFlag")
    
    def __str__(self):
        return self.value