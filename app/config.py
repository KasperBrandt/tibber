import os
import yaml


def load_config_from_env(environment):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "configs", f"{environment}.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


class Config:

    # Default to 'dev' if ENV is not set
    env = os.getenv("ENV", "dev")
    config = load_config_from_env(env)

    # Access configurations
    DATABASE_DB = config["database"]["db"]
    DATABASE_HOST = config["database"]["host"]
    DATABASE_USER = config["database"]["user"]
    DATABASE_PASSWORD = config["database"]["password"]

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}/{self.DATABASE_DB}"
