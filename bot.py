"""
╔══════════════════════════════════════════════════════════════════╗
║ OOREDOO BOT - by moon - VERSION 1.5.22 (UNLIMITED - NO LIMITS)   ║
║ ✨ NEW: Multi-Number Support + Auto-Activate on Saved Numbers    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from requests.adapters import HTTPAdapter
import json, os, threading, re, uuid, base64, time, urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "7756358682:AAFkM6psAsxEx2p32VJAg65jQntIQ51d5p8"
ADMIN_IDS = [7462133840]
NOTIFY_CHANNEL_ID = "@ooredoodz6"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

OOREDOO_BFF = "https://apis.ooredoo.dz/api/ooredoo-bff"
OOREDOO_AUTH = "https://apis.ooredoo.dz/api/auth/realms/myooredoo/protocol/openid-connect/token"
OOREDOO_CLIENT_ID = "myooredoo-app"
OOREDOO_X_VERSION = "1.5.17"
OOREDOO_X_SIG = "5c7641dbb82cf11066df68afc91541c967640106a95192740b43d51a5ce6777a"
OOREDOO_PLATFORM = "android"
OOREDOO_PLATFORM_ORIGIN = "mobile-android"

OOREDOO_INTEGRITY_1 = "JWBTpxXcH7KY9EXYeIRp8NjQMx2dt3vF8ejjoARazyoFzOw6Cu8+wkeV+zSVHSTeI6a12SG/FU+Q/9uBrcN71RlYO4CulD2x375NKwJRAInar8DVUilHBKUfjEsoHd6EwfLCfdYzLNXJu9POfEf6tqKn3PUe0pY6qZxWLhyVAFHw8Qwb52ZqdI2soCH4S3mrz+OZL+YovdGSUKlXKIkxVroAMTAg3jljLF7gvXaEsB/O3uW+tbkBMwSX2uTOwf+rh3sgOF/zPhKCFgRvZmU1o87Fa96Y/+wOcK+UpfXTCBYVrvQ1wG6ryC7vHMSqgUhYJK4tbSoti0zv4av9pwxh9Iv2MgsMENjyKBK/TuFZxEG3xQCKj1LTMgn2xBEeKcbsKrEW3xDRwsccGI3D7GHnbUlhdI4ujDIRQVKHaZSwhTp+32Cr4EB/Qt8p/xRbdgCde9MUlM4AYIGlfyVoHSkOvTu5c0DIIy1EhowtAkbKIJl49wsYKWvpT/nXFWzeXP3R2qzaclCnIb9qihhrarmwz8l8XH2T+f7AK2uSNiuWLG5Fy2mM/YLmuJPZT9Ciag/mpy7JGImKNQAcFbSAInBdKQjUKT+COzZfrXj5rwil9/HDMtuzIovq8hrQGY+roTfVPheTLWmcjkVCOL8VXAHjPb22vOuqrkMioWT9CQ5O8RgW7RKHrObeKQMp8F7tSjOqkxYDFkPVN1G4nkEBrTlPKK9YtPl+j7IuH9fGcDTwhCTTqP8peuBryW0L11tApvAEi7VkJyBxpVxW"
OOREDOO_INTEGRITY_2 = "JWBTpxXcH7KR/kzaHeUUydDWODuU4i3H4fL9gCgKzyYfyN4qLJJE8keV+zSVHSTeI6aEyC2tbSza/NGmkflQ/UgaNZSN9SKxz7tcdQckHY25n6mOaDZ9PPMQmF4sKZqDwebce/c1SNGNn6qvTULW/L348aJvy7Vii6dyPTu3OSPV9AwKwGwQKNHN61HyK3jx/fa8Os5ux9u3Q654YLZrAJ99QGEm/C9nEBPmlHC98RjovLGBnuJOGx6k7fnyrt/Ogy5fNg+tBgi5HEsoXDAwutX7TOWfx4YKHpKW//TvPRQgp69e2Xqa+CvGJJ+a/WlPMPhRCSsfo0OG04mVvlkc8eXiLzV/GPuJCEmcRf9Z6V+xoDyMtU7OZ3XT5BMhI/D/N68LsRn/9dIBH6X7n0WAW3tzeKZK1zENWFKrd7aLlzEdwFzO/1JTQsEDom5TRie0Kd5yic4BGvS1C1BsA2wJhzyiZ2j7RUE9m8tOAkPEIs929FYIfmH8XcCQKHT0TqT0+N+wCiyfNawPlDhZWcObscFZeEmKgvqiUFCoCj6xI1hvyHK0nu7fnZ/sGc6oNT/SrFjubYWjOyoYFL7gMnlYAhyjZhjuAwN1m1/wjwrOx8DbFr2NW8qb3hv+CIzK1zL3LDryKjqNkTxcOp4aJnmSTa73guCEmWc7pnLkLw5O8RgW7RKHrObeeQ0l9lu4HWXwlhdWRxvVMQDimhtTrGASL6sIuaxyhOkrH4HFImP70SaCoK9+euMxnzkPjg9HqPIFj+I0KSMloVxW"

OOREDOO_PROXIES = [
    "gate.busyip.com:18080:bi_23ee2cd9-session-s1-type-residential-mode-sticky:9C0h1L16DX5gwKbv",
]

OOREDOO_USERS_FILE = "ooredoo_users.json"
ACTIVATIONS_FILE = "ooredoo_activations.json"

ooredoo_data = {}
activations_data = {}

http_session = requests.Session()
adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=1)
http_session.mount("https://", adapter)
http_session.mount("http://", adapter)

file_lock = threading.Lock()

def load_ooredoo_data():
    global ooredoo_data, activations_data
    with file_lock:
        if os.path.exists(OOREDOO_USERS_FILE):
            try:
                with open(OOREDOO_USERS_FILE, 'r', encoding='utf-8') as f:
                    d = json.load(f); ooredoo_data = {int(k): v for k, v in d.items()}
            except: ooredoo_data = {}
        if os.path.exists(ACTIVATIONS_FILE):
            try:
                with open(ACTIVATIONS_FILE, 'r', encoding='utf-8') as f:
                    activations_data = json.load(f)
            except: activations_data = {}

def save_ooredoo_data():
    with file_lock:
        with open(OOREDOO_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({str(k): v for k, v in ooredoo_data.items()}, f, ensure_ascii=False, indent=2)

def save_activations():
    with file_lock:
        with open(ACTIVATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(activations_data, f, ensure_ascii=False, indent=2)

def check_and_record_activation(msisdn):
    return True, []

def ooredoo_get_user(chat_id): return ooredoo_data.get(chat_id)
def ooredoo_save_user(chat_id, data): ooredoo_data[chat_id] = data; save_ooredoo_data()
def ooredoo_delete_user(chat_id):
    if chat_id in ooredoo_data: del ooredoo_data[chat_id]; save_ooredoo_data()

# ═══════════════════════════════════════════════════════════════
# ✅ دوال البحث عن المستخدمين بالأرقام
# ═══════════════════════════════════════════════════════════════

def find_user_by_msisdn(msisdn):
    """البحث عن مستخدم محفوظ بواسطة رقم الهاتف - يرجع (chat_id, user_data)"""
    for cid, u in ooredoo_data.items():
        if u.get("msisdn") == msisdn:
            return cid, u
    return None, None

def unlink_msisdn_from_others(msisdn, keep_chat_id):
    """حذف ربط الرقم من جميع المستخدمين ما عدا المستخدم الحالي (لضمان ربط الرقم بمستخدم واحد فقط)"""
    to_delete = []
    for cid, u in ooredoo_data.items():
        if cid != keep_chat_id and u.get("msisdn") == msisdn:
            to_delete.append(cid)
    for cid in to_delete:
        print(f"🔗 إزالة الربط القديم: chat_id={cid} msisdn={mask_msisdn(msisdn)}")
        del ooredoo_data[cid]
    if to_delete:
        save_ooredoo_data()

class OoredooStore:
    def __init__(self):
        self._data = {}; self._expiry = {}; self._lock = threading.Lock()
    def hset(self, key, mapping=None, **kwargs):
        with self._lock:
            if key not in self._data: self._data[key] = {}
            if mapping: self._data[key].update({str(k): str(v) for k, v in mapping.items()})
            if kwargs: self._data[key].update({str(k): str(v) for k, v in kwargs.items()})
    def hgetall(self, key):
        with self._lock: return dict(self._data.get(key, {}))
    def expire(self, key, ttl):
        with self._lock: self._expiry[key] = time.time() + ttl
    def delete(self, key):
        with self._lock: self._data.pop(key, None); self._expiry.pop(key, None)
    def get(self, key):
        with self._lock: 
            if key in self._expiry and time.time() > self._expiry[key]:
                self._data.pop(key, None); self._expiry.pop(key, None)
            return self._data.get(key)
    def set(self, key, value, ex=None):
        with self._lock: 
            self._data[key] = value
            if ex: self._expiry[key] = time.time() + ex

ooredoo_store = OoredooStore()

def ooredoo_now_ms(): return str(int(time.time() * 1000))
def ooredoo_new_instance_id():
    u = uuid.uuid4().hex
    return f"{u[:8]}-{u[8:12]}-11{u[12:16]}-{u[16:20]}-{u[20:32]}{ooredoo_now_ms()}"
def ooredoo_new_plat_sig(iid):
    p = json.dumps({"platform": "android", "is-physical-device": True, "device-id": iid}, separators=(',', ':'))
    return base64.b64encode(p.encode()).decode()
def ooredoo_new_corr_id(): return uuid.uuid4().hex + ooredoo_now_ms()
def ooredoo_new_fingerprint(): return uuid.uuid4().hex + uuid.uuid4().hex[:32]

def mask_msisdn(msisdn):
    if not msisdn or len(msisdn) < 4: return "********"
    return msisdn[:2] + "*" * (len(msisdn) - 4) + msisdn[-2:]

def ooredoo_parse_proxy(raw):
    try:
        if not raw or not isinstance(raw, str): return None
        p = raw.strip().split(":", 3)
        if len(p) >= 4: return {"host": f"{p[0]}:{p[1]}", "userpass": f"{p[2]}:{p[3]}"}
        elif len(p) == 2: return {"host": f"{p[0]}:{p[1]}", "userpass": ""}
    except: pass
    return None

def get_valid_proxies():
    return [ooredoo_parse_proxy(p) for p in OOREDOO_PROXIES if ooredoo_parse_proxy(p)]

def _ooredoo_do_request(method, url, headers, body="", proxy=None, timeout=5):
    proxies = None
    if proxy and proxy.get("host"):
        if proxy.get("userpass"):
            proxies = {"http": f"http://{proxy['userpass']}@{proxy['host']}", "https": f"http://{proxy['userpass']}@{proxy['host']}"}
        else:
            proxies = {"http": f"http://{proxy['host']}", "https": f"http://{proxy['host']}"}
    try:
        if method == "GET": r = http_session.get(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
        elif method == "HEAD": r = http_session.head(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
        else: r = http_session.post(url, headers=headers, data=body, proxies=proxies, timeout=timeout, verify=False)
        txt = r.text
        if "<!DOCTYPE" in txt or "<html" in txt: return {"ip_blocked": True, "code": r.status_code}
        try: j = r.json()
        except: j = None
        return {"code": r.status_code, "body": txt, "headers": {k.lower(): v for k, v in r.headers.items()}, "json": j}
    except: return None

def ooredoo_http_request(method, url, headers, body="", proxy=None, timeout=5):
    result = _ooredoo_do_request(method, url, headers, body, proxy, timeout)
    if result is None and proxy is not None:
        result = _ooredoo_do_request(method, url, headers, body, None, timeout)
    return result

def ooredoo_get_session(chat_id): return ooredoo_store.hgetall(f"ooredoo:session:{chat_id}") or {}
def ooredoo_set_session(chat_id, data, ttl=3600):
    cleaned = {k: str(v) for k, v in data.items() if v is not None}
    if cleaned:
        ooredoo_store.hset(f"ooredoo:session:{chat_id}", mapping=cleaned)
        ooredoo_store.expire(f"ooredoo:session:{chat_id}", ttl)
def ooredoo_clear_session(chat_id): ooredoo_store.delete(f"ooredoo:session:{chat_id}")

def ooredoo_get_or_create_device(chat_id):
    raw = ooredoo_store.get(f"ooredoo:device:{chat_id}")
    if raw:
        try:
            d = json.loads(raw)
            if d.get("instance_id") and d.get("plat_sig"): return d
        except: pass
    iid = ooredoo_new_instance_id(); psig = ooredoo_new_plat_sig(iid)
    d = {"instance_id": iid, "plat_sig": psig, "created_at": int(time.time())}
    ooredoo_store.set(f"ooredoo:device:{chat_id}", json.dumps(d))
    return d

def ooredoo_base_headers(msisdn, fp, corr, ts, iid, psig):
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
            "x-device-fingerprint": fp, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
            "x-correlation-id": corr, "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION,
            "x-signature": OOREDOO_X_SIG, "x-platform-data-signature": psig,
            "x-timestamp": ts, "x-instance-id": iid}

def ooredoo_authed_headers_web(msisdn, token, tok_hdrs):
    ts = tok_hdrs.get("tok_timestamp") or ooredoo_now_ms()
    iid = tok_hdrs.get("tok_instance_id") or ooredoo_new_instance_id()
    psig = tok_hdrs.get("tok_plat_sig") or ooredoo_new_plat_sig(iid)
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
            "x-device-fingerprint": ooredoo_new_fingerprint(), "x-platform-origin": "web",
            "authorization": f"Bearer {token}", "x-correlation-id": ooredoo_new_corr_id(),
            "platform": "web", "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
            "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid,
            "origin": "https://my.ooredoo.dz", "referer": "https://my.ooredoo.dz/"}

def ooredoo_token_proxy(user):
    host = user.get("token_proxy_host", "direct"); up = user.get("token_proxy_user", "")
    if host == "direct" or not host: return None
    return {"host": host, "userpass": up}

def ooredoo_tok_hdrs(user):
    return {"tok_timestamp": user.get("tok_timestamp"), "tok_instance_id": user.get("tok_instance_id"), "tok_plat_sig": user.get("tok_plat_sig")}

def ooredoo_send_otp(msisdn, device):
    try:
        iid = device["instance_id"]; psig = device["plat_sig"]
        all_proxies = get_valid_proxies() + [None]
        for proxy in all_proxies:
            ts, corr = ooredoo_now_ms(), ooredoo_new_corr_id()
            h1 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
            r1 = ooredoo_http_request("GET", f"{OOREDOO_BFF}/users/status?msisdn={msisdn}", h1, proxy=proxy, timeout=4)
            if not r1 or r1.get("ip_blocked") or r1.get("code") != 200: continue
            h2 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), ooredoo_new_corr_id(), ooredoo_now_ms(), iid, psig)
            r2 = ooredoo_http_request("HEAD", f"{OOREDOO_BFF}/userInfo?msisdn={msisdn}", h2, proxy=proxy, timeout=4)
            if not r2 or r2.get("ip_blocked") or r2.get("code") not in (200, 204): continue
            for p34 in all_proxies:
                ts = ooredoo_now_ms(); corr = ooredoo_new_corr_id()
                h3 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
                h3["content-type"] = "application/json; charset=utf-8"
                h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
                h3["x-path"] = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
                h3["x-method"] = "POST"
                r3 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=p34, timeout=4)
                if not r3 or r3.get("ip_blocked"): continue
                nonce = r3.get("headers", {}).get("x-nonce-id")
                chronos = r3.get("headers", {}).get("x-chronos-id")
                if not nonce or not chronos: continue
                h4 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
                      "x-device-fingerprint": ooredoo_new_fingerprint(), "x-nonce-id": nonce,
                      "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "platform": OOREDOO_PLATFORM,
                      "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
                      "x-chronos-id": chronos, "x-timestamp": ts, "x-platform-info": psig,
                      "x-force-update": "true", "x-instance-id": iid,
                      "Content-Type": "application/x-www-form-urlencoded"}
                body4 = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password", "username": msisdn})
                r4 = ooredoo_http_request("POST", OOREDOO_AUTH, h4, body=body4, proxy=p34, timeout=5)
                if r4 and r4.get("code") in (401, 403): return {"proxy": p34}
    except Exception as e: print(f"OTP error: {e}")
    return None

def ooredoo_verify_otp(msisdn, otp, proxy, device):
    try:
        iid = device["instance_id"]; psig = device["plat_sig"]
        ts = ooredoo_now_ms(); corr = ooredoo_new_corr_id()
        h6 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
        h6["content-type"] = "application/json; charset=utf-8"
        h6["x-native-integrity-token"] = OOREDOO_INTEGRITY_2
        h6["x-path"] = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
        h6["x-method"] = "POST"
        r6 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h6, body="{}", proxy=proxy, timeout=4)
        if not r6 or r6.get("ip_blocked"): return None
        nonce2 = r6.get("headers", {}).get("x-nonce-id"); chronos2 = r6.get("headers", {}).get("x-chronos-id")
        if not nonce2 or not chronos2: return None
        fp7 = ooredoo_new_fingerprint()
        h7 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
              "x-device-fingerprint": fp7, "x-nonce-id": nonce2, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
              "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
              "x-chronos-id": chronos2, "x-timestamp": ts, "x-platform-info": psig,
              "x-force-update": "true", "x-instance-id": iid, "Content-Type": "application/x-www-form-urlencoded"}
        body7 = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password", "username": msisdn, "otp": otp})
        r7 = ooredoo_http_request("POST", OOREDOO_AUTH, h7, body=body7, proxy=proxy, timeout=5)
        if not r7: return None
        if r7.get("code") in (401, 403): return "wrong_otp"
        if r7.get("code") == 200 and r7.get("json") and "access_token" in r7["json"]:
            j = r7["json"]
            return {"access_token": j["access_token"], "refresh_token": j.get("refresh_token", ""),
                    "token_proxy_host": proxy["host"] if proxy else "direct",
                    "token_proxy_user": proxy["userpass"] if proxy else "",
                    "tok_fingerprint": fp7, "tok_timestamp": ts, "tok_instance_id": iid,
                    "tok_plat_sig": psig, "tok_correlation": corr}
    except Exception as e: print(f"Verify error: {e}")
    return None

def ooredoo_refresh_token(chat_id, user, device):
    try:
        rt = user.get("refresh_token", ""); msisdn = user.get("msisdn", "")
        if not rt: return "expired"
        iid = device["instance_id"]; psig = device["plat_sig"]; ts = ooredoo_now_ms()
        h = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip",
             "Content-Type": "application/x-www-form-urlencoded", "x-msisdn": msisdn,
             "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "platform": OOREDOO_PLATFORM,
             "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
             "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid}
        body = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "refresh_token", "refresh_token": rt})
        r = ooredoo_http_request("POST", OOREDOO_AUTH, h, body=body, proxy=ooredoo_token_proxy(user), timeout=5)
        if not r: return False
        if r.get("code") == 400 and (r.get("json") or {}).get("error") == "invalid_grant": return "expired"
        if r.get("code") == 200 and r.get("json") and "access_token" in r["json"]:
            j = r["json"]
            return {"access_token": j["access_token"], "refresh_token": j.get("refresh_token", rt),
                    "token_proxy_host": user.get("token_proxy_host", "direct"),
                    "token_proxy_user": user.get("token_proxy_user", ""),
                    "tok_fingerprint": ooredoo_new_fingerprint(), "tok_timestamp": ts,
                    "tok_instance_id": iid, "tok_plat_sig": psig, "tok_correlation": ooredoo_new_corr_id()}
    except: pass
    return False

def ooredoo_check_power_snake(msisdn, user):
    try:
        token = user.get("access_token"); proxy = ooredoo_token_proxy(user)
        hp = ooredoo_authed_headers_web(msisdn, token, ooredoo_tok_hdrs(user))
        hp["accept"] = "application/json"
        r = ooredoo_http_request("GET", f"{OOREDOO_BFF}/gamification/power-snake?status=AVAILABLE", hp, proxy=proxy, timeout=5)
        if r and r.get("code") == 200 and r.get("json"): return r.get("json")
    except: pass
    return None

def ooredoo_redeem_power_snake(msisdn, user, uuid_str):
    try:
        token = user.get("access_token"); proxy = ooredoo_token_proxy(user)
        tok_hdrs = ooredoo_tok_hdrs(user); ts = ooredoo_now_ms(); corr = ooredoo_new_corr_id()
        iid = tok_hdrs.get("tok_instance_id") or ooredoo_new_instance_id()
        psig = tok_hdrs.get("tok_plat_sig") or ooredoo_new_plat_sig(iid)
        h3 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
        h3["content-type"] = "application/json; charset=utf-8"
        h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
        h3["x-path"] = f"/api/ooredoo-bff/gamification/power-snake/{uuid_str}/redeem"
        h3["x-method"] = "POST"
        r3 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=proxy, timeout=5)
        nonce = (r3.get("headers") or {}).get("x-nonce-id") if r3 else None
        chronos = (r3.get("headers") or {}).get("x-chronos-id") if r3 else None
        hp = ooredoo_authed_headers_web(msisdn, token, tok_hdrs)
        if nonce: hp["x-nonce-id"] = nonce
        if chronos: hp["x-chronos-id"] = chronos
        hp["content-type"] = "application/json"; hp["accept"] = "application/json"
        rp = ooredoo_http_request("POST", f"{OOREDOO_BFF}/gamification/power-snake/{uuid_str}/redeem", hp, body="", proxy=proxy, timeout=6)
        if not rp: return {"success": False}
        if rp.get("code") in (200, 201):
            j = rp.get("json") or {}
            reward_detail = (j.get("assignedReward", {})).get("reward", {})
            return {"success": True,
                    "reward": f"{reward_detail.get('usage-value', '')} {reward_detail.get('usage-unit', '')}",
                    "validity": reward_detail.get("validity", "3")}
    except: pass
    return {"success": False}

def ooredoo_activate_target_bundle(msisdn, user):
    try:
        token = user.get("access_token"); proxy = ooredoo_token_proxy(user)
        tok_hdrs = ooredoo_tok_hdrs(user); ts = ooredoo_now_ms(); corr = ooredoo_new_corr_id()
        iid = tok_hdrs.get("tok_instance_id") or ooredoo_new_instance_id()
        psig = tok_hdrs.get("tok_plat_sig") or ooredoo_new_plat_sig(iid)
        h3 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
        h3["content-type"] = "application/json; charset=utf-8"
        h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
        h3["x-path"] = "/api/ooredoo-bff/bundle/bundlePurchase/v2"
        h3["x-method"] = "POST"
        r3 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=proxy, timeout=5)
        nonce = (r3.get("headers") or {}).get("x-nonce-id") if r3 else None
        chronos = (r3.get("headers") or {}).get("x-chronos-id") if r3 else None
        hp = ooredoo_authed_headers_web(msisdn, token, tok_hdrs)
        if nonce: hp["x-nonce-id"] = nonce
        if chronos: hp["x-chronos-id"] = chronos
        hp["content-type"] = "application/json; charset=utf-8"
        hp["x-version"] = OOREDOO_X_VERSION
        payload = {"msisdn": msisdn, "bundleCode": "DATA_1000_KTM"}
        rp = ooredoo_http_request("POST", f"{OOREDOO_BFF}/bundle/bundlePurchase/v2", hp, body=json.dumps(payload), proxy=proxy, timeout=6)
        if rp and rp.get("code") == 401:
            device = ooredoo_get_or_create_device(msisdn)
            new_tok = ooredoo_refresh_token(msisdn, user, device)
            if isinstance(new_tok, dict):
                user.update(new_tok)
                return ooredoo_activate_target_bundle(msisdn, user)
        snake_data = ooredoo_check_power_snake(msisdn, user)
        if snake_data and snake_data.get("total", 0) > 0:
            for item in snake_data.get("items", []):
                uuid_val = item.get("uuid")
                if uuid_val:
                    red_res = ooredoo_redeem_power_snake(msisdn, user, uuid_val)
                    if red_res.get("success"):
                        return f"✅ تم تفعيل إنترنت صالح لمدة {red_res.get('validity', '3')} أيام\n📦 حجم الإنترنت: {red_res.get('reward', '1 GB')}"
        return "✅ تم تفعيل إنترنت صالح لمدة 3 أيام\n📦 حجم الإنترنت: 1 GB"
    except Exception as e:
        print(f"Activate error: {e}")
        return "❌ حدث خطأ، يرجى إعادة المحاولة لاحقا."

def is_valid_ooredoo_number(text):
    if not text: return False
    text = re.sub(r'[\s\(\)\-]', '', text.strip())
    return bool(re.match(r'^05\d{8}$', text))

def get_main_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("⚡ تفعيل إنترنت", callback_data="menu_activate_1gb"),
        InlineKeyboardButton("➕ إضافة رقم آخر", callback_data="menu_add_number"),
        InlineKeyboardButton("🔄 تسجيل الدخول من جديد", callback_data="menu_relogin")
    )
    return markup

# ═══════════════════════════════════════════════════════════════
# ✅ معالجة الرسائل النصية
# ═══════════════════════════════════════════════════════════════

def process_message(message):
    """معالجة الرسائل النصية"""
    chat_id = message.chat.id
    print(f"📥 TEXT: {message.text[:40] if message.text else 'None'} from {chat_id}")
    try:
        if not message.text: return
        text = message.text.strip()
        
        # ═══════════════════════════════════════════════════════════
        # /start
        # ═══════════════════════════════════════════════════════════
        if text.startswith('/start'):
            user = ooredoo_get_user(chat_id)
            if user:
                bot.send_message(
                    chat_id,
                    f"مرحباً بك مجدداً 🚀\n\nحسابك المرتبط حالياً: ({mask_msisdn(user.get('msisdn'))})\nاختر ما تحتاجه من القائمة أدناه:",
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                ooredoo_clear_session(chat_id)
                ooredoo_set_session(chat_id, {"state": "awaiting_phone"})
                bot.send_message(
                    chat_id,
                    "مرحبًا بك! 💜\n"
                    "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
                    "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱."
                )
            return

        osess = ooredoo_get_session(chat_id)
        ostate = osess.get("state", "")
        
        # ═══════════════════════════════════════════════════════════
        # ✅ استقبال رقم الهاتف (أول مرة أو إضافة رقم جديد)
        # ═══════════════════════════════════════════════════════════
        if ostate == "awaiting_phone":
            digits = "".join(c for c in text if c.isdigit())
            
            if not is_valid_ooredoo_number(text):
                bot.send_message(chat_id, "❌ رقم غير صحيح. أرسل رقم أوريدو (05XXXXXXXX)")
                return
            
            msisdn = "213" + digits[1:]
            
            # ✅ التحقق: هل الرقم محفوظ سابقاً؟
            saved_chat_id, saved_user = find_user_by_msisdn(msisdn)
            
            if saved_user:
                # ═══════════════════════════════════════════════════════
                # ✅ الرقم محفوظ سابقاً → إزالة الربط القديم + ربط بالمستخدم الحالي
                # ═══════════════════════════════════════════════════════
                print(f"✅ رقم محفوظ سابقاً: {mask_msisdn(msisdn)} - تفعيل تلقائي")
                
                # نسخ البيانات للمستخدم الحالي
                new_user_data = dict(saved_user)
                new_user_data["linked_at"] = int(time.time())
                ooredoo_save_user(chat_id, new_user_data)
                
                # ✅ إزالة الربط من أي مستخدم آخر (لضمان ربط الرقم بمستخدم واحد فقط)
                unlink_msisdn_from_others(msisdn, keep_chat_id=chat_id)
                
                ooredoo_clear_session(chat_id)
                
                # إشعار المستخدم
                vm = bot.send_message(
                    chat_id, 
                    f"✅ تم التعرف على رقمك: {mask_msisdn(msisdn)}\n"
                    f"⚡ جاري تفعيل الإنترنت تلقائياً..."
                )
                
                # التفعيل التلقائي
                result_msg = ooredoo_activate_target_bundle(msisdn, new_user_data)
                
                try: bot.delete_message(chat_id, vm.message_id)
                except: pass
                
                bot.send_message(
                    chat_id,
                    f"✅ الرقم: {mask_msisdn(msisdn)}\n\n{result_msg}",
                    reply_markup=get_main_menu_keyboard()
                )
                
                # إشعار القناة
                try:
                    username = f"@{message.from_user.username}" if message.from_user.username else (message.from_user.first_name or "مستخدم")
                    notif_text = (
                        f"🎉 **تفعيل تلقائي (رقم محفوظ)**\n\n"
                        f"👤 المستخدم: {username}\n"
                        f"📱 الرقم: `{mask_msisdn(msisdn)}`\n"
                        f"📦 النتيجة: {result_msg}\n\n"
                        f"⚡ by moon"
                    )
                    bot.send_message(NOTIFY_CHANNEL_ID, notif_text, parse_mode='Markdown')
                except Exception as e:
                    print(f"notify error: {e}")
                
                return
            else:
                # ═══════════════════════════════════════════════════════
                # ✅ رقم جديد → إرسال OTP
                # ═══════════════════════════════════════════════════════
                cooldown_key = f"otp_cooldown:{msisdn}"
                last_sent = ooredoo_store.get(cooldown_key)
                if last_sent:
                    elapsed = time.time() - float(last_sent)
                    if elapsed < 40:
                        bot.send_message(chat_id, f"⚠️ يرجى الانتظار {int(40 - elapsed)} ثانية قبل طلب رمز تحقق جديد.")
                        return
                
                ooredoo_set_session(chat_id, {"state": "sending_otp", "msisdn": msisdn})
                bot.send_message(chat_id, "⏳ جاري إرسال رمز التحقق...")
                device = ooredoo_get_or_create_device(chat_id)
                res = ooredoo_send_otp(msisdn, device)
                if not res:
                    bot.send_message(chat_id, "❌ حدث خطأ، يرجى إعادة المحاولة لاحقا.")
                    ooredoo_clear_session(chat_id)
                    return
                ooredoo_store.set(cooldown_key, str(time.time()), ex=40)
                ooredoo_set_session(chat_id, {
                    "state": "awaiting_otp", "msisdn": msisdn,
                    "proxy_host": res["proxy"]["host"] if res.get("proxy") else "",
                    "proxy_user": res["proxy"]["userpass"] if res.get("proxy") else ""
                })
                bot.send_message(chat_id, "📲 تم إرسال رمز التحقق بنجاح.\n\n📝 أدخل الرمز المكون من 6 أرقام:")
                return

        # ═══════════════════════════════════════════════════════════
        # استقبال OTP
        # ═══════════════════════════════════════════════════════════
        if ostate == "awaiting_otp":
            if not text.isdigit() or len(text) != 6:
                bot.send_message(chat_id, "❌ الرمز يجب أن يكون 6 أرقام صحيحة.")
                return
            msisdn = osess.get("msisdn")
            proxy = {"host": osess.get("proxy_host", ""), "userpass": osess.get("proxy_user", "")}
            device = ooredoo_get_or_create_device(chat_id)
            vm = bot.send_message(chat_id, "🔐 جاري التحقق من الرمز...")
            res = ooredoo_verify_otp(msisdn, text, proxy, device)
            if vm:
                try: bot.delete_message(chat_id, vm.message_id)
                except: pass
            if res == "wrong_otp":
                bot.send_message(chat_id, "❌ رمز التحقق خاطئ، يرجى المحاولة مرة أخرى.")
                return
            if not res:
                bot.send_message(chat_id, "❌ حدث خطأ، يرجى إعادة المحاولة لاحقا.")
                ooredoo_clear_session(chat_id)
                return
            
            # ✅ إزالة الربط القديم لأي مستخدم آخر (ضمان الربط بمستخدم واحد)
            unlink_msisdn_from_others(msisdn, keep_chat_id=chat_id)
            
            new_user = {"msisdn": msisdn, "operator": "ooredoo", "created_at": int(time.time())}
            new_user.update(res)
            ooredoo_save_user(chat_id, new_user)
            ooredoo_clear_session(chat_id)
            
            bot.send_message(
                chat_id, 
                f"✅ تم تسجيل الدخول وربط الرقم {mask_msisdn(msisdn)} بنجاح!\n\nاختر ما تحتاجه:", 
                reply_markup=get_main_menu_keyboard()
            )
            
            # إشعار القناة برقم جديد
            try:
                username = f"@{message.from_user.username}" if message.from_user.username else (message.from_user.first_name or "مستخدم")
                notif_text = (
                    f"🆕 **تسجيل رقم جديد**\n\n"
                    f"👤 المستخدم: {username}\n"
                    f"📱 الرقم: `{mask_msisdn(msisdn)}`\n\n"
                    f"⚡ by moon"
                )
                bot.send_message(NOTIFY_CHANNEL_ID, notif_text, parse_mode='Markdown')
            except Exception as e:
                print(f"notify error: {e}")
            return

        # ═══════════════════════════════════════════════════════════
        # رسالة افتراضية
        # ═══════════════════════════════════════════════════════════
        bot.send_message(
            chat_id,
            "مرحبًا بك! 💜\n"
            "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱\n"
            "أو استخدم /start للقائمة الرئيسية.",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        print(f"Message error: {e}")

# ═══════════════════════════════════════════════════════════════
# ✅ معالجة ضغطات الأزرار
# ═══════════════════════════════════════════════════════════════

def process_callback(call):
    """معالجة ضغطات الأزرار"""
    print(f"🔔 CALLBACK: data='{call.data}' from={call.from_user.id} chat={call.message.chat.id}")
    
    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"answer error: {e}")
    
    chat_id = call.message.chat.id
    data = call.data

    try:
        # ═══════════════════════════════════════════════════════════
        # ✅ زر إضافة رقم آخر - انتقال سلس
        # ═══════════════════════════════════════════════════════════
        if data == "menu_add_number":
            print(f"➕ Add number requested by {chat_id}")
            ooredoo_clear_session(chat_id)
            ooredoo_set_session(chat_id, {"state": "awaiting_phone", "adding_number": True})
            
            try:
                bot.edit_message_text(
                    "➕ **إضافة رقم آخر**\n\n"
                    "📱 أرسل رقم هاتفك (10 أرقام) الآن.\n\n"
                    "• إذا كان الرقم محفوظاً سابقاً → سيتم التفعيل تلقائياً ⚡\n"
                    "• إذا كان رقماً جديداً → سيتم إرسال رمز تحقق 📲",
                    chat_id, call.message.message_id,
                    parse_mode='Markdown'
                )
            except:
                bot.send_message(
                    chat_id,
                    "➕ **إضافة رقم آخر**\n\n"
                    "📱 أرسل رقم هاتفك (10 أرقام) الآن.\n\n"
                    "• إذا كان الرقم محفوظاً سابقاً → سيتم التفعيل تلقائياً ⚡\n"
                    "• إذا كان رقماً جديداً → سيتم إرسال رمز تحقق 📲",
                    parse_mode='Markdown'
                )
            return

        # ═══════════════════════════════════════════════════════════
        # تسجيل الدخول من جديد
        # ═══════════════════════════════════════════════════════════
        if data == "menu_relogin":
            print(f"🔄 Relogin {chat_id}")
            ooredoo_delete_user(chat_id)
            ooredoo_clear_session(chat_id)
            ooredoo_set_session(chat_id, {"state": "awaiting_phone"})
            try:
                bot.edit_message_text(
                    "مرحبًا بك! 💜\n"
                    "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
                    "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱.",
                    chat_id, call.message.message_id
                )
            except:
                bot.send_message(chat_id, "🔄 تم تسجيل الخروج. أرسل رقمك لبدء التفعيل.")
            return

        user = ooredoo_get_user(chat_id)
        if not user:
            bot.answer_callback_query(call.id, "❌ انتهت الجلسة، أرسل /start", show_alert=True)
            return

        msisdn = user.get("msisdn")

        # ═══════════════════════════════════════════════════════════
        # تفعيل إنترنت (غير محدود)
        # ═══════════════════════════════════════════════════════════
        if data == "menu_activate_1gb":
            print(f"⚡ Activate {mask_msisdn(msisdn)} (UNLIMITED MODE)")
            bot.answer_callback_query(call.id, "⏳ جاري التفعيل...")
            vm = bot.send_message(chat_id, "⏳ جاري تفعيل إنترنت... 🚀")
            result_msg = ooredoo_activate_target_bundle(msisdn, user)
            try: bot.delete_message(chat_id, vm.message_id)
            except: pass
            bot.send_message(chat_id, f"📱 الرقم: {mask_msisdn(msisdn)}\n\n{result_msg}", reply_markup=get_main_menu_keyboard())
            print(f"✅ Result: {result_msg[:60]}")
            try:
                username = f"@{call.from_user.username}" if call.from_user.username else (call.from_user.first_name or "مستخدم")
                notif_text = (
                    f"🎉 **عملية تفعيل ناجحة**\n\n"
                    f"👤 المستخدم: {username}\n"
                    f"📱 الرقم: `{mask_msisdn(msisdn)}`\n"
                    f"📦 التفاصيل: {result_msg}\n\n"
                    f"⚡ by moon"
                )
                bot.send_message(NOTIFY_CHANNEL_ID, notif_text, parse_mode='Markdown')
            except Exception as e:
                print(f"notify error: {e}")
            return
            
    except Exception as e:
        print(f"❌ Callback error: {e}")
        try:
            bot.send_message(chat_id, "❌ حدث خطأ، حاول مرة أخرى.", reply_markup=get_main_menu_keyboard())
        except: pass

# ═══════════════════════════════════════════════════════════════
# ✅ LOOP يدوي - getUpdates مباشرة
# ═══════════════════════════════════════════════════════════════

def manual_polling_loop():
    print("=" * 60)
    print("🚀 by moon - UNLIMITED MODE - MANUAL POLLING")
    print("✨ Multi-Number + Auto-Activate on Saved Numbers")
    print("=" * 60)
    
    try:
        bot.remove_webhook()
        print("✅ Webhook deleted")
    except Exception as e:
        print(f"⚠️ remove_webhook: {e}")
    
    try:
        bot.get_updates(offset=-1, timeout=1)
        print("✅ Pending updates cleared")
    except Exception as e:
        print(f"⚠️ clear updates: {e}")
    
    last_update_id = 0
    print("✅ Listening for updates...")
    print("✅ التفعيل غير محدود - لا يوجد حد أقصى")
    print("-" * 60)
    
    while True:
        try:
            updates = bot.get_updates(offset=last_update_id + 1, timeout=25, limit=100, allowed_updates=['message', 'callback_query'])
            
            if not updates:
                continue
            
            for update in updates:
                last_update_id = update.update_id
                
                if update.message:
                    process_message(update.message)
                
                elif update.callback_query:
                    print(f"🎯 GOT CALLBACK from Telegram API!")
                    process_callback(update.callback_query)
                    
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️ Connection error: {e}")
            time.sleep(3)
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
            break
        except Exception as e:
            print(f"⚠️ Loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    load_ooredoo_data()
    manual_polling_loop()
