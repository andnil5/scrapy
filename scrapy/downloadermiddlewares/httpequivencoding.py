from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
import re

class HttpEquivEncodingMiddleware:
    """
    Obey a ``http-equiv`` header for ``Content-Type`` encoding when the HTTP
    header states another encoding.
    """

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPEQUIVENCODING_ENABLED'):
            raise NotConfigured
        return cls()

    def process_response(self, request, response, spider):
        
        if not isinstance(response, HtmlResponse):
            return response

        # Filter HTML comments and spaces
        body = re.sub(b'\s+|<\!--.*?-->', b'', response.body, re.DOTALL)

        # Extract the meta http-equiv='Content-Type' tag from the body if exists
        meta_tag = b'<metahttp-equiv=[\"\']Content-Type[\"\'].*charset[^>)]*?/>'
        meta_charset_tag = re.search(meta_tag, body, re.IGNORECASE)
        if meta_charset_tag:
            # Extract charset key, value pair.
            charset_mapping = re.search(b'charset=[^;\"\']+', meta_charset_tag[0], re.IGNORECASE)
            if charset_mapping:
                # Extract charset value and update response encoding
                response._encoding = charset_mapping[0][8:].decode()

        return response
