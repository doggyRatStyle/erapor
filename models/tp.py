from dataclasses import dataclass, asdict


@dataclass
class TujuanPembelajaran:
    id_tp: str
    id_mapel: str
    tujuan_pembelajaran: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def generate_id(cls, count: int):
        """Generate ID like TP001"""
        return f"TP{str(count + 1).zfill(3)}"

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(id_tp=row[0], id_mapel=row[1], tujuan_pembelajaran=row[2])