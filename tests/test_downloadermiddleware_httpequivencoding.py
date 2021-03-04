import unittest

from scrapy.downloadermiddlewares.httpequivencoding import HttpEquivEncodingMiddleware
from scrapy.http import Request, Response, TextResponse
from scrapy.utils.test import get_crawler
from scrapy.exceptions import NotConfigured


class HttpEquivEncodingMiddlewareTest(unittest.TestCase):

    def _get_meta_tag_body(self, charset):
        """Creates a html body with a http-equiv attribute declaring
           a specific charset.
        """
        body = """
            <html><head>
                <meta http-equiv="Content-Type" content="text/html; charset={}" />
            </head></html>""".format(charset)
        return body.encode(charset)

    def _get_header(self, charset):
        """Creates a header dictionary declaring a specific charset.
        """
        return {"Content-type": ["text/html; charset={}".format(charset)]}

    def _get_mw_spider(self):
        """Creates a spider and a HttpEquivEncodingMiddleware instance.
        """
        crawler = get_crawler(settings_dict={'HTTPEQUIVENCODING_ENABLED': True})
        spider = crawler._create_spider('foo')
        mw = HttpEquivEncodingMiddleware.from_crawler(crawler)
        return mw, spider

    def _req_res(self, req_kwargs=None, res_kwargs=None):
        """Creates a Request and a TextResponse instance with a
           dummy url and kwargs as specified in the parameters.
        """
        url = "http://example.com/"
        req = Request(url, **(req_kwargs or {}))
        res = TextResponse(url, request=req, **(res_kwargs or {}))
        return req, res

    def test_obey_body_encoding(self):
        """Test that `process_response` obey body encoding if header 
           and body disagree.
        """
        mw, spider = self._get_mw_spider()
        req, res = self._req_res(res_kwargs={
            "body": self._get_meta_tag_body("windows-1252"),
            "headers": self._get_header("utf-8")
        })
        res2 = mw.process_response(req, res, spider)
        self.assertEqual(res2.encoding, "cp1252")

    def test_prioritise_encoding_argument(self):
        """Test that `process_response` prioritise `_encoding`
           if set.
        """
        mw, spider = self._get_mw_spider()
        req, res = self._req_res(res_kwargs={
            "encoding": "utf-16",
            "body": self._get_meta_tag_body("windows-1252"),
            "headers": self._get_header("utf-8")
        })
        res2 = mw.process_response(req, res, spider)
        self.assertEqual(res2.encoding, "utf-16")
        self.assertIs(res, res2)

    def test_no_headers_encoding(self):
        """Test that `process_response` does not modify the response
           if no charset is specified in the header.
        """
        mw, spider = self._get_mw_spider()
        req, res = self._req_res(res_kwargs={
            "body": self._get_meta_tag_body("windows-1252"),
        })
        res2 = mw.process_response(req, res, spider)
        self.assertEqual(res2.encoding, "cp1252")
        self.assertIs(res, res2)

    def test_no_body_encoding(self):
        """Test that `process_response` does not modify the response
           if the body does not contain a charset declaration. 
        """
        mw, spider = self._get_mw_spider()
        req, res = self._req_res(res_kwargs={
            "body": b'<html> <head></head> </html>',
            "headers": self._get_header("utf-8")
        })
        res2 = mw.process_response(req, res, spider)
        self.assertEqual(res2.encoding, "utf-8")
        self.assertIs(res, res2)

    def test_same_encoding(self):
        """Test that `process_response` does not modify the response
           if the body and header charset is equal.
        """
        mw, spider = self._get_mw_spider()
        req, res = self._req_res(res_kwargs={
            "body": self._get_meta_tag_body("utf-8"),
            "headers": self._get_header("utf-8")
        })
        res2 = mw.process_response(req, res, spider)
        self.assertEqual(res2.encoding, "utf-8")
        self.assertIs(res, res2)

    def test_not_text_response(self):
        """Test that `process_response` does not modify the response
           if the given response is not a TextResponse instance.
        """
        mw, spider = self._get_mw_spider()
        url = "http://example.com/"
        req = Request(url)
        res = Response(url)
        res2 = mw.process_response(req, res, spider)
        self.assertIs(res, res2)

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
