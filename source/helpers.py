import os

def get_config(cli, env, default):
    return cli or os.getenv(env) or default


def get_bool(cli, env):
    return cli or (os.getenv(env, "false").lower() == "true")

