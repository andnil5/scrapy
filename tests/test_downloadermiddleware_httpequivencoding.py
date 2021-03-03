import unittest

from scrapy.downloadermiddlewares.httpequivencoding import HttpEquivEncodingMiddleware
from scrapy.exceptions import NotConfigured
from scrapy.utils.test import get_crawler


class HttpEquivEncodingMiddlewareTest(unittest.TestCase):

    def test_setting_enabled_false(self):
        """Test that `from_crawler` raises `NotConfigured` when
           `HttpEquivEncodingMiddleware` is disabled in the settings.
        """
        self.assertRaises(
            NotConfigured,
            HttpEquivEncodingMiddleware.from_crawler,
            get_crawler(settings_dict={'HTTPEQUIVENCODING_ENABLED': False})
        )

    def test_setting_enabled_default(self):
        """Test that `HttpEquivEncodingMiddleware` is disabled in the default
           settings.
        """
        self.assertRaises(
            NotConfigured,
            HttpEquivEncodingMiddleware.from_crawler,
            get_crawler()
        )

    def test_setting_enabled_true(self):
        """Test that `from_crawler` creates a `HttpEquivEncodingMiddleware`
           instance when the middleware is enabled in the settings.
        """
        self.assertIsInstance(
            HttpEquivEncodingMiddleware.from_crawler(
                get_crawler(settings_dict={'HTTPEQUIVENCODING_ENABLED': True})
            ),
            HttpEquivEncodingMiddleware
        )
