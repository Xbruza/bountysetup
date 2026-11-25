# Template agent review bug bounty

Pakai satu agent untuk menelaah kode yang diizinkan atau menilai draf laporan yang sudah ada. Template ini hanya berisi Markdown. Tidak perlu instalasi, akun platform, konektor, atau model tertentu.

## Pakai di agent lain

1. Salin [AGENTS.md](AGENTS.md) ke workspace privat. Jika agent tidak otomatis membaca file itu, tempel seluruh isinya sebagai instruksi sesi.
2. Berikan satu kandidat, kutipan kebijakan resmi, versi aset, bukti yang sudah disamarkan, dan tiket pembanding yang boleh dibaca. Isi konteks program saat memakai template, bukan di repo template.
3. Minta: **“Review kandidat ini dengan AGENTS.md. Kembalikan kartu keputusan dan sebutkan sumber yang belum bisa diperiksa.”** Simpan hasil di workspace privat.

**Cek pemasangan:** berikan kandidat kosong tanpa kebijakan, bukti, dan riwayat tiket. Hasil yang diharapkan: `HOLD`, tiga penilaian `UNKNOWN`, dan daftar bahan yang kurang. Agent tidak boleh mengarang program atau memulai pengujian.
