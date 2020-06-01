from dataclasses import dataclass

@dataclass
class School:
    district: int
    district_name: str
    school: int
    school_name: str
    year: int
    website: str
    has_sro: int = None