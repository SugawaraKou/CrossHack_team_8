#!/bin/bash


exec python3 check_crsstalks.py &
exec python3 checking_token_life.py &
exec python3 parse_data.py &
exec python3 main.py &