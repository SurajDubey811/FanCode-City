from dataclasses import dataclass
from typing import Dict

@dataclass
class User:
    """Data class to represent a user"""
    id: int
    name: str
    username: str
    email: str
    address: Dict
    lat: float
    lng: float

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create User object from API response"""
        return cls(
            id=data['id'],
            name=data['name'],
            username=data['username'],
            email=data['email'],
            address=data['address'],
            lat=float(data['address']['geo']['lat']),
            lng=float(data['address']['geo']['lng'])
        )
