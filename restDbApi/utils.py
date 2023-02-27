from typing import Dict, Any
import json
import urllib
from urllib.parse import urlencode


def get_virtual_table(endpoint: str,
                      params: Dict[str, Any] = None,
                      headers: Dict[str, Any] = None,
                      body: Dict[str, Any] = None,
                      jsonpath: str = "$[*]") -> str:

    params_str = get_params_str(params=params)

    headers_custom_param = get_custom_header_params(is_param_added=True if params else False,
                                                    headers=headers)

    is_param_added = False
    if params or headers:
        is_param_added = True
    custom_body_param = get_custom_body_param(is_param_added=is_param_added,
                                              body=body)

    virtual_table = endpoint + params_str + headers_custom_param + custom_body_param + "#" + jsonpath
    return virtual_table


def get_custom_header_params(is_param_added: bool = False, headers: Dict[str, Any] = None) -> str:
    if not headers:
        return ''

    if is_param_added:
        headers_custom_param = '&'
    else:
        headers_custom_param = '?'

    header_number = 1
    loop = len(headers)
    for key, value in headers.items():
        headers_custom_param += 'header' + str(header_number) + "=" + key + ":" + value
        if header_number < loop:
            headers_custom_param += "&"
        header_number += 1

    return headers_custom_param


def get_params_str(params: Dict[str, Any] = None) -> str:
    if not params:
        return ''
    params_str = "?" + urlencode(params)
    return params_str


def get_custom_body_param(is_param_added: bool = False, body: Dict[Any, Any] = None) -> str:
    if not body:
        return ''

    if is_param_added:
        custom_body_param = '&body='
    else:
        custom_body_param = '?body='
    json_parsed_body = json.dumps(body)
    custom_body_param += urllib.parse.quote(json_parsed_body, 'utf8')
    return custom_body_param
