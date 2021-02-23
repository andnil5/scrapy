all: test

test:
	test -d branch_cov_logs || mkdir branch_cov_logs
	tox -- tests/test_http_request.py tests/test_utils_curl.py tests/test_utils_python.py