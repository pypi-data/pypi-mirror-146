#!/usr/bin/env bash
set -e

datamodel-codegen \
    --input sm-skill-api-definition/skill-api.yml \
    --input-file-type openapi \
    --output src/smskillsdk/models/api.py
