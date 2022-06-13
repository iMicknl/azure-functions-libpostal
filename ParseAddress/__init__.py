import logging
import json
import re

import azure.functions as func
from postal.parser import parse_address
from postal.normalize import normalize_string, DEFAULT_STRING_OPTIONS


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    address = req.params.get('address')
    language = req.params.get('language')

    if not address:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            address = req_body.get('address')
            language = req_body.get('language')

    if address:
        # Remove space in Dutch postal code
        address = re.sub(r"(\d{4})\s?([A-Z]{2})", r"\1\2", address)

        # Call Libpostal
        expanded_address = parse_address(address, language=language)

        # Rewrite tuple to object
        output = {}
        for k,v in expanded_address:
            output[v] = normalize_string(k, string_options= DEFAULT_STRING_OPTIONS)

        return func.HttpResponse(json.dumps(output))
    else:
        return func.HttpResponse(
             "Pass an address in the query string or in the request body.",
             status_code=200
        )
