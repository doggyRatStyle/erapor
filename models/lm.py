from dataclasses import dataclass, asdict


@dataclass
class LingkupMateri:
    id_lm: str
    id_mapel: str
    lingkup_materi: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def generate_id(cls, count: int):
        """Generate ID like LM001"""
        return f"LM{str(count + 1).zfill(3)}"

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(id_lm=row[0], id_mapel=row[1], lingkup_materi=row[2])