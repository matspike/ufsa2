from __future__ import annotations

import hashlib
from pathlib import Path


def _cache_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def fetch(
    url: str, cache_dir: Path, offline: bool = True, timeout: int = 10
) -> Path | None:
    """Fetch a URL with offline-first caching.

    - If offline is True, return cached file if present; otherwise None.
    - If offline is False, attempt to download and store in cache, then return path.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = _cache_key(url)
    path = cache_dir / f"{key}.html"
    if path.exists():
        return path
    if offline:
        return None
    try:
        import urllib.request

        with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310
            content = resp.read()
    except Exception:
        return None
    else:
        path.write_bytes(content)
        return path


def pin(url: str, cache_dir: Path) -> str | None:
    """Return the current cache key for a URL if cached; otherwise None."""
    key = _cache_key(url)
    path = cache_dir / f"{key}.html"
    if path.exists():
        return key
    return None


def verify(url: str, cache_dir: Path, key: str) -> bool:
    """Verify the cache content for URL matches the given key and exists."""
    expected = cache_dir / f"{key}.html"
    return expected.exists() and _cache_key(url) == key


def graphql_fetch(
    url: str,
    query: str,
    cache_dir: Path,
    offline: bool = True,
    timeout: int = 10,
) -> Path | None:
    """Fetch a GraphQL query result with offline-first caching.

    - Cache key is sha256(url + "\n" + query) with .json suffix.
    - If offline and cached present, return path; else None.
    - If online, perform HTTP POST with JSON body {"query": query} and cache the response.
    """
    import json as _json

    cache_dir.mkdir(parents=True, exist_ok=True)
    key_src = f"{url}\n{query}"
    key = hashlib.sha256(key_src.encode("utf-8")).hexdigest()
    path = cache_dir / f"{key}.json"
    if path.exists():
        return path
    if offline:
        return None
    try:
        import urllib.request

        payload = _json.dumps({"query": query}).encode("utf-8")
        req = urllib.request.Request(  # noqa: S310
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            content = resp.read()
    except Exception:
        return None
    else:
        path.write_bytes(content)
        return path
