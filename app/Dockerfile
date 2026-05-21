# ─────────────────────────────────────────
# Estágio 1: Builder — instala dependências
# ─────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Copia só o requirements primeiro (aproveita cache de camadas)
COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─────────────────────────────────────────
# Estágio 2: Runtime — imagem final mínima
# ─────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Boas práticas de segurança: não rodar como root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copia apenas os pacotes instalados (sem build tools)
COPY --from=builder /install /usr/local

# Copia o código da aplicação
COPY app.py .

# Define usuário não-privilegiado
USER appuser

# Documenta a porta exposta
EXPOSE 8080

# Health check nativo do Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Gunicorn: servidor WSGI de produção
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]
