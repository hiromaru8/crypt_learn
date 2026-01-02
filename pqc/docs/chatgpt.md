耐量子暗号（**Post-Quantum Cryptography：PQC**）とは、将来量子コンピューターによってRSAやECCのような従来の公開鍵暗号が破られるリスクに対抗するため、量子コンピューターでも解読が困難と考えられる数学的問題に基づく暗号方式の総称です。([NIST][1])

---

## ✅ 主要な耐量子暗号の候補方式（NIST標準化を中心に）

以下は、**米国標準技術研究所（NIST）**が評価・選定している耐量子暗号アルゴリズムの主要候補です。([NIST][1])

---

### 🔐 **公開鍵暗号／鍵交換（KEM：Key Encapsulation Mechanism）**

| 方式名                            | ベース理論      | 役割            |
| ------------------------------ | ---------- | ------------- |
| **CRYSTALS-Kyber (ML-KEM)**    | 格子問題（LWE系） | 鍵交換・暗号化       |
| **HQC (Hamming Quasi-Cyclic)** | 符号理論       | 鍵交換のバックアップ候補  |
| **Classic McEliece**           | 符号理論       | 伝統的候補（標準化外評価） |
| **BIKE**                       | 符号理論       | 標準化候補だが未最終選定  |

* **Kyber** は NIST のメイン標準として最も広く推奨される耐量子鍵交換／暗号化方式。性能と安全性のバランスが良く、多くの実装で採用が進んでいます。([NIST][1])
* **HQC** は 2025 年に追加で標準化予定の鍵交換方式で、Kyber とは異なる数学的基盤（誤り訂正符号）を使うことで冗長性と多様性を確保します。([Palo Alto Networks][2])
* **Classic McEliece** や **BIKE** は符号理論に基づく古典的候補で、実装実績は長いですが（McEliece は1990年代から）、NIST 内では標準化候補としての扱いが変化しています。([PostQuantum.com][3])

---

### ✍️ **デジタル署名**

| 方式名                             | ベース理論 | 役割            |
| ------------------------------- | ----- | ------------- |
| **CRYSTALS-Dilithium (ML-DSA)** | 格子問題  | 署名            |
| **SPHINCS+ (SLH-DSA)**          | ハッシュ  | 署名（耐量子バックアップ） |
| **FALCON (FN-DSA)**             | 格子問題  | 署名（追加標準化予定）   |

* **Dilithium** は PQC 署名の主力として選定されており、効率・安全性・実装性のバランスが良いと評価されています。([NIST][1])
* **SPHINCS+** は格子とは別のアプローチ（ハッシュベース）で安全性の多様性を提供します。([NIST][1])
* **FALCON** はより高速かつコンパクト署名を目指す格子ベースの署名方式で、標準化が進行中です。([NIST][1])

---

## 🧠 数学的基盤の違い

耐量子暗号は、量子コンピューターの能力でも解けないと考えられる数学的問題に依存します。主な基盤は次のとおりです。

* **格子（Lattice）問題：** Kyber、Dilithium、FALCON など
* **ハッシュ関数：** SPHINCS+
* **符号理論（Error-Correcting Codes）：** HQC、Classic McEliece、BIKE

これらは従来の RSA/ECC のような整数の素因数分解や離散対数問題ではなく、量子アルゴリズム（Shor など）でも効率的に解けないと考えられる問題を使った方式です。([NIST][1])

---

## 🧩 実装・移行のポイント

* **ハイブリッド運用**：量子耐性アルゴリズムだけでなく、既存の RSA/ECC と組み合わせて使う（“crypto-agility”）ことが業界では推奨されています。([野村証券][4])
* **標準化と実装**：多くのライブラリ（OpenSSL など）が PQC 方式の実装や実験的サポートを追加しています。([arXiv][5])
* **移行タイムライン**：NIST などの標準化団体は 2030 年代を見据えて従来暗号から PQC への移行完了を目指しています。([NRI][6])

---

## 🧾 まとめ：主な耐量子暗号候補

### 鍵交換・暗号化（KEM）

* **CRYSTALS-Kyber (ML-KEM)** – メイン推奨
* **HQC** – 追加選定予定
* **Classic McEliece / BIKE** – 評価対象

### デジタル署名

* **CRYSTALS-Dilithium (ML-DSA)** – 標準
* **SPHINCS+ (SLH-DSA)** – ハッシュベースバックアップ
* **FALCON (FN-DSA)** – 追加標準化進行中

---

必要であれば、**各方式の性能比較（鍵長・署名サイズ・計算コスト）**や、**実装例（OpenSSL など）での使い方**も詳細に解説できますので、続けて聞いてください。

[1]: https://www.nist.gov/cybersecurity/what-post-quantum-cryptography?utm_source=chatgpt.com "What Is Post-Quantum Cryptography? | NIST"
[2]: https://www.paloaltonetworks.com/cyberpedia/what-is-post-quantum-cryptography-pqc?utm_source=chatgpt.com "What Is Post-Quantum Cryptography (PQC)? A Complete Guide - Palo Alto Networks"
[3]: https://postquantum.com/post-quantum/post-quantum-cryptography-pqc/?utm_source=chatgpt.com "Post-Quantum Cryptography (PQC) Introduction"
[4]: https://www.nri-secure.co.jp/glossary/post-quantum-cryptography?utm_source=chatgpt.com "耐量子計算機暗号（Post-Quantum Cryptography）｜セキュリティ用語解説｜NRIセキュア"
[5]: https://arxiv.org/abs/2508.16078?utm_source=chatgpt.com "A Survey of Post-Quantum Cryptography Support in Cryptographic Libraries"
[6]: https://www.nri.com/jp/media/journal/20251126.html?utm_source=chatgpt.com "耐量子計算機暗号（PQC）の現状と今後 | NRI JOURNAL | 野村総合研究所(NRI)"
