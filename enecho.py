"""資源エネルギー庁（enecho.meti.go.jp）からのファイル取得。

このホストは CloudFront + AWS WAF の challenge action で保護されており、
短時間に続けて叩くと HTTP 202 と JavaScript の検証ページが返る。
challenge は時間で解けるので、202 が返ったら間隔を空けて取り直す。
"""

import logging
import time
from pathlib import Path

from curl_cffi import requests

logger = logging.getLogger("pipelines")

BASE_URL = "https://www.enecho.meti.go.jp"

# challenge を受けたときの待機間隔（秒）と試行回数。統計表が増えて 1 ビルドの
# 取得数が 30 を超えるようになり、ほぼ全ファイルが challenge に当たる。
RETRY_INTERVAL_SEC = 150.0
MAX_ATTEMPTS = 12

# 連続取得の最低間隔（秒）。challenge を誘発しないよう間隔を空ける。
FETCH_INTERVAL_SEC = 25.0

_last_fetch = 0.0


def _throttle() -> None:
    global _last_fetch
    wait = FETCH_INTERVAL_SEC - (time.monotonic() - _last_fetch)
    if wait > 0:
        time.sleep(wait)
    _last_fetch = time.monotonic()


def _get(path: str) -> requests.Response:
    """WAF の challenge が解けるまで間隔を空けて取り直す。"""
    url = path if path.startswith("http") else BASE_URL + path
    for attempt in range(MAX_ATTEMPTS):
        _throttle()
        # ブラウザ以外の TLS クライアントは遮断されるため TLS 指紋を模倣する。
        resp = requests.get(url, impersonate="chrome", timeout=120)
        if resp.headers.get("x-amzn-waf-action") != "challenge":
            resp.raise_for_status()
            return resp
        logger.info(
            f"  WAF challenge ({attempt + 1}/{MAX_ATTEMPTS}): "
            f"{RETRY_INTERVAL_SEC:.0f}s 待機して再取得 {url}"
        )
        time.sleep(RETRY_INTERVAL_SEC)
    raise RuntimeError(f"WAF challenge が解けなかった: {url}")


def fetch_text(path: str) -> str:
    """HTML ページを取得する。"""
    return _get(path).text


def fetch_file(path: str, dest: Path) -> None:
    """Excel などのバイナリを取得して保存する。

    challenge ページが xlsx として保存されるのを防ぐため、ZIP の
    マジックナンバー（xlsx は ZIP）を確認する。
    """
    resp = _get(path)
    if not resp.content.startswith(b"PK"):
        raise RuntimeError(f"xlsx ではない応答が返った: {path}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
