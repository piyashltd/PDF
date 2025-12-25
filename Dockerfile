# Python 3.10 এর হালকা ভার্সন ব্যবহার করা হচ্ছে
FROM python:3.10-slim

# WeasyPrint এর জন্য প্রয়োজনীয় সব সিস্টেম লাইব্রেরি ইন্সটল করা
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ফোল্ডার সেটআপ
WORKDIR /app

# ফাইল কপি করা
COPY . .

# পাইথন লাইব্রেরি ইন্সটল
RUN pip install --no-cache-dir -r requirements.txt

# অ্যাপ রান করা
CMD ["python", "main.py"]
