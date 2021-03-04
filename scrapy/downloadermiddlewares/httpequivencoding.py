from scrapy.exceptions import NotConfigured
from scrapy.http import TextResponse

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

        if isinstance(response, TextResponse) \
            and response._encoding is None \
            and response._headers_encoding is not None \
            and response._body_declared_encoding() is not None \
            and response._headers_encoding() != response._body_declared_encoding():
            return response.replace(encoding=response._body_declared_encoding())
            
        return response
