# Bounty setup

Mulai dari [workflow review laporan](WORKFLOW.md) dan [kartu keputusan Auditor](agents/AUDITOR.md). Jalur ini dipakai untuk draf yang sudah ada; tidak perlu API key, browser login, atau akses ke target. Direktori `data/xe/` berisi snapshot historis, bukan daftar lengkap tiket terkini. Driver, connector, dan skill hunting lama tetap tersedia sebagai arsip; bukan bagian dari jalur review.

## Migrasi dari setup lama

- Nonaktifkan job `xe-bounty-hunter-0800` dan `xe-bounty-hunter-2000` di scheduler yang sudah terpasang. Mengubah file Git tidak mengubah salinan job di server.
- Ganti salinan `agents/AUDITOR.md`, `agents/ORCHESTRATOR.md`, dan `skills-local/local-bounty-reporting/`. Pertahankan path relatifnya atau berikan isi prosedur Auditor langsung ke reviewer. Jangan gabungkan prompt baru dengan prompt filing lama.
- Uji dengan satu draf lama yang sudah ditutup. Sembunyikan verdict lama, isi kartu, lalu bandingkan dengan alasan triager. Jangan submit ulang. Dua watcher direktori program tidak diubah.
