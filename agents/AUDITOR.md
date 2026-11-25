# Review draf laporan (manual)

Review satu draf dari bukti yang sudah tersedia. Jangan menghubungi target, membuat PoC, atau mengirim laporan. Kalau sumber tidak tersedia, catat yang belum diketahui. Persetujuan beberapa model atas ringkasan yang sama bukan verifikasi independen.

## Kartu keputusan (simpan privat, satu per kandidat)

- **Identitas:** ID lokal stabil, program, aset, versi/commit, tanggal review. Jangan taruh bukti privat atau data pribadi di repo ini.
- **Scope:** kutip klausul program yang berlaku dan tautannya. Cek aset, versi, jenis dampak dan pengecualian. Dalam scope aset belum berarti dampaknya diterima.
- **Validitas:** tulis aturan yang seharusnya berlaku dan sumbernya. Pisahkan hasil yang benar-benar diamati dari dugaan. Sebut lokasi bukti tersamarkan, peran yang terdampak, dan konsekuensi terukur. Kalau hasil sesuai desain, catat rujukannya. Kesalahan tampilan bukan otomatis masalah keamanan.
- **Duplikat:** bandingkan dengan riwayat sendiri (termasuk yang ditolak), known issues, dan tiket yang terlihat. Simpan tanggal, sumber, cakupan pencarian, ID pembanding, kontrol yang gagal, dan apakah perbaikan tiket lama juga memperbaiki kandidat. Beda judul, file, atau endpoint saja belum membuktikan beda bug. Satu file juga bisa punya dua bug independen.
- **Batas visibilitas:** lima hasil teratas, cache lama, akses ditolak, dan tiket privat bukan pencarian menyeluruh. Bila pencarian yang relevan belum selesai, tahan. Bila selesai tanpa kecocokan, tulis `NO_VISIBLE_MATCH`, bukan klaim unik.

## Keputusan

Catat ketiga penilaian secara terpisah: scope (`IN / OUT / UNKNOWN`), validitas (`SUPPORTED / CONTRADICTED / UNKNOWN`), dedup (`MATCH / NO_VISIBLE_MATCH / UNKNOWN`). Sertakan alasan dan sumber untuk masing-masing.

- `ARCHIVE`: scope OUT, bukti bertentangan dengan klaim, atau ada MATCH yang didukung pembanding. Simpan alasan walau ada lebih dari satu. Bila duplikat, kaitkan kandidat ke tiket induk; jangan ajukan ulang varian judul.
- `HOLD`: tidak ada alasan arsip yang pasti, tapi ada UNKNOWN. Tulis tepat bukti apa yang kurang. Jangan menutupi ketidakpastian dengan menurunkan severity.
- `DRAFT_FOR_HUMAN`: hanya IN + SUPPORTED + NO_VISIBLE_MATCH dengan rujukan yang bisa diperiksa. Ini **bukan** izin submit dan bukan jaminan diterima.

Contoh: dua layar salah menampilkan nilai karena formatter bersama yang sudah dilaporkan → MATCH bila patch formatter menyelesaikan keduanya. Dua layar mirip tanpa akses ke isi tiket pembanding → UNKNOWN, bukan MATCH dan bukan bukti unik. Hasil nyata tetapi sesuai spesifikasi → CONTRADICTED, walaupun tidak ditemukan tiket serupa.

Sesudah keputusan triager tersedia, catat tanggal, ID laporan/induk, alasan asli yang sudah disamarkan, dan kaitkan ke kartu kandidat. Jangan samakan status tiket baru dengan laporan diterima.
