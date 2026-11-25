# Bounty Reporting - tulis laporan bug bounty yang diterima

Proses end-to-end dari kandidat bug jadi laporan yang di-file: cek scope, cek duplikat, uji aman, verifikasi ulang, tulis laporan terstruktur, file. Sumber: SOP user 2026-11-18 + pelajaran dari hunt XE Bounty (A1, A2, M1-1).

Use this skill for:
- nulis laporan bug bounty (HackerOne / Bugcrowd / Intigriti / Immunefi / XE Bounty / program lain)
- ngecek kandidat bug sebelum di-file (scope, duplikat, verifikasi)
- nentuin severity + CVSS yang jujur, nggak dilebih-lebihin
- bikin PoC minimal yang bisa diulang orang asing dari nol

Don't use for: nyerang target out-of-scope, exploit lebih jauh setelah bukti cukup, nulis laporan dari hasil scanner tanpa verifikasi, atau file laporan tanpa user milih kandidatnya.

## Batas dengan skill lain (no dupe)

- `local-agentic-bug-hunter`: skill hunting (recon, attack surface, vuln class, validasi awal). Skill ini mulai SETELAH kandidat terverifikasi: nulis, dedup akhir, file, follow-up. Kalau lagi hunt, pakai bug-hunter; kalau kandidat udah di tangan dan mau jadi laporan, pakai skill ini.
- `local-bounty-roi`: skill keputusan (worth it apa nggak, stop-loss effort). Dipakai SEBELUM hunt/file, bukan buat nulis laporan.
- `local-cybersec-glossary`: kamus istilah umum + Web3 (3.379 baris, dua file di `~/workspace/user/files/kamus_hacking_cybersecurity_*.txt`). Dipakai pas nentuin NAMA kelas kerentanan + mapping CWE/CVSS/SWC/OWASP di laporan — grep istilahnya, jangan paste seluruh file. File umum buat web/network/auth, file Web3 buat kontrak/DeFi/bridge/MEV.

## Bahan yang diperlukan

Kumpulin ini sebelum hunt, simpan per program di `~/workspace/<program>/`:

- Scope + rules + disclosure policy + tabel tier (kutip bagian yang relevan, jangan cuma link).
- Repo/kode target + HEAD/commit yang diuji, docs target (API docs, formula, dsb).
- Akun test sendiri, wallet/seed throwaway, kredensial login program (via Secure Vault, jangan di file).
- Akses disclosed reports / changelog / issue tracker buat dedup.
- Template laporan (`templates/report.md`).

Struktur folder kerja:

```
~/workspace/<program>/
  scope.md            # kutipan scope, in/out, tier, disclosure policy
  leads/              # file kandidat, satu file per area
  <slug>-poc.md       # bukti PoC per kandidat yang mau di-file
  <slug>-report-draft.md  # draft laporan, diupdate ID tiket setelah file
  tickets.json        # cache hasil pencarian dedup (opsional)
```

Completion criterion: folder program ada dan `scope.md` terisi sebelum hunt dimulai.


## Pre-flight checklist (lakuin SEBELUM nulis)

1. **Baca scope & aturan program, pastiin bug in-scope.** Baca halaman scope/rules program sampai habis. Catat: aset in-scope, aset out-of-scope, vuln class yang dikecualikan, known issues, disclosure policy (boleh publikasi kapan, ke siapa). Kalau scope nggak jelas, berhenti dan tanya user. Jangan sentuh apa pun di luar scope.
2. **Cek duplikat di disclosed reports / changelog.** Cari di disclosed reports program, changelog/release notes, dan issue tracker publik dengan keyword root cause (bukan cuma judul). Duplikat dinilai dari **root cause / code path yang sama**, bukan gejala mirip. Kalau sudah ada laporan dengan root cause sama, drop kandidatnya dan catat ID-nya. Satu laporan = satu bug, kecuali chain dan rantainya dijelasin.
3. **Uji aman.** Pakai akun sendiri. Jangan sentuh data user lain. Jangan DoS, jangan destructive test, jangan akses data yang bukan milikmu. Kalau PoC butuh data orang lain, berhenti — bukti dari akun sendiri sudah cukup, atau lapor sebagai teori dengan batasan yang jelas (dan ekspektasikan ditolak).
4. **Verifikasi ulang, jangan sampai false positive.** Ulangi reproduksi dari nol, minimal 2x, di environment bersih kalau bisa. Bedain "bug beneran" vs "intended design" vs "salah paham docs". Kalau hasil reproduksi nggak konsisten, jangan file. Laporan dari hasil scanner tanpa verifikasi manual = auto-reject dan ngerusak kredibilitas.

**Exploit script buat verifikasi (standing order user 2026-11-20):** kalau kandidat/potensi bug ketemu, BOLEH bikin script exploit buat ngetes beneran ada bugnya apa nggak — bangunnya di InstaBox, dan ketiga agent boleh berunding soal itu. Batasnya tetap: verifikasi aja, akun sendiri, ikut aturan testing program (tanpa live exploit trade, tanpa pindahin dana, tanpa destructive test, tanpa data user lain).

Completion criterion: keempat poin di atas ada buktinya tertulis di file kandidat (scope dikutip, hasil pencarian duplikat dengan ID terdekat, langkah uji aman, output reproduksi 2x) sebelum laporan ditulis.

## Prosedur dedup per program

Cari dengan keyword root cause / code path / nama fungsi, bukan judul. Baca laporan terdekat sampai habis sebelum verdict. Catat query + ID terdekat + alasan beda root cause di file kandidat.

- XE Bounty: `GET https://bounty.xe.network/v1/tickets?q=<keyword>` (publik, tanpa login). Duplikat = root cause / code path sama, sesuai aturan desk.
- HackerOne: cari di disclosed reports program (filter by asset + vuln type), plus cari judul di Google `site:hackerone.com <keyword>`.
- Bugcrowd: cari di disclosed submissions program + Crowdstream.
- Immunefi: cari di disclosed reports + leaderboard program.
- Repo publik / GitHub: cari issue + PR + commit message dengan keyword fungsi/file, cek changelog/release notes versi yang diuji.
- Kalau program nggak punya disclosed reports publik, tulis itu sebagai batasan di draft ("tidak ada disclosed reports yang bisa dicek") dan andalkan changelog + repo.

## Harness PoC (target kode / node lokal)

Buat kandidat yang butuh bukti live, jangan cuma baca kode:

1. Build dari HEAD/commit yang diuji, catat command build + versi toolchain.
2. Jalanin target di loopback saja, data dir fresh, port sendiri. Akun/wallet/seed throwaway, dana testnet sendiri atau nol.
3. Jalankan langkah reproduksi persis seperti yang akan ditulis di laporan, tangkap output mentah (bukan ringkasan).
4. Bandingkan dengan kontrol: input valid vs input rusak, endpoint sibling yang benar vs yang bug.
5. Bersihin setelah selesai: stop proses, hapus data dir + seed throwaway. Jangan sisain node jalan.
6. Tulis file `<slug>-poc.md`: verdict CONFIRMED / NOT CONFIRMED / BLOCKED, command persis, output mentah, aritmatika, caveat (misal: lease dibuat via helper karena CLI hardcode live node, tapi renew pakai CLI asli).

Kalau PoC butuh sentuh live network orang lain, berhenti dan lapor sebagai temuan kode saja dengan batasan yang jelas.

## Kalibrasi severity + CVSS

Jangan tebak severity dari feeling. Pakai tabel ini, lalu hitung CVSS 3.1 (kalkulator FIRST: https://www.first.org/cvss/calculator/3.1) dan cantumin vector + skor di laporan.

| Severity | Ciri | Contoh |
|---|---|---|
| Critical | RCE / takeover tanpa interaksi korban, data sensitif massal | RCE, auth bypass total |
| High | Takeover dengan interaksi minimal, leak data akun lain | Stored XSS, IDOR ke data orang |
| Medium | Dampak nyata tapi butuh kondisi sempit / privilege | CSRF dengan prasyarat, info leak terbatas |
| Low / Minor | Display, validasi, error handling, tanpa leak / tanpa dana | Label salah, param diabaikan, exit code salah |

Contoh vector Minor (M1-1, XE-18358): `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N` skor 0.0, tapi dampaknya bukan keamanan melainkan keandalan operator, jadi claim Minor program (bukan CVSS). Kalau CVSS 0.0 tapi bug nyata, jelasin kenapa tetap layak Minor dan jangan paksain skor.

Aturan: ragu antara dua tingkat, ambil yang lebih rendah dan jelasin kenapa. Severity dilebih-lebihin = kredibilitas hilang, dan triager bakal diskon laporan berikutnya.


## Struktur laporan

### 1. Judul
Spesifik: jenis bug + lokasi + dampak.
- Salah: "XSS di website"
- Bener: "Stored XSS di kolom komentar /posts/{id} memungkinkan pengambilalihan sesi"

### 2. Ringkasan
2-3 kalimat. Apa bug-nya, di mana, akibatnya.

### 3. Severity
Usulin Low / Medium / High / Critical. Idealnya pakai CVSS + alasan. Jangan dilebih-lebihin, karena kredibilitasmu taruhannya. Kalau ragu antara dua tingkat, ambil yang lebih rendah dan jelasin kenapa.

### 4. Langkah reproduksi
Ini bagian paling penting. Harus bisa diikutin orang asing dari nol. Cantumin URL, parameter, metode HTTP, akun/role, payload atau request lengkap, plus browser/versi. Tiap langkah bernomor, tiap langkah punya hasil yang bisa dicek. Kalau ada setup (akun test, environment lokal), tulis dari nol.

### 5. Proof of Concept
Screenshot, video singkat, atau skrip minimal. Samarkan data sensitif. Buktikan dampak tanpa ngerusak. PoC harus nunjukin dampak, bukan cuma nunjukin request terkirim. Stop setelah bukti cukup, jangan exploit lebih jauh.

### 6. Dampak
Skenario realistis aja. Siapa terdampak, data apa yang bisa diakses, apa yang bisa dilakuin penyerang. Jangan berspekulasi liar. Fokus dampak bisnis: account takeover, data leak, RCE biasanya dinilai tinggi. Kalau dampaknya cuma display/cosmetic, bilang begitu dengan jujur dan claim Minor/Low.

### 7. Rekomendasi perbaikan
Saran singkat: validasi input, output encoding, cek otorisasi di server, rate limiting. Opsional, tapi biasanya disuka tim. Satu paragraf, jangan essay.

### 8. Info tambahan
Lingkungan uji, tanggal/waktu, referensi CWE/OWASP, versi kode/commit yang diuji (HEAD/commit hash kalau dari repo publik).

## Template ringkas

```
Judul: [Bug] pada [komponen] memungkinkan [dampak]
Ringkasan → Severity (CVSS) → Langkah Reproduksi → PoC → Dampak → Rekomendasi → Info tambahan
```

Template lengkap per laporan ada di `templates/report.md`.

## Tips biar diterima

- Satu laporan = satu bug, kecuali chain dan lo jelasin rantainya.
- Bahasa profesional & netral, jangan nuntut atau nyebut bounty di awal.
- Laporan dibaca sebagai SATU ethical hacker profesional (manusia): jangan pernah nyebut agent, subagent, atau sistem multi-agent ("3 agents", "agent") di laporan — nggak ada jejak AI/multi-agent di teks yang dikirim. Tulis rapi ala manusia, tanpa em-dash. Laporan wajib bahasa Inggris.
- Fokus dampak bisnis: account takeover, data leak, RCE biasanya dinilai tinggi.
- Selalu ada bukti yang bisa diulang.
- Berhenti setelah bukti cukup, jangan exploit lebih jauh.
- Balas klarifikasi cepet & sopan.
- Patuhi disclosure policy, jangan publikasi sebelum diizinin.

## Kesalahan umum

- Judul terlalu umum.
- Langkah reproduksi ambigu (nggak bisa diikutin orang asing dari nol).
- Lapor hasil scanner tanpa verifikasi.
- Severity dilebih-lebihin.
- Lapor out-of-scope / known issue.
- Spam laporan duplikat / berkualitas rendah.

## Filing (setelah user milih kandidat)

- File SATU-SATU, jangan batch beberapa laporan sekaligus. Jeda antar submit: program bisa rate-limit (XE: 3x ditolak "too many reports from this address", lolos di percobaan ke-4 setelah ~19 menit).
- Verifikasi setelah submit: buka halaman tiket, konfirmasi status New, severity yang di-claim, visibilitas yang benar, dan tiket muncul di daftar laporan akun. Catat ID + URL mentah.
- Update file draft dengan ID tiket + tanggal file. Jangan file ulang kandidat yang sama.

## Pasca-file

- Pantau status tiket: New -> triaging -> accepted / closed (duplicate / invalid / out of scope). Cek berkala, catat perubahan status + tier/award di MEMORY.md.
- Balas klarifikasi (needs-info) cepat dan sopan, jawab yang ditanya saja, tambah bukti kalau diminta. Jangan debat severity di thread, sampaikan fakta.
- Kalau salah visibilitas (misal ke-file private padahal harus public) dan program tidak menyediakan tombol ubah: withdraw tiketnya, lalu file ulang dengan visibilitas benar. Jangan file duplikat tanpa withdraw dulu.
- Kalau ditutup duplicate: baca tiket yang diduplikat, catat root cause yang sama, jangan file varian dari keluarga itu lagi.
- Kalau ditutup invalid / intended design: catat alasannya di file kandidat, jangan ajukan ulang dengan kata-kata berbeda.
- Jangan publikasi temuan sebelum disclosure policy mengizinkan.


## Appendix: standing rules XE Bounty (program-specific, bukan aturan umum)

- Tier XE (ceiling, paid in XE at mainnet): Critical 50,000, Severe 25,000, High 10,000, Medium 2,500, Minor 650.
- Laporan XE harus PUBLIC: uncheck "Keep this report private" (default checked) sebelum submit. Reporter tidak bisa mengubah visibilitas setelah filing; satu-satunya jalan adalah withdraw lalu file ulang.
- Dedup via desk API: `GET /v1/tickets?q=<keyword>` di bounty.xe.network, cari root cause, bukan judul.
- PoC live di node lokal sebelum filing (loopback, throwaway wallet, no testnet funds). Contoh terverifikasi: M1-1 `xe lease renew` print cost 1.000.000x (XE-18358, Minor, filed 2026-11-18).
- Jangan file varian SSE re-validation (XE-18076 sudah klaim angle itu, 2026-11-18).
- Akun: <YOUR_BOUNTY_USERNAME> (GitHub <YOUR_GITHUB_HANDLE>). Login via browser, sesi bisa expired dan perlu sign-in ulang.

## Verification checklist (sebelum file)

- [ ] Folder program ada, scope.md terisi (kutipan scope, tier, disclosure policy)
- [ ] Scope program dibaca, bug in-scope, kutipan scope ada di draft
- [ ] Pencarian duplikat dilakukan per prosedur program, ID terdekat dicatat, verdict NOT-DUPLICATE beralasan
- [ ] Reproduksi diulang 2x dari nol, output asli dikutip (bukan dikarang), file PoC ada kalau butuh bukti live
- [ ] PoC nunjukin dampak, data sensitif disamarkan, tidak ada data user lain
- [ ] Severity jujur, CVSS vector + skor ada, tidak dilebih-lebihin
- [ ] Judul spesifik (bug + lokasi + dampak)
- [ ] Satu laporan = satu bug (atau chain dijelaskan)
- [ ] User sudah milih kandidat ini untuk di-file
