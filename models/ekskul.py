from dataclasses import dataclass, asdict


@dataclass
class Ekskul:
    id_ekskul: str
    nama_ekskul: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def generate_id(cls, count: int):
        """Generate ID like EKS001"""
        return f"EKS{str(count + 1).zfill(3)}"

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(id_ekskul=row[0], nama_ekskul=row[1])