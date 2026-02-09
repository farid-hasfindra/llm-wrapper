# 🚀 Tutorial Deployment: The "Easy & Free" Way (Render.com)

Anda merasa EC2 terlalu ribet (harus SSH, terminal, config Linux)? Tenang, ada **Render.com**.
Ini adalah layanan **Container-as-a-Service** (mirip AWS ECS) tapi jauh lebih otomatis dan punya **Free Tier**.

Cocok banget untuk Portfolio:
1.  **Gratis** (untuk hobby project).
2.  **Otomatis** (Connect GitHub -> Auto Deploy).
3.  **Docker Native** (Menggunakan `Dockerfile` yang sudah kita buat).
4.  **Zero Config** (Tidak perlu SSH/Linux).

---

## Langkah 1: Push Code ke GitHub
Pastikan kode project Anda sudah ada di repository GitHub (Public/Private).

## Langkah 2: Daftar Render
1.  Buka [dashboard.render.com](https://dashboard.render.com/).
2.  Login menggunakan akun **GitHub** Anda.

## Langkah 3: Create Web Service
1.  Klik tombol **New +** di pojok kanan atas.
2.  Pilih **Web Service**.
3.  Pilih **Build and deploy from a Git repository**.
4.  Pilih repository `llm-wrapper` Anda.

## Langkah 4: Konfigurasi (Penting!)
Isi form dengan setting berikut:

*   **Name**: `llm-portfolio` (bebas).
*   **Region**: `Singapore` (biar cepat).
*   **Branch**: `main`.
*   **Root Directory**: (Kosongkan/Default).
*   **Runtime**: **Docker** (PENTING! Jangan pilih Python, pilih Docker karena kita sudah punya `Dockerfile`).
*   **Instance Type**: **Free** (0.5 CPU, 512MB RAM).

## Langkah 5: Environment Variables (.env)
Scroll ke bawah ke bagian **Environment Variables**. Masukkan key-value dari file `.env` Anda:

| Key | Value |
| :--- | :--- |
| `PROJECT_NAME` | `LLM-Wrapper` |
| `GOOGLE_API_KEY` | `AIzaSy....` (Copy dari .env asli Anda) |
| `ENVIRONMENT` | `production` |
| `PORT` | `8000` |

## Langkah 6: Deploy!
Klik **Create Web Service**.

Render akan:
1.  Clone repo Anda.
2.  Membangun Docker Image (membaca `infra/docker/Dockerfile` otomatis).
3.  Menjalankan container.

Tunggu sekitar 3-5 menit. Dalah log akan muncul:
`Release is live` atau `Application startup complete`.

## Cek Hasil
Di pojok kiri atas dashboard Render, ada URL project Anda (misal: `https://llm-portfolio-xyz.onrender.com`).
Klik URL terseut dan tambahkan `/docs` di belakangnya.

Contoh: `https://llm-portfolio-xyz.onrender.com/docs`

**Selamat! Project Anda sudah online!** 🥳

---

# 🤔 FAQ: Kenapa Tidak AWS ECS?

**Tanya**: "Kenapa tidak pakai AWS ECS saja?"
**Jawab**:
1.  **ECS Fargate (Mudah)**: **TIDAK GRATIS**. Anda harus bayar per menit CPU/RAM berjalan.
2.  **ECS EC2 (Gratis)**: **SANGAT RIBET**. Anda harus setup Cluster, Capacity Provider, Auto Scaling Group, VPC Networking, dan Load Balancer secara manual. Jauh lebih ribet dari tutorial EC2 sebelumnya.

Untuk Portfolio pribadi, **Render** atau **Railway** adalah standar industri saat ini karena kemudahannya (Developer Experience).
