from fabric import Connection, Config, task


@task
def deploy(c):
    remote_user = 'root'
    remote_password = 'qwert1234'
    remote_host = '178.62.2.141'

    config = Config(overrides={'sudo': {'password': remote_password}})
    connect_kwarg = {'password': remote_password, 'allow_agent': False}
    conn = Connection(host=remote_host, user=remote_user, config=config, connect_kwargs=connect_kwarg)
    print("Connected with remote machine")

    print("Copy sources")
    conn.put("app.py")
    conn.put("config.json")

    print("Install requirements")
    conn.sudo("pip3 install Flask Flask-CORS")

    print("Shutdown previous server")
    conn.sudo("pkill -F server.pid", warn=True)

    print("Start server")
    conn.sudo("nohup python3 app.py &> logs.txt & echo $! > server.pid")

    print("Success!")
    conn.close()