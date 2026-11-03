#!/usr/bin/env python3
"""Only probe explicitly enabled PUBLIC HTTPS URLs; export a safe static snapshot.

Runs in GitHub Actions or locally. Not a replacement for internal monitoring.
No redirects, localhost, private IP literals, or unapproved DNS hostnames.
"""
from __future__ import annotations
from datetime import datetime, timezone
import ipaddress
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import build_opener, Request, HTTPRedirectHandler

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/public-endpoints.json'
DEST = ROOT / 'site/lab/status/status.json'

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def valid_public_url(url, allowed_domain):
    try:
        u = urlsplit(url)
        host = (u.hostname or '').lower().rstrip('.')
        if u.scheme != 'https' or u.username is not None or u.password is not None:
            return False
        if not host or not (host == allowed_domain or host.endswith('.' + allowed_domain)):
            return False
        try:
            ipaddress.ip_address(host)
            return False
        except ValueError:
            pass
        if u.port not in (None, 443):
            return False
        if u.query or u.fragment:
            return False
        return True
    except (ValueError, TypeError):
        return False


def check(url):
    opener = build_opener(NoRedirect)
    request = Request(url, headers={'User-Agent': 'Rohan-Lab-PublicStatus/1.0', 'Accept': 'text/html,application/json'}, method='GET')
    try:
        with opener.open(request, timeout=8) as response:
            code = response.status
            return 'up' if 200 <= code < 300 else 'unexpected_response'
    except HTTPError as exc:
        if exc.code in (401, 403):
            return 'restricted'
        if 300 <= exc.code < 400:
            return 'redirect'
        return 'down'
    except (URLError, TimeoutError, OSError):
        return 'down'


def main():
    cfg = json.loads(CONFIG.read_text())
    allowed_domain = cfg['allowed_domain']
    if allowed_domain != 'rohanmarar.com':
        raise ValueError('Hard-coded ownership guard: only rohanmarar.com hosts allowed')
    checks = []
    for raw in cfg['checks']:
        name = str(raw['name'])[:80]
        enabled = raw.get('enabled') is True
        stamp = None
        state = 'not_configured'
        if enabled:
            stamp = now()
            url = raw.get('url', '')
            state = check(url) if valid_public_url(url, allowed_domain) else 'invalid_configuration'
        checks.append({'name': name, 'enabled': enabled, 'state': state, 'checked_at': stamp})
    data = {'generated_at': now(), 'checks': checks}
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(data, indent=2) + '\n')
    print(f'Wrote {DEST.relative_to(ROOT)}, {sum(x["enabled"] for x in checks)} enabled checks')

if __name__ == '__main__':
    main()
