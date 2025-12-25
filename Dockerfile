# আমরা python:3.9-slim এর বদলে python:3.9-slim-bullseye ব্যবহার করছি
# Bullseye হলো Debian 11, যা খুব স্ট্যাবল এবং এখানে সব প্যাকেজ পাওয়া যায়।
FROM python:3.9-slim-bullseye

# সিস্টেম ডিপেন্ডেন্সি ইনস্টল করা
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean

# ওয়ার্কিং ডিরেক্টরি সেট করা
WORKDIR /app

# সব ফাইল কপি করা
COPY . /app

# পাইথন লাইব্রেরি ইনস্টল করা
RUN pip install --no-cache-dir -r requirements.txt

# বট রান করা
CMD ["python", "main.py"]
