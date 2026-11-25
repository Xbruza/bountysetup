---
name: local-cybersec-glossary
description: Kamus istilah hacking & cybersecurity — umum + Web3 (3.379 baris total, 21 + 19 seksi). Use when you need the precise name, class, or standard mapping (CWE/CVSS/OWASP/MITRE/SWC) for a vulnerability, technique, or security concept while hunting or writing a bug bounty report. Load on demand, never paste whole.
---

# Cybersecurity Glossary — kamus istilah umum + Web3

Source: dua file upload user 2026-11-20, disimpan di `~/workspace/user/files/`:
- `kamus_hacking_cybersecurity_umum.txt` (1.788 baris, 36.714 byte,
  21 seksi) — istilah umum: web, network, OS, memory, malware, auth,
  crypto, recon/OSINT, forensics, standar. **Tanpa Web3.**
- `kamus_hacking_cybersecurity_web3.txt` (1.591 baris, 31.775 byte,
  19 seksi) — Web3: fundamental blockchain, smart contract & EVM
  exploits, DeFi/DEX/lending, MEV, bridge, wallet/NFT, governance/DAO,
  Solana & non-EVM, oracle/indexer, standar audit (SWC, OWASP Smart
  Contract Top 10, Code4rena/Sherlock/Cantina).

Use this skill for:
- naming a finding precisely: cari istilah yang tepat sebelum nulis judul
  laporan (mis. IDOR vs BOLA; reentrancy vs read-only reentrancy;
  ERC-4626 inflation vs donation attack; oracle TWAP manipulation vs
  spot manipulation)
- mapping ke standar: CWE / CVE / CVSS / OWASP Top 10 / OWASP Smart
  Contract Top 10 / SWC Registry / MITRE ATT&CK buat severity +
  klasifikasi di laporan (umum seksi 19-20, Web3 seksi 15 + 19)
- hunting web/app scope (Socket, BYDFi/BugEx, XE web assets): kelas
  kerentanan web (umum seksi 3), auth/identitas (umum seksi 8),
  recon/OSINT (umum seksi 10), cloud/container (umum seksi 14)
- hunting smart contract / DeFi (Merkl, WalletConnect, XE node):
  fundamental chain (Web3 seksi 6), EVM exploits (Web3 seksi 7),
  DeFi/DEX/lending (Web3 seksi 8), MEV (Web3 seksi 9), bridge
  (Web3 seksi 10), wallet/signature/NFT (Web3 seksi 11), governance
  (Web3 seksi 12), Solana/non-EVM (Web3 seksi 13)
- baca laporan audit / post-mortem exploit / program bounty: decode
  istilah yang tidak dikenal (Web3 seksi 18: bahasa laporan exploit —
  root cause, funds at risk, invariant break, accounting mismatch)

Don't use for:
- payload, exploit code, atau langkah serangan — kamus ini HANYA nama dan
  definisi kelas, bukan panduan exploit; PoC tetap ditulis dari verifikasi
  kode + reproduksi live, bukan dari kamus
- dedup: kamus tidak tahu finding mana yang sudah dilaporkan; dedup tetap
  lewat prosedur program (desk API, laporan audit, riwayat Cantina/
  Code4rena/Sherlock) — kamus cuma bantu menamai kandidatnya dengan tepat
- menyerang target out-of-scope; aturan program + SOP bounty tetap di atas
  kamus ini

## How to use

- Jangan baca seluruh file ke context. `grep -i "<istilah>"` file yang
  relevan, atau `grep -n "^==\|^[0-9]+\."` buat daftar seksi, lalu baca
  seksi yang relevan saja.
- Pilih file dulu: istilah umum/web/network -> file umum; istilah
  chain/kontrak/DeFi/bridge/MEV -> file Web3. Satu istilah bisa muncul di
  kedua file dengan nuansa beda — pakai yang sesuai konteks temuan.
- Seksi yang paling sering dipakai: umum 3 (web vulns), 8 (auth), 10
  (recon), 19-20 (standar + singkatan); Web3 6-7 (fundamental + EVM
  exploits), 8 (DeFi), 10 (bridge), 15 (standar audit), 18 (bahasa
  laporan exploit), 19 (singkatan).
- Kalau istilahnya tidak ada di kamus, jangan dipaksa: sebutkan apa
  adanya dari kode / perilaku yang diamati, lalu cari mapping CWE/SWC
  yang paling dekat.

## Boundaries (no dupe)

- `local-agentic-bug-hunter`: workflow hunting (recon -> hunt -> validasi).
  Kamus ini referensi penamaan, bukan workflow.
- `local-claude-bughunter`: pola deteksi + payload per kelas dari
  disclosed reports. Kamus ini definisi kelas, bukan pola serangan.
- `local-bounty-reporting`: penulisan + filing laporan. Kamus ini
  dipakai DI DALAM langkah penamaan/klasifikasi laporan itu.
