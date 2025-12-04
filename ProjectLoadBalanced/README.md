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
![WhatsApp Image 2025-12-03 at 21 05 54_6f17c98d](https://github.com/user-attachments/assets/65e88ecf-4976-4ac0-98ac-a20d16b89848)


**Cara Menjalankan**

**Build image backend:**

docker build -t backend-app .


**Jalankan semua service:**

docker compose up -d


**Cek container berjalan:**

docker compose ps


   **Melihat log:**
   
   docker compose logs nginx
   docker compose logs backend1
   docker compose logs backend2


   **Tes aplikasi:**

   curl http://localhost:8080

   **Hasil Running**
   <img width="1263" height="248" alt="Screenshot 2025-12-04 130318" src="https://github.com/user-attachments/assets/575a715c-533e-4584-97fd-0ecc5b4a48fb" />
   
   <img width="1901" height="617" alt="Screenshot 2025-12-04 134525" src="https://github.com/user-attachments/assets/7da22910-010e-4647-a79f-f09462f1abaf" />




   


   **Konfigurasi**
   **1. Dockerfile (Penjelasan Ringkas)**

   Dockerfile bertugas membangun image untuk backend Flask. Isi dan fungsinya:

   Base image: python:3.10-slim

   Install dependency: Flask & redis-py untuk koneksi ke Redis

   Copy source code: seluruh folder /src dipindahkan ke dalam container

   Set working directory: /app

   Expose port: 5000 agar dapat diakses oleh Nginx

   CMD: menjalankan python app.py sebagai aplikasi utama

   Ringkasannya: Dockerfile membuat image backend API siap dijalankan dengan Flask + Redis.

   **2. docker-compose.yml (Hubungan Antar Service)**

   File docker-compose.yml mengatur keseluruhan arsitektur sistem multi-container:

   Service & Hubungan Antar Service:

   backend1 dan backend2

   Dibangun dari Dockerfile yang sama

   Mengakses Redis melalui hostname service redis

   Tidak diexpose ke host → hanya internal network

   **Redis**

   Database untuk menyimpan total_visits

   Menggunakan volume redis_data:/data agar data persistent

   nginx

   Reverse proxy & load balancer

   Mengarahkan request client ke backend1 & backend2 (round robin)

   Mendengarkan pada port 8080

   Terhubung ke backend melalui internal network

   **Network**

   Semua service otomatis berada di jaringan internal:
   projectloadbalanced_default
   sehingga dapat saling berkomunikasi menggunakan nama service (backend1, backend2, redis).

   **Volume**

   redis_data untuk menyimpan data kunjungan secara permanen.

   Ringkasannya:
   docker-compose.yml menghubungkan backend ↔ Redis ↔ Nginx menjadi satu sistem load-balanced API dengan database persistent.
   Base image: python:3.10-slim

   Install dependency Flask + Redis client

   Copy source code

   Expose port 5000

   CMD menjalankan app.py

   docker-compose.yml

   **Service:**

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

**Kendala & Solusi**
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
