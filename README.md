# Project UAS Sistem Operasi – Docker & Docker Compose

## Kelompok 4  
- Alayavaro Rachmadia : 2410501095  
- Panji Anugerah Panengah : 2410501105  
- Rakha Abyan Hertamtama : 2410501089
- Rizki Ramadhan : 2410501091
- Shidqi Athalla Arka Qafriyanto : 2410501077

## Tema Project  
Load Balancer + 2 Backend Instance + Redis Database (Data Persistence)


## Layanan dalam Project
1. **Backend 1 (Python Flask API)**  
   Menyediakan endpoint / yang menampilkan:

   container_id

   total_visits (dari Redis)

   status koneksi database

2. **Backend 2 (Python Flask API)**  
   Instansi kedua backend untuk load balancing, menjalankan fungsi yang sama dengan backend1.

3. **Redis Database**  
   Menyimpan jumlah kunjungan (`total_visits`) secara persistent menggunakan Docker Volume.

4. **Nginx Reverse Proxy / Load Balancer**  
   Mendistribusikan request secara bergantian ke backend1 dan backend2 (round robin).

---

## Arsitektur Sistem  
Arsitektur Sistem
        ┌──────────────────────────────────────┐
        │               Client                 │
        └───────────────────────┬──────────────┘
                                │  HTTP :8080
                                ▼
                     ┌────────────────────┐
                     │     NGINX LB       │
                     │   (Reverse Proxy)  │
                     └───────┬────────────┘
             ┌───────────────┴───────────────┐
             ▼                               ▼
   ┌──────────────────┐             ┌──────────────────┐
   │   Backend 1      │             │   Backend 2      │
   │ Flask API :5000  │             │ Flask API :5000  │
   └─────────┬────────┘             └─────────┬────────┘
             │                                │
             └──────────────┬─────────────────┘
                            ▼
                  ┌──────────────────┐
                  │      Redis        │
                  │  DB :6379         │
                  └──────────────────┘

Cara Menjalankan

Build image backend:

docker build -t backend-app .


Jalankan semua service:

docker compose up -d


Cek container berjalan:

docker compose ps


Melihat log:

docker compose logs nginx
docker compose logs backend1
docker compose logs backend2


Tes aplikasi:

curl http://localhost:8080

Hasil Running

Contoh Output:

{
  "container_id": "fc897fc7d06b",
  "message": "Halo dari Backend API!",
  "database_status": "Terhubung",
  "total_visits": 12
}



Base image: python:3.10-slim

Install dependency Flask + Redis client

Copy source code

Expose port 5000

CMD menjalankan app.py

docker-compose.yml

Service:

backend1: membangun dari Dockerfile backend

backend2: instance kedua backend

redis: database, menggunakan volume redis_data:/data untuk persistence

nginx: reverse proxy & load balancer

Konfigurasi lain:

Semua service berada pada 1 internal network

Port mapping:

nginx: 8080:80

redis: 6379:6379

backend internal only (tanpa port host expose)

Kendala & Solusi
1. Backend awalnya jalan di port 3000 = Load balancer error

Solusi: Mengubah Flask app.run() menjadi:

app.run(host="0.0.0.0", port=5000)

2. Nginx 502 Bad Gateway

Solusi: Memastikan upstream memakai nama service Docker Compose (backend1:5000, backend2:5000).

3. Redis tidak persistent

Solusi: Menambahkan volume:

volumes:
  redis_data:

4. Request tidak bergantian ke Backend1/Backend2

Solusi: Memakai round_robin default pada Nginx upstream.

Note:
(Dokumentasi Lengkapnya ada Di PDF)
