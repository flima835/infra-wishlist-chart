from flask import Flask, jsonify, request, Response
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST
)
import time

app = Flask(__name__)

# ── Métricas de negócio ──────────────────────────────────────
WISH_COUNT = Gauge(
    'wishlist_total_wishes',
    'Total de desejos na lista'
)

REQUEST_COUNT = Counter(
    'wishlist_requests_total',
    'Total de requisições',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'wishlist_request_duration_seconds',
    'Latência das requisições em segundos',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

wishes = []

# ── Middleware de métricas automático ────────────────────────
@app.before_request
def start_timer():
    request._start_time = time.time()

@app.after_request
def record_metrics(response):
    if request.path != '/metrics':
        latency = time.time() - request._start_time
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.path
        ).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
    return response

# ── Rotas ────────────────────────────────────────────────────
@app.route('/wishes', methods=['GET'])
def get_wishes():
    return jsonify(wishes)

@app.route('/wishes', methods=['POST'])
def add_wish():
    data = request.get_json()
    wishes.append(data.get('wish', ''))
    WISH_COUNT.set(len(wishes))
    return jsonify({'status': 'added', 'wishes': wishes}), 201

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
