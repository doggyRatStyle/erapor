# Models package initialization
from .user import User
from .sekolah import Sekolah
from .siswa import Siswa
from .mapel import Mapel
from .ekskul import Ekskul
from .tp import TujuanPembelajaran
from .lm import LingkupMateri
from .nilai import NilaiFormatif, NilaiSumatif, NilaiEkskul
from .mutasi import Mutasi

__all__ = [
    'User',
    'Sekolah',
    'Siswa',
    'Mapel',
    'Ekskul',
    'TujuanPembelajaran',
    'LingkupMateri',
    'NilaiFormatif',
    'NilaiSumatif',
    'NilaiEkskul',
    'Mutasi'
]