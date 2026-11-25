# Template agent review bug bounty

Agent utama adalah **ORCHESTRATOR**. Ia membagi review antara **RESEARCHER**, **BUILDER**, dan **AUDITOR**, lalu mengembalikan hasil ke pengguna. Pakai runtime yang mendukung delegasi subagent. Template Markdown ini tidak bergantung pada program, platform, atau model tertentu.

## Pakai di agent lain

1. Salin [AGENTS.md](AGENTS.md) ke workspace privat. Jika agent tidak otomatis membaca file itu, tempel seluruh isinya sebagai instruksi sesi.
2. Berikan satu kandidat, kutipan kebijakan resmi, versi aset, bukti yang sudah disamarkan, dan tiket pembanding yang boleh dibaca. Isi konteks program saat memakai template, bukan di repo template.
3. Minta: **“Review kandidat ini dengan AGENTS.md. Kembalikan kartu keputusan dan sebutkan sumber yang belum bisa diperiksa.”** Simpan hasil di workspace privat.

**Cek pemasangan:** berikan kandidat kosong tanpa kebijakan, bukti, dan riwayat tiket. Hasil yang diharapkan: `HOLD`, tiga penilaian `UNKNOWN`, dan daftar bahan yang kurang. Agent tidak boleh mengarang program atau memulai pengujian.
