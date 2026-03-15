from dataclasses import dataclass, asdict


@dataclass
class Mapel:
    id_mapel: str
    nama_mapel: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def generate_id(cls, count: int):
        """Generate ID like MP001"""
        return f"MP{str(count + 1).zfill(3)}"

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(id_mapel=row[0], nama_mapel=row[1])