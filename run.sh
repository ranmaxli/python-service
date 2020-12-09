rm logs/*
ENV=dev
python src/main.py --common_config=conf/python-service.conf --env=$ENV
