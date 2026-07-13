from dataclasses import dataclass


@dataclass
class Job:
    title: str
    company: str
    location: str
    salary: str
    apply_url: str
    source: str
    description: str = ""
    score: int = 0