# Gunakan image python yang ringan
FROM python:3.10-slim

# Set folder kerja di dalam container
WORKDIR /app

# Copy daftar dependency dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode ke dalam container
COPY . .

# Jalankan bot
CMD ["python", "run_bot.py"]