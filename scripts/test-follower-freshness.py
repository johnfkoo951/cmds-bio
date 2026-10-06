#!/usr/bin/env python3
"""Offline regression checks for partial collection and independent content dates."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / 'scripts/refresh-followers.sh').read_text()
BLOCKS = re.findall(r"<<'PY'\n(.*?)\nPY", SCRIPT, re.S)

class FreshnessTests(unittest.TestCase):
    def test_partial_and_failed_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {'asOf': '2026-01-01', 'platforms': [
                {'id': 'x', 'label': 'X', 'count': 10, 'display': '10', 'checkedAt': '2026-01-01'},
                {'id': 'linkedin', 'label': 'LinkedIn', 'count': 20, 'display': '20', 'checkedAt': '2026-01-01'}]}
            path = root / 'followers.json'
            path.write_text(json.dumps(data))
            page = root / 'index.html'
            page.write_text((ROOT / 'index.html').read_text())
            content_date = re.search(r'<time id="pageUpdated".*?</time>', page.read_text()).group()
            subprocess.run([sys.executable, '-c', BLOCKS[0], str(path), '', '11', '', '', '', ''], check=True, capture_output=True)
            result = json.loads(path.read_text())
            self.assertEqual(result['platforms'][0]['count'], 11)
            self.assertEqual(result['platforms'][0]['status'], 'verified')
            self.assertEqual(result['platforms'][1]['checkedAt'], '2026-01-01')
            self.assertEqual(result['platforms'][1]['status'], 'retained')
            subprocess.run([sys.executable, '-c', BLOCKS[1], str(path), str(page)], check=True, capture_output=True)
            self.assertIn(content_date, page.read_text())
            self.assertIn('previous count retained', page.read_text())
            verified_date = result['platforms'][0]['checkedAt']
            subprocess.run([sys.executable, '-c', BLOCKS[0], str(path), '', '', '', '', '', ''], check=True, capture_output=True)
            result = json.loads(path.read_text())
            self.assertEqual(result['platforms'][0]['count'], 11)
            self.assertEqual(result['platforms'][0]['checkedAt'], verified_date)
            self.assertTrue(all(p['status'] == 'retained' for p in result['platforms']))

if __name__ == '__main__':
    unittest.main()
