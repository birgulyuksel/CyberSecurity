"""
config.py
Genel yapılandırma ayarları.
Gizli veri tutulmamalıdır! API key gerekirse .env / secret manager kullanılmalı.
"""

HIBP_API_BASE_URL = "https://api.pwnedpasswords.com"
HIBP_RANGE_ENDPOINT = "/range/{prefix}"

# HIBP dokümanlarına göre anlamlı bir User-Agent 
USER_AGENT = "password-breach-check-student-project/1.0"

# Gizlilik açısından önerilir.
ADD_PADDING = True

# HTTP timeout (saniye)
REQUEST_TIMEOUT = 5
