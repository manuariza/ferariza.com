import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('social', Path(__file__).with_name('publish-articles.py'))
social = importlib.util.module_from_spec(spec)
spec.loader.exec_module(social)
URL = 'https://www.eldebate.com/test.html'
ARTICLE = {'publication': 'El Debate', 'url': URL, 'date': '2026-09-30'}

class SocialTests(unittest.TestCase):
    def test_baseline_never_calls_buffer(self):
        with patch.object(social, 'api') as api:
            social.publish({'articles': {URL: {'status': 'baseline'}}}, {URL: ARTICLE}, 'channel')
            api.assert_not_called()

    def setup_api(self, existing=(), mutation=None):
        responses = [ {'account': {'organizations': [{'id': 'org'}]}},
                     {'channels': [{'id': 'channel', 'name': 'ferariza_', 'service': 'twitter',
                                    'isDisconnected': False, 'isLocked': False, 'isQueuePaused': False}]} ]
        if mutation is not None:
            responses.append(mutation)
        return patch.object(social, 'api', side_effect=responses)

    def test_reconciles_existing_post_without_mutation(self):
        state = {'articles': {URL: {'status': 'attempting'}}}
        with self.setup_api(), patch.object(social, 'existing_posts', return_value=[
                {'id': 'post', 'text': social.message(ARTICLE), 'status': 'sent'}]), patch.object(social, 'save'):
            social.publish(state, {URL: ARTICLE}, 'channel')
        self.assertEqual(state['articles'][URL]['bufferPostId'], 'post')

    def test_uncertain_result_never_blindly_retries(self):
        with self.setup_api(), patch.object(social, 'existing_posts', return_value=[]), patch.object(social, 'save'):
            with self.assertRaisesRegex(RuntimeError, 'Uncertain'):
                social.publish({'articles': {URL: {'status': 'attempting'}}}, {URL: ARTICLE}, 'channel')

    def test_persists_intent_before_post_and_records_success(self):
        state = {'articles': {}}
        events = []
        def save(s, persist):
            events.append(s['articles'][URL]['status'])
        with self.setup_api(mutation={'createPost': {'post': {'id': 'post'}}}) as api, \
                patch.object(social, 'existing_posts', return_value=[]), patch.object(social, 'save', side_effect=save):
            social.publish(state, {URL: ARTICLE}, 'channel')
        self.assertEqual(events, ['attempting', 'submitted'])
        self.assertIn('mode: shareNow', api.call_args.args[0])

    def test_rejection_remains_retryable(self):
        state = {'articles': {}}
        with self.setup_api(mutation={'createPost': {'message': 'Queue full'}}), \
                patch.object(social, 'existing_posts', return_value=[]), patch.object(social, 'save'):
            with self.assertRaisesRegex(RuntimeError, 'rejected'):
                social.publish(state, {URL: ARTICLE}, 'channel')
        self.assertEqual(state['articles'][URL]['status'], 'retry')
