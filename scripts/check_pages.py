"""Validate the static Pages entry point, relative assets and bundled data."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'app'


class Assets(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        asset = attrs.get('src') if tag == 'script' else (
            attrs.get('href') if tag == 'link' else None
        )
        if asset:
            parsed = urlsplit(asset)
            assert not parsed.scheme and not parsed.netloc, f'External asset: {asset}'
            assert not parsed.path.startswith('/'), f'Asset breaks project Pages path: {asset}'
            assert (SITE / parsed.path).is_file(), f'Missing asset: {asset}'


def main():
    Assets().feed((SITE / 'index.html').read_text(encoding='utf-8'))
    source = (SITE / 'data.js').read_text(encoding='utf-8').strip()
    prefix = 'window.ANI_DATA = '
    assert source.startswith(prefix) and source.endswith(';'), 'Invalid data bundle'
    data = json.loads(source[len(prefix):-1])
    assert data, 'Dataset is empty'
    required = {'id', 'year', 'office', 'group', 'end', 'status', 'progress'}
    assert all(required <= row.keys() for row in data), 'Dataset fields missing'
    assert (SITE / '.nojekyll').is_file(), 'Missing .nojekyll'
    print(f'Pages validation passed: entry point, relative assets, {len(data)} records.')


if __name__ == '__main__':
    main()
