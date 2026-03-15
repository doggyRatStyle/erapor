from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Sekolah:
    nama_sekolah: str = ""
    npsn: str = ""
    nss: str = ""
    alamat: str = ""
    kode_pos: str = ""
    desa_kelurahan: str = ""
    kecamatan: str = ""
    kabupaten_kota: str = ""
    provinsi: str = ""
    website: str = ""
    email: str = ""
    nama_kepala_sekolah: str = ""
    nip_kepala_sekolah: str = ""
    nama_wali_kelas: str = ""
    nip_wali_kelas: str = ""
    kelas: str = ""
    fase: str = ""
    semester: str = ""
    tahun_ajaran: str = ""
    tempat_tanggal_rapor: str = ""

    def to_dict(self):
        return asdict(self)

    def get_alamat_lengkap(self):
        return f"{self.alamat}, {self.desa_kelurahan}, {self.kecamatan}, {self.kabupaten_kota}, {self.provinsi} {self.kode_pos}"

    @classmethod
    def from_db_row(cls, row: dict):
        """Create from database row"""
        return cls(**row)

    def validate(self):
        """Validate required fields"""
        errors = []
        if not self.nama_sekolah:
            errors.append("Nama sekolah wajib diisi")
        if not self.npsn:
            errors.append("NPSN wajib diisi")
        return errors