import json
import re
import sys
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/lab'
sys.path.insert(0, str(ROOT / 'tools'))
from check_status import valid_public_url

class RefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        if tag in ('a', 'link', 'script', 'img'):
            for name, val in attrs:
                if name in ('href', 'src') and val:
                    self.urls.append(val)

class SiteTests(unittest.TestCase):
    def test_home_and_public_pages(self):
        for f in ('index.html','status/index.html','demos/index.html','docs/index.html',
                  'docs/architecture/index.html','docs/projects/ml-platform/index.html',
                  'docs/projects/thermostat/index.html','docs/projects/observability/index.html'):
            self.assertTrue((SITE/f).is_file(), f)

    def test_all_relative_links_exist(self):
        pages = list(SITE.rglob('*.html'))
        self.assertGreaterEqual(len(pages), 10)
        for page in pages:
            parser=RefParser()
            parser.feed(page.read_text(encoding='utf-8'))
            for link in parser.urls:
                parsed=urlsplit(link)
                if parsed.scheme or link.startswith(('#','//','mailto:')):
                    continue
                target=(page.parent / unquote(parsed.path)).resolve()
                if target.is_dir():target=target/'index.html'
                self.assertTrue(target.exists(), f'Broken link: {page.relative_to(ROOT)} -> {link}')
                self.assertTrue(target.is_relative_to(SITE), f'Link escapes deployment: {link}')

    def test_safe_endpoint_validation(self):
        good=['https://lab.rohanmarar.com/', 'https://docs.rohanmarar.com/a']
        bad=['http://lab.rohanmarar.com', 'https://127.0.0.1/',
             'https://rohanmarar.com.evil.test/', 'https://localhost/',
             'https://user:pass@lab.rohanmarar.com/', 'https://bad.rohanmarar.com:8080/',
             'https://demo.rohanmarar.com/?token=secret', 'file:///etc/passwd']
        for url in good:self.assertTrue(valid_public_url(url,'rohanmarar.com'),url)
        for url in bad:self.assertFalse(valid_public_url(url,'rohanmarar.com'),url)

    def test_status_endpoints_are_public_and_truthful(self):
        cfg=json.loads((ROOT/'config/public-endpoints.json').read_text())
        public=json.loads((SITE/'status/status.json').read_text())
        self.assertEqual(len(cfg['checks']),len(public['checks']))
        for original, result in zip(cfg['checks'], public['checks']):
            self.assertEqual(original['name'],result['name'])
            self.assertEqual(bool(original['enabled']),bool(result['enabled']))
            if original['enabled']:
                self.assertTrue(valid_public_url(original['url'], 'rohanmarar.com'), original['url'])
            else:
                self.assertEqual(result['state'], 'not_configured')

    def test_showcase_matches_public_thermostat_story(self):
        home = (SITE/'index.html').read_text(encoding='utf-8')
        js = (SITE/'assets/app.js').read_text(encoding='utf-8')
        thermostat = (SITE/'docs/projects/thermostat/index.html').read_text(encoding='utf-8')
        self.assertIn('Buffy', home)
        self.assertIn('buffy-dashboard.webp', home)
        self.assertTrue((SITE/'assets/buffy-dashboard.webp').is_file())
        self.assertTrue((SITE/'assets/architecture.svg').is_file())
        self.assertIn('rohanmarar.substack.com/p/the-thermostat-wars-revenge-of-the', thermostat)
        for value in ('68.5', '69.5', '72', '0.2', '0.4'):
            self.assertIn(value, js)
        self.assertNotIn('sanitized', home.lower())
        self.assertNotIn('sanitized', thermostat.lower())

    def test_demo_link_requires_https(self):
        js=(SITE/'demos/config.js').read_text()
        if re.search(r'enabled:\s*true', js):
            match = re.search(r'url:\s*[\"\'](https://[^\"\']+)',js)
            self.assertIsNotNone(match, 'Enabled demo must specify HTTPS URL')
            self.assertTrue(valid_public_url(match.group(1),'rohanmarar.com'))
        else:
            self.assertIn('enabled: false',js)

if __name__ == '__main__':unittest.main()
