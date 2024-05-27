#!/bin/bash


exec python3 modules/check_crsstalks.py &
exec python3 modules/checking_token_life.py &
exec python3 modules/parse_data.py &
exec python3 main.py &