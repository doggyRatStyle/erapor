from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
from config import MUTASI_MASUK, MUTASI_KELUAR


@dataclass
class Mutasi:
    id: Optional[int] = None
    jenis_mutasi: str = ""  # MASUK atau KELUAR
    uuid_siswa: str = ""
    kelas_ditinggalkan: Optional[str] = None  # Untuk keluar
    alasan: Optional[str] = None
    tanggal_mutasi: Optional[str] = None

    def __post_init__(self):
        if self.tanggal_mutasi is None:
            self.tanggal_mutasi = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)

    def is_masuk(self):
        return self.jenis_mutasi == MUTASI_MASUK

    def is_keluar(self):
        return self.jenis_mutasi == MUTASI_KELUAR

    def get_output_text(self, nama_siswa: str, kelas: str):
        """Generate output text for surat mutasi"""
        if self.is_keluar():
            return f"{nama_siswa} keluar dari kelas {kelas} dengan alasan: {self.alasan}"
        return f"{nama_siswa} masuk ke kelas {kelas}"

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            id=row[0],
            jenis_mutasi=row[1],
            uuid_siswa=row[2],
            kelas_ditinggalkan=row[3],
            alasan=row[4],
            tanggal_mutasi=row[5]
        )