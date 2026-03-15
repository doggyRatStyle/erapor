from dataclasses import dataclass, asdict
from typing import Optional
import uuid as uuid_lib


@dataclass
class Siswa:
    uuid: str
    nis: str
    nisn: str
    nama_lengkap: str
    jenis_kelamin: str = "L"  # L atau P
    tempat_lahir: str = ""
    tanggal_lahir: str = ""
    agama: str = ""
    pendidikan_sebelumnya: str = ""
    alamat_siswa: str = ""
    nama_ayah: str = ""
    nama_ibu: str = ""
    pekerjaan_ayah: str = ""
    pekerjaan_ibu: str = ""
    alamat_ortu_jalan: str = ""
    alamat_ortu_kelurahan: str = ""
    alamat_ortu_kecamatan: str = ""
    alamat_ortu_kabupaten: str = ""
    alamat_ortu_provinsi: str = ""
    nama_wali: str = ""
    pekerjaan_wali: str = ""
    alamat_wali: str = ""
    no_telepon: str = ""
    status: str = "Aktif"  # Aktif, Keluar, Lulus

    def __post_init__(self):
        if not self.uuid:
            self.uuid = str(uuid_lib.uuid4())

    def to_dict(self):
        return asdict(self)

    def get_nama_ortu(self):
        return f"{self.nama_ayah} / {self.nama_ibu}"

    def get_alamat_ortu_lengkap(self):
        parts = [
            self.alamat_ortu_jalan,
            self.alamat_ortu_kelurahan,
            self.alamat_ortu_kecamatan,
            self.alamat_ortu_kabupaten,
            self.alamat_ortu_provinsi
        ]
        return ", ".join([p for p in parts if p])

    def get_jenis_kelamin_display(self):
        return "Laki-laki" if self.jenis_kelamin == "L" else "Perempuan"

    @classmethod
    def from_csv_row(cls, row: dict):
        """Create from CSV import"""
        return cls(
            uuid=str(uuid_lib.uuid4()),
            nis=str(row.get('NIS', '')),
            nisn=str(row.get('NISN', '')),
            nama_lengkap=row.get('NAMA PESERTA DIDIK', ''),
            jenis_kelamin=row.get('L/P', 'L'),
            tempat_lahir=row.get('TEMPAT LAHIR', ''),
            tanggal_lahir=row.get('TANGGAL LAHIR', ''),
            agama=row.get('AGAMA', ''),
            pendidikan_sebelumnya=row.get('PENDIDIKAN SEBELUMNYA', ''),
            alamat_siswa=row.get('ALAMAT PESERTA DIDIK', ''),
            nama_ayah=row.get('NAMA AYAH', ''),
            nama_ibu=row.get('NAMA IBU', ''),
            pekerjaan_ayah=row.get('PEKERJAAN AYAH', ''),
            pekerjaan_ibu=row.get('PEKERJAAN IBU', ''),
            alamat_ortu_jalan=row.get('JALAN', ''),
            alamat_ortu_kelurahan=row.get('KELURAHAN/DESA', ''),
            alamat_ortu_kecamatan=row.get('KECAMATAN', ''),
            alamat_ortu_kabupaten=row.get('KAB./KOTA', ''),
            alamat_ortu_provinsi=row.get('PROPINSI', ''),
            nama_wali=row.get('NAMA WALI', ''),
            pekerjaan_wali=row.get('PEKERJAAN WALI', ''),
            alamat_wali=row.get('ALAMAT WALI', ''),
            no_telepon=row.get('NOMOR TELEPHON', '')
        )

    @classmethod
    def from_db_row(cls, row: tuple):
        """Create from database tuple"""
        return cls(
            uuid=row[0],
            nis=row[1],
            nisn=row[2],
            nama_lengkap=row[3],
            jenis_kelamin=row[4],
            tempat_lahir=row[5],
            tanggal_lahir=row[6],
            agama=row[7],
            pendidikan_sebelumnya=row[8],
            alamat_siswa=row[9],
            nama_ayah=row[10],
            nama_ibu=row[11],
            pekerjaan_ayah=row[12],
            pekerjaan_ibu=row[13],
            alamat_ortu_jalan=row[14],
            alamat_ortu_kelurahan=row[15],
            alamat_ortu_kecamatan=row[16],
            alamat_ortu_kabupaten=row[17],
            alamat_ortu_provinsi=row[18],
            nama_wali=row[19],
            pekerjaan_wali=row[20],
            alamat_wali=row[21],
            no_telepon=row[22],
            status=row[23] if len(row) > 23 else "Aktif"
        )