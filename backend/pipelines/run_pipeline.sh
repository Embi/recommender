#!/usr/bin/env bash

python -m bytewax.run  -w"${NUMBER_OF_WORKERS:-4}" "pipelines.${PIPELINE_NAME}.pipeline:get_flow()"
