import os

from patchwork import files
from fabric import Connection, Config, task


@task
def deploy(c):
    remote_user = os.environ['REMOTEUSER']
    remote_pass = os.environ['USERPASS']
    host = os.environ['REMOTEHOST']

    config = Config(overrides={'sudo': {'password': remote_pass}})
    connect_kwargs = {"password": remote_pass, 'allow_agent': False}
    conn = Connection(host=host, user=remote_user, config=config, connect_kwargs=connect_kwargs)
    print("Connected with remote server")

    print("Copy sources")
    conn.put("app.py")

    print("Install requirements")
    conn.sudo("pip3 install Flask Flask-CORS")

    if files.exists(conn, "/root/server.pid"):
        print("Shutdown previous server")
        conn.sudo("pkill -F server.pid")

    print("Run server")
    conn.sudo("nohup python3 app.py &> logs.txt & echo $! > server.pid")

    conn.close()
    print("Success!")