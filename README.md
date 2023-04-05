
This is an interactive website made using  [Dash](https://plotly.com/dash/) to display the results of a computer-assisted systematic map of the literature on climate change and health outcomes.

After installing the libraries in requirements.txt

`pip install -r requirements.txt`

you can run the app on a localserver simply by executing

`python app.py`

## production setup
```bash
$ gunicorn -b localhost:8000 -w 4 app:server
``` 

### systemd target

Create `/etc/systemd/system/climate-health.service` with the following content, 
then `sudo systemctl daemon-reload` 
before you can manage the service with systemd `sudo systemctl (start|enable|status|stop) climate-health`.

```
[Unit]
Description=Climate and Health App
After=network.target

[Service]
User=www-data
Environment=FLASK_CONFIG=production
Environment=CHA_HOST=127.0.0.1
Environment=CHA_PORT=8085
Environment=CHA_DEBUG=off
WorkingDirectory=/var/www/climate-health
ExecStart=/var/www/climate-health/venv/bin/python -m gunicorn -b 127.0.0.1:8085 -w 4 app:server
Restart=always

[Install]
WantedBy=multi-user.target
```