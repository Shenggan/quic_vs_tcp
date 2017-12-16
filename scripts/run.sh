#!/bin/bash

# python run_benchmark.py -p QUIC TCP -l 0.0 -d 10 -v 0 -b 100 --vverbose
# python run_benchmark.py -p QUIC TCP -l 0.0 -d 10 -v 0 -b 40 --vverbose
# python run_benchmark.py -p QUIC TCP -l 0.0 -d 10 -v 0 -b 5 --vverbose

# python run_benchmark.py -p QUIC TCP -l 5.0 -d 10 -v 0 -b 100 --vverbose
# python run_benchmark.py -p QUIC TCP -l 5.0 -d 10 -v 0 -b 40 --vverbose
# python run_benchmark.py -p QUIC TCP -l 5.0 -d 10 -v 0 -b 5 --vverbose

# python run_benchmark.py -p QUIC TCP -l 0.0 -d 50 -v 0 -b 100 --vverbose
# python run_benchmark.py -p QUIC TCP -l 0.0 -d 50 -v 0 -b 40 --vverbose
# python run_benchmark.py -p QUIC TCP -l 0.0 -d 50 -v 0 -b 5 --vverbose

python run_benchmark.py -p QUIC TCP -l 5.0 -d 50 -v 0 -b 100 --vverbose
python run_benchmark.py -p QUIC TCP -l 5.0 -d 50 -v 0 -b 40 --vverbose
python run_benchmark.py -p QUIC TCP -l 5.0 -d 50 -v 0 -b 5 --vverbose

python run_benchmark.py -p QUIC TCP -l 0.0 -d 10 -v 0 -b 100 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 0.0 -d 10 -v 0 -b 40 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 0.0 -d 10 -v 0 -b 5 -s 1 --vverbose

python run_benchmark.py -p QUIC TCP -l 5.0 -d 10 -v 0 -b 100 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 5.0 -d 10 -v 0 -b 40 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 5.0 -d 10 -v 0 -b 5 -s 1 --vverbose

python run_benchmark.py -p QUIC TCP -l 0.0 -d 50 -v 0 -b 100 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 0.0 -d 50 -v 0 -b 40 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 0.0 -d 50 -v 0 -b 5 -s 1 --vverbose

python run_benchmark.py -p QUIC TCP -l 5.0 -d 50 -v 0 -b 100 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 5.0 -d 50 -v 0 -b 40 -s 1 --vverbose
python run_benchmark.py -p QUIC TCP -l 5.0 -d 50 -v 0 -b 5 -s 1 --vverbose