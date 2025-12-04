from flask import Flask, jsonify
import os
import redis
import socket

app = Flask(__name__)

# Mengambil konfigurasi dari Environment Variable (sesuai ketentuan UAS)
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = os.environ.get('REDIS_PORT', 6379)

# Koneksi ke Database Redis (Service 3: Database Kecil)
try:
    cache = redis.Redis(host=redis_host, port=redis_port)
    cache.ping()
    db_status = "Terhubung"
except redis.exceptions.ConnectionError:
    db_status = "Terputus (Pastikan service Redis berjalan)"

@app.route('/')
def hello():
    # Fitur Database: Menghitung jumlah kunjungan (Counter)
    count = 0
    if db_status == "Terhubung":
        count = cache.incr('hits')
    
    # Mengambil Hostname Container untuk membuktikan Load Balancing
    # Saat di-refresh, container_id akan berubah jika load balancer bekerja
    container_id = socket.gethostname()

    return jsonify({
        "message": "Halo dari Backend API!",
        "container_id": container_id,
        "database_status": db_status,
        "total_visits": count,
        "info": "Refresh halaman ini untuk melihat container_id berubah (Load Balancing)"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)