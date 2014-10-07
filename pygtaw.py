# -*- coding: utf-8 -*-
import requests
from langs import langs

class Client(object):
    def __init__(self, api_key):
        self._payload = {'key': api_key}
        self._url = 'https://www.googleapis.com/language/translate/v2?'
        self._response = None
        self._source = None

    def build_translation_request(self, query, target, source):
        payload = dict(q=query, target=target, **self._payload)
        if source:
            payload['source'] = source
        return payload

    def translate(self, query, target='Spanish', source=None):
        query.decode(encoding='utf-8')
        payload = self.build_translation_request(query, langs[target], langs.get(source, None))
        r = requests.get(self._url, params=payload)
        self._source = source
        self._response = r.json()['data']['translations'][0]

    @property
    def source_language_detected(self):
        try:
            return self._response['detectedSourceLanguage']
        except KeyError:
            return 'No detected source language, source provided by user: {}'.format(self._source)
    
    @property
    def translated_text(self):
        return self._response['translatedText']