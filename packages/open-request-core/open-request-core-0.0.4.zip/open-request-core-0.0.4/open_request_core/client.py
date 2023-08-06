#!/usr/bin/env python
# coding=utf-8
from __future__ import annotations
from typing import TypeVar, TYPE_CHECKING
import logging

import requests

from .exception import ServerException


if TYPE_CHECKING:
    from .request import Request
    from .response import ContentResponse

    TResponse = TypeVar("TResponse", bound=ContentResponse)

__all__ = ["Client"]
logger = logging.getLogger("open-request-core")


class Client(object):
    def __init__(self, base_url: str, timeout=3, https_verify=False, max_retries=3):
        self.__base_url = base_url
        self.__timeout = timeout
        self.__https_verify = https_verify
        self.__max_retries = max_retries

    def get_baseurl(self):
        return self.__base_url

    def set_baseurl(self, baseurl):
        self.__base_url = baseurl

    def get_timeout(self):
        return self.__timeout

    def set_timeout(self, timeout):
        self.__timeout = timeout

    def get_https_verify(self):
        return self.__https_verify

    def get_signed_headers(self, request: Request):
        return request.get_headers()

    def get_signed_query_params(self, request: Request):
        return request.get_query_params()

    def _handle_single_request(self, request: Request):
        """发送请求

        Args:
            request (Request): Request对象

        Returns:
            tuple: 返回三元组(HTTP status code, HTTP headers, HTTP byte content)
        """
        uri = request.get_uri()
        if self.__base_url.endswith("/") and uri.startswith("/"):
            url = self.__base_url + uri[1:]
        elif not self.__base_url.endswith("/") and not uri.startswith("/"):
            url = self.__base_url + "/" + uri
        else:
            url = self.__base_url + uri
        resp = requests.request(
            method=request.get_method(),
            url=url,
            params=self.get_signed_query_params(request),
            data=request.get_data(),
            headers=self.get_signed_headers(request),
            json=request.get_json(),
            files=request.get_files(),
            verify=self.__https_verify,
            timeout=self.__timeout,
        )
        return resp.status_code, resp.headers, resp.content

    def do_action(self, request: Request[TResponse]) -> TResponse:
        retries = 0
        while True:
            retries += 1
            logger.debug("client do action send request: {}".format(request))
            status_code, headers, content = self._handle_single_request(request)
            if retries > self.__max_retries:
                break
            if self.should_retry(status_code, headers, content):
                continue
            self.should_exception(status_code, headers, content)
            break
        resp = request.resp_cls(content)
        logger.debug("client do action get response: {}".format(resp))
        return resp

    def should_retry(self, status_code, headers, content) -> bool:
        return False

    def should_exception(self, status_code, headers, content):
        if status_code < 200 or status_code >= 300:
            raise ServerException(status_code, content)
