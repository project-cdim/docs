# Copyright 2025 NEC Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
#  under the License.

"""REST API stub."""

import logging
from pathlib import Path

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse


logger = logging.getLogger("uvicorn")
app = FastAPI()


@app.get("{uri:path}")
def get(request: Request, uri: str) -> Response:
    """Handle a GET request."""
    uri_with_query = uri
    if request.url.query:
        uri_with_query += f"?{request.url.query}"

    json_path = _locate_json(uri_with_query)
    logger.info("GET: %s => %s", uri_with_query, json_path)
    if not json_path:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return FileResponse(json_path)


@app.post("{uri:path}", status_code=status.HTTP_200_OK)
async def post(request: Request, uri: str) -> Response:
    """Handle a POST request."""
    match request.headers["content-type"]:
        case "application/json":
            body = await request.json()
        case "application/x-www-form-urlencoded":
            body = await request.form()
        case _:
            body = await request.body()

    uri_with_query = uri
    if request.url.query:
        uri_with_query += f"?{request.url.query}"

    json_path = _locate_json(uri_with_query)
    if json_path:
        logger.info("POST: %s body=[%s] => [ %s ]", uri_with_query, body, json_path)
        return FileResponse(json_path)

    logger.info("POST: %s body=[%s] => OK", uri_with_query, body)
    return Response(status_code=status.HTTP_200_OK)


def _normalize_json_dirs(*uri_dir_pairs: tuple[str, str]) -> list[tuple[str, Path]]:
    data_dir = Path(__file__).parent.joinpath("data")
    sorted_uri_dir_pairs = sorted(uri_dir_pairs, key=lambda x: len(x[0]), reverse=True)  # longest match
    return [(x[0], data_dir.joinpath(x[1]).absolute()) for x in sorted_uri_dir_pairs]


# (URI prefix, JSON directory)
JSON_DIRS = _normalize_json_dirs(
    ("/cdim/api/v1/agent/", "agent"),
    ("/oob-sample/redfish/v1/", "oob-sample"),
    ("/fm-sample/", "fm-sample"),
    ("/hw-control/", "hw-control"),
)


def _locate_json(uri_with_query: str) -> Path | None:
    for uri_prefix, json_dir in JSON_DIRS:
        if uri_with_query.startswith(uri_prefix):
            filename = uri_with_query[len(uri_prefix):]
            filename = filename.replace("/", "_")
            filename = filename.replace("?", "__").replace("&", "__")
            json_path = json_dir.joinpath(f"{filename}.json").resolve()
            if not json_path.is_relative_to(json_dir) or not json_path.is_file():
                return None
            return json_path
    return None
