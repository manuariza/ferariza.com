import importlib.util
import io
import os
from pathlib import Path
import ssl
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('tls_social', Path(__file__).with_name('publish-articles.py'))
social = importlib.util.module_from_spec(spec)
spec.loader.exec_module(social)


class TrustTests(unittest.TestCase):
    def test_buffer_uses_patched_ca_bundle(self):
        with patch.dict(os.environ, {'BUFFER_API_KEY': 'offline-placeholder'}), patch.object(social, 'urlopen', return_value=io.BytesIO(b'{"data":{}}')) as network:
            social.api('query { account { id } }')
        ctx = network.call_args.kwargs['context']
        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(ctx.check_hostname)
        self.assertNotIn('emsign ecc root ca - g3', str(ctx.get_ca_certs()).lower())
