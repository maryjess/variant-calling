# Static results viewer only. No R/Bioconductor, no scikit-learn — this
# image only ever reads and displays CSVs that were already computed
# elsewhere (your original submission's predictions + metrics).
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Populate before building — see README notes in app.py.
# {sample}_pred.csv for syn1..syn5 only (no real1/real2), plus metrics.csv
COPY precomputed/ ./precomputed/

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
