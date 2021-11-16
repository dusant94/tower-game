## Starting project


Create virtual enviroment
- py -3.8 -m venv .venv

Install requirements
- pip install -r requirements.txt

Create config 
- mkdir -p storage/config && cp storage/config_templates/docker* storage/config

Run migration
- make upgrade

Start servers
1. main.py
2. hocus/server.py
3. pocus/server.py

Aio pika consumers
1. api/amqp_consumer.py
2. hocus/consumer.py
3. pocus/conusmer.py
 