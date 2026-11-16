"""経済産業省（www.meti.go.jp）からのファイル取得。

このホストは CloudFront + AWS WAF の challenge action で保護されており、
短時間に続けて叩くと HTTP 202 と JavaScript の検証ページが返る。
challenge は時間で解けるので、202 が返ったら間隔を空けて取り直す。
"""

import hashlib
import logging
import time
from datetime import UTC, datetime
from pathlib import Path

from curl_cffi import requests

logger = logging.getLogger("pipelines")

# challenge を受けたときの待機間隔（秒）と試行回数。
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


def _get(url: str) -> requests.Response:
    """WAF の challenge が解けるまで間隔を空けて取り直す。"""
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


def fetch_file(url: str, dest: Path) -> None:
    """Excel などのバイナリを取得して保存する。

    challenge ページが xlsx として保存されるのを防ぐため、ZIP の
    マジックナンバー（xlsx は ZIP）を確認する。
    """
    resp = _get(url)
    if not resp.content.startswith(b"PK"):
        raise RuntimeError(f"xlsx ではない応答が返った: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)


def fetch_pdf(url: str, dest: Path) -> dict | None:
    """計画・通知等の PDF を取得して保存し、shared/fetch.py の fetch_file と同じ形の行を返す。

    shared/review_plans.py の download_plans に fetch として渡す。4xx（リンク切れなど）は None を返し、
    PDF かどうかは download_plans が確かめる。
    """
    try:
        resp = _get(url)
    except requests.exceptions.HTTPError as error:
        if error.response is not None and error.response.status_code < 500:
            return None
        raise
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return {
        "url": url,
        "sha256": hashlib.sha256(resp.content).hexdigest(),
        "bytes": len(resp.content),
        "media_type": resp.headers.get("Content-Type", "").split(";")[0].strip()
        or None,
        "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "etag": resp.headers.get("ETag"),
        "last_modified": resp.headers.get("Last-Modified"),
    }
