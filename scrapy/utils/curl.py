import argparse
import warnings
from shlex import split
from http.cookies import SimpleCookie
from urllib.parse import urlparse

from w3lib.http import basic_auth_header

coverage_curl_to_request_kwargs = [False]*25

class CurlParser(argparse.ArgumentParser):
    def error(self, message):
        error_msg = f'There was an error parsing the curl command: {message}'
        raise ValueError(error_msg)


curl_parser = CurlParser()
curl_parser.add_argument('url')
curl_parser.add_argument('-H', '--header', dest='headers', action='append')
curl_parser.add_argument('-X', '--request', dest='method')
curl_parser.add_argument('-d', '--data', '--data-raw', dest='data')
curl_parser.add_argument('-u', '--user', dest='auth')


safe_to_ignore_arguments = [
    ['--compressed'],
    # `--compressed` argument is not safe to ignore, but it's included here
    # because the `HttpCompressionMiddleware` is enabled by default
    ['-s', '--silent'],
    ['-v', '--verbose'],
    ['-#', '--progress-bar']
]

for argument in safe_to_ignore_arguments:
    curl_parser.add_argument(*argument, action='store_true')


def curl_to_request_kwargs(curl_command, ignore_unknown_options=True):
    """Convert a cURL command syntax to Request kwargs.

    :param str curl_command: string containing the curl command
    :param bool ignore_unknown_options: If true, only a warning is emitted when
                                        cURL options are unknown. Otherwise
                                        raises an error. (default: True)
    :return: dictionary of Request kwargs
    """

    curl_args = split(curl_command)

    if curl_args[0] != 'curl':
        coverage_curl_to_request_kwargs[0] = True
        raise ValueError('A curl command must start with "curl"')
    else:
        coverage_curl_to_request_kwargs[1] = True

    parsed_args, argv = curl_parser.parse_known_args(curl_args[1:])

    if argv:
        coverage_curl_to_request_kwargs[2] = True
        msg = f'Unrecognized options: {", ".join(argv)}'
        if ignore_unknown_options:
            coverage_curl_to_request_kwargs[3] = True
            warnings.warn(msg)
        else:
            coverage_curl_to_request_kwargs[4] = True
            raise ValueError(msg)
    else:
        coverage_curl_to_request_kwargs[5] = True

    url = parsed_args.url

    # curl automatically prepends 'http' if the scheme is missing, but Request
    # needs the scheme to work
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        coverage_curl_to_request_kwargs[6] = True
        url = 'http://' + url
    else:
        coverage_curl_to_request_kwargs[7] = True

    # Only for branch coverage
    if parsed_args.method:
        coverage_curl_to_request_kwargs[8] = True
    else:
        coverage_curl_to_request_kwargs[9] = True

    method = parsed_args.method or 'GET'

    result = {'method': method.upper(), 'url': url}

    headers = []
    cookies = {}

    # Only for branch coverage
    if parsed_args.headers:
        coverage_curl_to_request_kwargs[10] = True
    else:
        coverage_curl_to_request_kwargs[11] = True

    for header in parsed_args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        if name.title() == 'Cookie':
            coverage_curl_to_request_kwargs[12] = True
            for name, morsel in SimpleCookie(val).items():
                coverage_curl_to_request_kwargs[13] = True
                cookies[name] = morsel.value
        else:
            coverage_curl_to_request_kwargs[14] = True
            headers.append((name, val))

    if parsed_args.auth:
        coverage_curl_to_request_kwargs[15] = True
        user, password = parsed_args.auth.split(':', 1)
        headers.append(('Authorization', basic_auth_header(user, password)))
    else:
        coverage_curl_to_request_kwargs[16] = True

    if headers:
        coverage_curl_to_request_kwargs[17] = True
        result['headers'] = headers
    else:
        coverage_curl_to_request_kwargs[18] = True

    if cookies:
        coverage_curl_to_request_kwargs[19] = True
        result['cookies'] = cookies
    else:
        coverage_curl_to_request_kwargs[20] = True

    if parsed_args.data:
        coverage_curl_to_request_kwargs[21] = True
        result['body'] = parsed_args.data
        if not parsed_args.method:
            coverage_curl_to_request_kwargs[22] = True
            # if the "data" is specified but the "method" is not specified,
            # the default method is 'POST'
            result['method'] = 'POST'
        else:
            coverage_curl_to_request_kwargs[23] = True
    else:
        coverage_curl_to_request_kwargs[24] = True

    return result
