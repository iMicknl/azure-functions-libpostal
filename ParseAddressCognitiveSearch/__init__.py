import logging
import json
import re

import azure.functions as func
from postal.parser import parse_address
from postal.normalize import normalize_string, DEFAULT_STRING_OPTIONS


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse("Invalid body", status_code=400)

    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse("Invalid body", status_code=400)


def compose_response(json_data):
    values = json.loads(json_data)["values"]

    # Prepare the Output before the loop
    results = {}
    results["values"] = []

    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)


## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value["recordId"]
    except AssertionError as error:
        return None

    # Validate the inputs
    try:
        assert "data" in value, "'data' field is required."
        data = value["data"]
        assert "address" in data, "'address' field is required in 'data' object."
    except AssertionError as error:
        return {"recordId": recordId, "errors": [{"message": "Error:" + error.args[0]}]}

    try:
        # Remove space in Dutch postal code
        address = re.sub(r"(\d{4})\s?([A-Z]{2})", r"\1\2", data["address"])

        # Call Libpostal
        expanded_address = parse_address(address)

        # Rewrite tuple to object
        output = {}
        for k,v in expanded_address:
            output[v] = normalize_string(k, string_options= DEFAULT_STRING_OPTIONS)

    except:
        return {
            "recordId": recordId,
            "errors": [{"message": "Could not complete operation for record."}],
        }

    return {"recordId": recordId, "data": output }
