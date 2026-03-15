import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, List
from config import DB_NAME, SESSION_FILE
from models import (
    Siswa, Mapel, Ekskul, TujuanPembelajaran,
    LingkupMateri, NilaiFormatif, NilaiSumatif,
    NilaiEkskul, Mutasi, Sekolah
)


class Database:
    def __init__(self):
        self.db_name = DB_NAME
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabel Sekolah
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sekolah (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_sekolah TEXT,
                npsn TEXT,
                nss TEXT,
                alamat TEXT,
                kode_pos TEXT,
                desa_kelurahan TEXT,
                kecamatan TEXT,
                kabupaten_kota TEXT,
                provinsi TEXT,
                website TEXT,
                email TEXT,
                nama_kepala_sekolah TEXT,
                nip_kepala_sekolah TEXT,
                nama_wali_kelas TEXT,
                nip_wali_kelas TEXT,
                kelas TEXT,
                fase TEXT,
                semester TEXT,
                tahun_ajaran TEXT,
                tempat_tanggal_rapor TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabel Siswa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS siswa (
                uuid TEXT PRIMARY KEY,
                nis TEXT UNIQUE,
                nisn TEXT UNIQUE,
                nama_lengkap TEXT,
                jenis_kelamin TEXT,
                tempat_lahir TEXT,
                tanggal_lahir TEXT,
                agama TEXT,
                pendidikan_sebelumnya TEXT,
                alamat_siswa TEXT,
                nama_ayah TEXT,
                nama_ibu TEXT,
                pekerjaan_ayah TEXT,
                pekerjaan_ibu TEXT,
                alamat_ortu_jalan TEXT,
                alamat_ortu_kelurahan TEXT,
                alamat_ortu_kecamatan TEXT,
                alamat_ortu_kabupaten TEXT,
                alamat_ortu_provinsi TEXT,
                nama_wali TEXT,
                pekerjaan_wali TEXT,
                alamat_wali TEXT,
                no_telepon TEXT,
                status TEXT DEFAULT 'Aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabel Mata Pelajaran
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mapel (
                id_mapel TEXT PRIMARY KEY,
                nama_mapel TEXT
            )
        ''')

        # Tabel Ekstrakurikuler
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ekskul (
                id_ekskul TEXT PRIMARY KEY,
                nama_ekskul TEXT
            )
        ''')

        # Tabel Tujuan Pembelajaran
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tujuan_pembelajaran (
                id_tp TEXT PRIMARY KEY,
                id_mapel TEXT,
                tujuan_pembelajaran TEXT,
                FOREIGN KEY (id_mapel) REFERENCES mapel(id_mapel)
            )
        ''')

        # Tabel Lingkup Materi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lingkup_materi (
                id_lm TEXT PRIMARY KEY,
                id_mapel TEXT,
                lingkup_materi TEXT,
                FOREIGN KEY (id_mapel) REFERENCES mapel(id_mapel)
            )
        ''')

        # Tabel Asesmen Formatif
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asesmen_formatif (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid_siswa TEXT,
                id_mapel TEXT,
                id_tp TEXT,
                kktp TEXT,
                tampil_di_rapor TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uuid_siswa) REFERENCES siswa(uuid),
                FOREIGN KEY (id_mapel) REFERENCES mapel(id_mapel),
                FOREIGN KEY (id_tp) REFERENCES tujuan_pembelajaran(id_tp)
            )
        ''')

        # Tabel Asesmen Sumatif
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asesmen_sumatif (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid_siswa TEXT,
                id_mapel TEXT,
                jenis_sumatif TEXT,
                id_lm TEXT,
                nilai REAL,
                semester TEXT,
                tahun_ajaran TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uuid_siswa) REFERENCES siswa(uuid),
                FOREIGN KEY (id_mapel) REFERENCES mapel(id_mapel),
                FOREIGN KEY (id_lm) REFERENCES lingkup_materi(id_lm)
            )
        ''')

        # Tabel Nilai Ekstrakurikuler
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nilai_ekskul (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid_siswa TEXT,
                id_ekskul TEXT,
                nilai TEXT,
                deskripsi TEXT,
                semester TEXT,
                tahun_ajaran TEXT,
                FOREIGN KEY (uuid_siswa) REFERENCES siswa(uuid),
                FOREIGN KEY (id_ekskul) REFERENCES ekskul(id_ekskul)
            )
        ''')

        # Tabel Kehadiran
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kehadiran (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid_siswa TEXT,
                sakit INTEGER DEFAULT 0,
                ijin INTEGER DEFAULT 0,
                tanpa_keterangan INTEGER DEFAULT 0,
                semester TEXT,
                tahun_ajaran TEXT,
                FOREIGN KEY (uuid_siswa) REFERENCES siswa(uuid)
            )
        ''')

        # Tabel Mutasi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mutasi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jenis_mutasi TEXT,
                uuid_siswa TEXT,
                kelas_ditinggalkan TEXT,
                alasan TEXT,
                tanggal_mutasi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uuid_siswa) REFERENCES siswa(uuid)
            )
        ''')

        conn.commit()
        conn.close()

    # Session Management
    def save_session(self, user_data):
        with open(SESSION_FILE, 'w') as f:
            json.dump({
                'token': user_data.get('token'),
                'email': user_data.get('email'),
                'nama_lengkap': user_data.get('nama_lengkap'),
                'account_type': user_data.get('account_type', 'Free'),
                'login_at': datetime.now().isoformat()
            }, f)

    def load_session(self):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        return None

    def clear_session(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    # CRUD Operations untuk Sekolah
    def save_sekolah(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM sekolah')
        cursor.execute('''
            INSERT INTO sekolah VALUES (
                NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
            )
        ''', (
            data['nama_sekolah'], data['npsn'], data['nss'], data['alamat'],
            data['kode_pos'], data['desa_kelurahan'], data['kecamatan'],
            data['kabupaten_kota'], data['provinsi'], data['website'],
            data['email'], data['nama_kepala_sekolah'], data['nip_kepala_sekolah'],
            data['nama_wali_kelas'], data['nip_wali_kelas'], data['kelas'],
            data['fase'], data['semester'], data['tahun_ajaran'],
            data['tempat_tanggal_rapor']
        ))

        conn.commit()
        conn.close()

    def get_sekolah(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sekolah ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'nama_sekolah': row[1], 'npsn': row[2], 'nss': row[3],
                'alamat': row[4], 'kode_pos': row[5], 'desa_kelurahan': row[6],
                'kecamatan': row[7], 'kabupaten_kota': row[8], 'provinsi': row[9],
                'website': row[10], 'email': row[11], 'nama_kepala_sekolah': row[12],
                'nip_kepala_sekolah': row[13], 'nama_wali_kelas': row[14],
                'nip_wali_kelas': row[15], 'kelas': row[16], 'fase': row[17],
                'semester': row[18], 'tahun_ajaran': row[19],
                'tempat_tanggal_rapor': row[20]
            }
        return None

    # CRUD Siswa
    def save_siswa(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO siswa VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Aktif', CURRENT_TIMESTAMP
            )
        ''', (
            data['uuid'], data['nis'], data['nisn'], data['nama_lengkap'],
            data['jenis_kelamin'], data['tempat_lahir'], data['tanggal_lahir'],
            data['agama'], data['pendidikan_sebelumnya'], data['alamat_siswa'],
            data['nama_ayah'], data['nama_ibu'], data['pekerjaan_ayah'],
            data['pekerjaan_ibu'], data['alamat_ortu_jalan'],
            data['alamat_ortu_kelurahan'], data['alamat_ortu_kecamatan'],
            data['alamat_ortu_kabupaten'], data['alamat_ortu_provinsi'],
            data['nama_wali'], data['pekerjaan_wali'], data['alamat_wali'],
            data['no_telepon']
        ))
        conn.commit()
        conn.close()

    def get_all_siswa(self, status='Aktif'):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM siswa WHERE status = ? ORDER BY nama_lengkap', (status,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict_siswa(row) for row in rows]

    def get_siswa_by_uuid(self, uuid):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM siswa WHERE uuid = ?', (uuid,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_dict_siswa(row) if row else None

    def _row_to_dict_siswa(self, row):
        return {
            'uuid': row[0], 'nis': row[1], 'nisn': row[2], 'nama_lengkap': row[3],
            'jenis_kelamin': row[4], 'tempat_lahir': row[5], 'tanggal_lahir': row[6],
            'agama': row[7], 'pendidikan_sebelumnya': row[8], 'alamat_siswa': row[9],
            'nama_ayah': row[10], 'nama_ibu': row[11], 'pekerjaan_ayah': row[12],
            'pekerjaan_ibu': row[13], 'alamat_ortu_jalan': row[14],
            'alamat_ortu_kelurahan': row[15], 'alamat_ortu_kecamatan': row[16],
            'alamat_ortu_kabupaten': row[17], 'alamat_ortu_provinsi': row[18],
            'nama_wali': row[19], 'pekerjaan_wali': row[20], 'alamat_wali': row[21],
            'no_telepon': row[22], 'status': row[23]
        }

    def import_siswa_csv(self, dataframe):
        import uuid
        conn = self.get_connection()
        cursor = conn.cursor()

        for _, row in dataframe.iterrows():
            siswa_uuid = str(uuid.uuid4())
            cursor.execute('''
                INSERT OR REPLACE INTO siswa VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Aktif', CURRENT_TIMESTAMP)
            ''', (
                siswa_uuid, str(row.get('NIS', '')), str(row.get('NISN', '')),
                row.get('NAMA PESERTA DIDIK', ''), row.get('L/P', ''),
                row.get('TEMPAT LAHIR', ''), row.get('TANGGAL LAHIR', ''),
                row.get('AGAMA', ''), row.get('PENDIDIKAN SEBELUMNYA', ''),
                row.get('ALAMAT PESERTA DIDIK', ''),
                row.get('NAMA AYAH', ''), row.get('NAMA IBU', ''),
                row.get('PEKERJAAN AYAH', ''), row.get('PEKERJAAN IBU', ''),
                row.get('JALAN', ''), row.get('KELURAHAN/DESA', ''),
                row.get('KECAMATAN', ''), row.get('KAB./KOTA', ''),
                row.get('PROPINSI', ''), row.get('NAMA WALI', ''),
                row.get('PEKERJAAN WALI', ''), row.get('ALAMAT WALI', ''),
                row.get('NOMOR TELEPHON', '')
            ))

        conn.commit()
        conn.close()

    # Mapel
    def save_mapel(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO mapel VALUES (?, ?)',
                       (data['id_mapel'], data['nama_mapel']))
        conn.commit()
        conn.close()

    def get_all_mapel(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mapel ORDER BY id_mapel')
        rows = cursor.fetchall()
        conn.close()
        return [{'id_mapel': r[0], 'nama_mapel': r[1]} for r in rows]

    def generate_mapel_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM mapel')
        count = cursor.fetchone()[0]
        conn.close()
        return f"MP{str(count + 1).zfill(3)}"

    # Ekskul
    def save_ekskul(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO ekskul VALUES (?, ?)',
                       (data['id_ekskul'], data['nama_ekskul']))
        conn.commit()
        conn.close()

    def get_all_ekskul(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ekskul ORDER BY id_ekskul')
        rows = cursor.fetchall()
        conn.close()
        return [{'id_ekskul': r[0], 'nama_ekskul': r[1]} for r in rows]

    def generate_ekskul_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM ekskul')
        count = cursor.fetchone()[0]
        conn.close()
        return f"EKS{str(count + 1).zfill(3)}"

    # Tujuan Pembelajaran
    def save_tp(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO tujuan_pembelajaran VALUES (?, ?, ?)',
                       (data['id_tp'], data['id_mapel'], data['tujuan_pembelajaran']))
        conn.commit()
        conn.close()

    def get_tp_by_mapel(self, id_mapel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tujuan_pembelajaran WHERE id_mapel = ?', (id_mapel,))
        rows = cursor.fetchall()
        conn.close()
        return [{'id_tp': r[0], 'id_mapel': r[1], 'tujuan_pembelajaran': r[2]} for r in rows]

    def generate_tp_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM tujuan_pembelajaran')
        count = cursor.fetchone()[0]
        conn.close()
        return f"TP{str(count + 1).zfill(3)}"

    # Lingkup Materi
    def save_lm(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO lingkup_materi VALUES (?, ?, ?)',
                       (data['id_lm'], data['id_mapel'], data['lingkup_materi']))
        conn.commit()
        conn.close()

    def get_lm_by_mapel(self, id_mapel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lingkup_materi WHERE id_mapel = ?', (id_mapel,))
        rows = cursor.fetchall()
        conn.close()
        return [{'id_lm': r[0], 'id_mapel': r[1], 'lingkup_materi': r[2]} for r in rows]

    def generate_lm_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM lingkup_materi')
        count = cursor.fetchone()[0]
        conn.close()
        return f"LM{str(count + 1).zfill(3)}"

    # Asesmen Formatif
    def save_formatif(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO asesmen_formatif (uuid_siswa, id_mapel, id_tp, kktp, tampil_di_rapor)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['uuid_siswa'], data['id_mapel'], data['id_tp'],
              data['kktp'], data['tampil_di_rapor']))
        conn.commit()
        conn.close()

    def get_formatif_by_siswa_mapel(self, uuid_siswa, id_mapel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT af.*, tp.tujuan_pembelajaran 
            FROM asesmen_formatif af
            JOIN tujuan_pembelajaran tp ON af.id_tp = tp.id_tp
            WHERE af.uuid_siswa = ? AND af.id_mapel = ?
        ''', (uuid_siswa, id_mapel))
        rows = cursor.fetchall()
        conn.close()
        return [{
            'id': r[0], 'uuid_siswa': r[1], 'id_mapel': r[2], 'id_tp': r[3],
            'kktp': r[4], 'tampil_di_rapor': r[5], 'tujuan_pembelajaran': r[7]
        } for r in rows]

    # Asesmen Sumatif
    def save_sumatif(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO asesmen_sumatif (uuid_siswa, id_mapel, jenis_sumatif, id_lm, nilai, semester, tahun_ajaran)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['uuid_siswa'], data['id_mapel'], data['jenis_sumatif'],
              data.get('id_lm'), data['nilai'], data.get('semester'), data.get('tahun_ajaran')))
        conn.commit()
        conn.close()

    def get_sumatif_by_siswa_mapel(self, uuid_siswa, id_mapel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM asesmen_sumatif 
            WHERE uuid_siswa = ? AND id_mapel = ?
        ''', (uuid_siswa, id_mapel))
        rows = cursor.fetchall()
        conn.close()
        return [{
            'id': r[0], 'uuid_siswa': r[1], 'id_mapel': r[2], 'jenis_sumatif': r[3],
            'id_lm': r[4], 'nilai': r[5], 'semester': r[6], 'tahun_ajaran': r[7]
        } for r in rows]

    # Nilai Ekskul
    def save_nilai_ekskul(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO nilai_ekskul (uuid_siswa, id_ekskul, nilai, deskripsi, semester, tahun_ajaran)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['uuid_siswa'], data['id_ekskul'], data['nilai'],
              data['deskripsi'], data.get('semester'), data.get('tahun_ajaran')))
        conn.commit()
        conn.close()

    def get_nilai_ekskul_by_siswa(self, uuid_siswa):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ne.*, e.nama_ekskul 
            FROM nilai_ekskul ne
            JOIN ekskul e ON ne.id_ekskul = e.id_ekskul
            WHERE ne.uuid_siswa = ?
        ''', (uuid_siswa,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            'id': r[0], 'uuid_siswa': r[1], 'id_ekskul': r[2], 'nilai': r[3],
            'deskripsi': r[4], 'nama_ekskul': r[7]
        } for r in rows]

    # Mutasi
    def save_mutasi(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mutasi (jenis_mutasi, uuid_siswa, kelas_ditinggalkan, alasan)
            VALUES (?, ?, ?, ?)
        ''', (data['jenis_mutasi'], data['uuid_siswa'],
              data.get('kelas_ditinggalkan'), data.get('alasan')))

        if data['jenis_mutasi'] == 'KELUAR':
            cursor.execute('UPDATE siswa SET status = ? WHERE uuid = ?',
                           ('Keluar', data['uuid_siswa']))

        conn.commit()
        conn.close()

    def get_mutasi_keluar(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, s.nama_lengkap, s.nis, s.nisn
            FROM mutasi m
            JOIN siswa s ON m.uuid_siswa = s.uuid
            WHERE m.jenis_mutasi = 'KELUAR'
            ORDER BY m.tanggal_mutasi DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [{
            'id': r[0], 'jenis_mutasi': r[1], 'uuid_siswa': r[2],
            'kelas_ditinggalkan': r[3], 'alasan': r[4], 'tanggal_mutasi': r[5],
            'nama_lengkap': r[6], 'nis': r[7], 'nisn': r[8]
        } for r in rows]

    def get_siswa_model(self, uuid: str) -> "Optional[Siswa]":
        """Get Siswa as model"""
        row = self.get_siswa_by_uuid(uuid)
        if row:
            return Siswa(**row)
        return None

    def get_all_siswa_models(self) -> "List[Siswa]":
        """Get all Siswa as models"""
        rows = self.get_all_siswa()
        return [Siswa(**row) for row in rows]

    def save_siswa_model(self, siswa: "Siswa"):
        """Save Siswa model"""
        self.save_siswa(siswa.to_dict())

    def get_sekolah_model(self) -> "Optional[Sekolah]":
        """Get Sekolah as model"""
        row = self.get_sekolah()
        if row:
            return Sekolah(**row)
        return None

    def save_sekolah_model(self, sekolah: "Sekolah"):
        """Save Sekolah model"""
        self.save_sekolah(sekolah.to_dict())


db = Database()
