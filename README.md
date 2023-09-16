# simple-phonebook-flask
Make your simple phonebook with flask and asterisk database.

|   Start screen      |     Search screen      |     Useful screen     |
|------------|-------------|-------------|
| <img src="https://github.com/vansatchen/simple-phonebook-flask/blob/main/screenshots/Screenshot1.png" width="250"> | <img src="https://github.com/vansatchen/simple-phonebook-flask/blob/main/screenshots/Screenshot2.png" width="250"> | <img src="https://github.com/vansatchen/simple-phonebook-flask/blob/main/screenshots/Screenshot3.png" width="250"> |

## Preparation
### Need:
- Linux server(Ubuntu) with user with sudo privilage.
- Nginx installed.
- Domain name(optional).
```
git clone https://github.com/vansatchen/simple-phonebook-flask.git ~/simple-phonebook-flask
```
### Installations:
```
$ sudo apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```
Make virtual environment(optional)
```
$ sudo apt install python3-venv
$ sudo cp -r ~/simple-phonebook-flask/phonebook_flask /opt/phonebook
$ sudo chown -R user:user /opt/phonebook
$ cd /opt/phonebook
$ python3 -m venv venv
# Activate virtual environment
$ source venv/bin/activate
```
Install nedded python modules from pip
```
$ pip install wheel
```
> In venv use **pip**, not pip3
```
$ pip install uwsgi flask flask-sqlalchemy mysqlclient
```
Edit app.py with your needs.
Especially this line for connect to mysql:
> app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:userpass@localhost/asteriskdb'

Test installation:
```
$ python3 app.py
```
it must be something like that:
> * Serving Flask app "app" (lazy loading)
> * Environment: production
>   WARNING: Do not use the development server in a production environment.
>   Use a production WSGI server instead.
> * Debug mode: off
> * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Test uwsgi:
```
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```
If your use virtual environment, deactivate it:
```
deactivate
```
## Systemd
Now let's use systemd for autostart phonebook:
```
$ sudo cp ~/simple-phonebook-flask/systemd/phonebook-flask.service /etc/systemd/system/
$ sudo systemctl start phonebook-flask.service
$ sudo systemctl enable phonebook-flask.service
```
## Nginx
```
$ sudo cp ~/simple-phonebook-flask/nginx/phonebook-flask /etc/nginx/sites-available/
```
Edit **server_name** and **ssl** options in /etc/nginx/sites-available/phonebook-flask
> If you don't want use ssl, just replace  ```listen 443;```  to  ```listen 80;```
> and remove lines  ```ssl on```  ```ssl_certificate```  ```ssl_certificate_key```
```
$ sudo ln -s /etc/nginx/sites-available/phonebook-flask /etc/nginx/sites-enabled/
```
Check nginx config:
```
$ sudo nginx -t
```
Restart nginx:
```
$ sudo systemctl restart nginx
```
Now open it in browser

## Check errors
```
$ sudo journalctl -u nginx
$ sudo journalctl -u phonebook-flask
```
