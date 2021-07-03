#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR && docker-compose -f docker-compose.yml -f docker-compose-prod.yml pull && docker-compose -p capstone up -f docker-compose.yml -f docker-compose-prod.yml -d