# Copyright (C) 2025-2026 NEC Corporation.
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
"""FastAPI stub for configuration and policy management API"""
import os
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import settings

app = FastAPI()

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESOURCES_FILE = os.path.join(DATA_DIR, "resources.json")
NODES_FILE = os.path.join(DATA_DIR, "nodes.json")
POLICIES_FILE = os.path.join(DATA_DIR, "policies.json")
PROCEDURES_FILE = os.path.join(DATA_DIR, "migration_procedures.json")


def load_json_data(file_path: str):
    """Load data from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return JSONResponse(
            status_code=500,
            content={"message": f"Data file not found: {file_path}"}
        )
    except PermissionError:
        return JSONResponse(
            status_code=500,
            content={"message": f"Permission denied: {file_path}"}
        )
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=500,
            content={"message": f"Invalid JSON format: {file_path}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error loading JSON data: {file_path}, {str(e)}"}
        )


@app.get("/cdim/api/v1/resources")
def get_all_resources():
    """API to retrieve all resource information from configuration management"""
    return load_json_data(RESOURCES_FILE)


@app.get("/cdim/api/v1/nodes")
def get_all_nodes():
    """API to retrieve all node information from configuration management"""
    return load_json_data(NODES_FILE)


@app.get("/cdim/api/v1/policies")
def get_all_policies():
    """API to retrieve all policies from policy management"""
    return load_json_data(POLICIES_FILE)


@app.post("/cdim/api/v1/migration-procedures")
def create_migration_procedures():
    """API to create migration procedures"""
    return load_json_data(PROCEDURES_FILE)


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT, use_colors=False)
