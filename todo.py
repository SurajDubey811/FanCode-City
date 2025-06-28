from dataclasses import dataclass
from typing import Dict

@dataclass
class Todo:
    """Data class to represent a todo task"""
    id: int
    user_id: int
    title: str
    completed: bool

    @classmethod
    def from_dict(cls, data: Dict) -> 'Todo':
        """Create Todo object from API response"""
        return cls(
            id=data['id'],
            user_id=data['userId'],
            title=data['title'],
            completed=data['completed']
        )
