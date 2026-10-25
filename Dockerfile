# ═══════════════════════════════════════════════════════════════════
# OOREDOO BOT - Docker Image
# ═══════════════════════════════════════════════════════════════════

FROM python:3.11-slim

# ─── معلومات الصورة ───
LABEL maintainer="moon" \
      description="Ooredoo Bot - Unlimited Mode v1.5.22" \
      version="1.5.22"

# ─── متغيرات البيئة ───
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Africa/Algiers

# ─── إعدادات المنطقة الزمنية ───
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata ca-certificates && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# ─── مجلد العمل ───
WORKDIR /app

# ─── تثبيت المكتبات ───
RUN pip install --no-cache-dir \
    pyTelegramBotAPI==4.23.0 \
    requests==2.32.3

# ─── نسخ ملفات المشروع ───
COPY bot.py /app/bot.py

# ─── إنشاء مجلد البيانات (للملفات المحفوظة) ───
RUN mkdir -p /app/data && \
    ln -sf /app/data/ooredoo_users.json /app/ooredoo_users.json && \
    ln -sf /app/data/ooredoo_activations.json /app/ooredoo_activations.json

# ─── مستخدم غير root للأمان ───
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app
USER botuser

# ─── مجلد البيانات (Volume) ───
VOLUME ["/app/data"]

# ─── تشغيل البوت ───
CMD ["python", "-u", "bot.py"]
