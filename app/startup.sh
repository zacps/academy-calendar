set -euo pipefail

python data_fetch.py & 
gunicorn --conf gunicorn_conf.py --bind 0.0.0.0:80 main:app