from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class NilaiFormatif:
    id: Optional[int] = None
    uuid_siswa: str = ""
    id_mapel: str = ""
    id_tp: str = ""
    kktp: str = "1"  # 1=Tercapai, 0=Tidak Tercapai
    tampil_di_rapor: str = "1"  # 1=Tampil, 0=Tidak
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)

    def is_tercapai(self):
        return self.kktp == "1"

    def is_tampil(self):
        return self.tampil_di_rapor == "1"

    def get_capaian_text(self, nama_siswa: str, tp_text: str):
        """Generate capaian kompetensi text"""
        if self.is_tercapai():
            return f"Ananda {nama_siswa} menunjukkan pemahaman dalam {tp_text}"
        else:
            return f"Ananda {nama_siswa} membutuhkan bimbingan dalam {tp_text}"


@dataclass
class NilaiSumatif:
    id: Optional[int] = None
    uuid_siswa: str = ""
    id_mapel: str = ""
    jenis_sumatif: str = ""  # Lingkup Materi, STS, SAS
    id_lm: Optional[str] = None  # Null untuk STS/SAS
    nilai: float = 0.0
    semester: str = ""
    tahun_ajaran: str = ""
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)

    def get_predikat(self):
        """Convert nilai to predikat"""
        if self.nilai >= 85:
            return "A"
        elif self.nilai >= 70:
            return "B"
        elif self.nilai >= 60:
            return "C"
        else:
            return "D"


@dataclass
class NilaiEkskul:
    id: Optional[int] = None
    uuid_siswa: str = ""
    id_ekskul: str = ""
    nilai: str = ""  # A, B, C, D atau deskriptif
    deskripsi: str = ""
    semester: str = ""
    tahun_ajaran: str = ""

    def to_dict(self):
        return asdict(self)

    def get_deskripsi_lengkap(self, nama_siswa: str, nama_ekskul: str):
        """Generate deskripsi if empty"""
        if self.deskripsi:
            return self.deskripsi
        return f"Ananda {nama_siswa} telah mengikuti kegiatan {nama_ekskul} dengan {self.get_predikat_text()}"

    def get_predikat_text(self):
        predikat_map = {
            "A": "Sangat Baik",
            "B": "Baik",
            "C": "Cukup",
            "D": "Perlu Bimbingan"
        }
        return predikat_map.get(self.nilai, "Baik")