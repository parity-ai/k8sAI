import configparser
from uuid import UUID
import uuid
import click
import os
import json
from posthog import Posthog
import requests


class Usage:
    def __init__(self):
        self.posthog = None
        self.enabled = False
        self.uuid = None

    def setup(self):
        self.prompt_usage()
        config_path = os.path.expanduser("~/.k8sAI/config.ini")
        config = configparser.ConfigParser()

        if os.path.exists(config_path):
            config.read(config_path)
            # Check if 'usage' section and necessary keys exist
            if "usage" in config and "usage_enabled" in config["usage"]:
                self.enabled = config["usage"].getboolean("usage_enabled")
            if "usage" in config and "uuid" in config["usage"]:
                self.uuid = config["usage"]["uuid"]
            if "key" in config:
                self.ph = config["key"]["ph"]

        if getattr(self, "enabled", False) and self.ph:
            self.posthog = Posthog(
                project_api_key=self.ph,
                host="https://us.i.posthog.com",
            )

    def prompt_usage(self):
        config = configparser.ConfigParser()
        config_path = os.path.expanduser("~/.k8sAI/config.ini")
        config.read(config_path)
        config_dir = os.path.dirname(config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        if "usage" not in config:
            click.echo("Thank you for using k8sAI!")
            if click.confirm(
                "Do you want to help improve k8sAI by sending anonymous usage statistics?"
            ):
                # User agreed to usage
                config = configparser.ConfigParser()
                config.read(config_path)
                config["usage"] = {"usage_enabled": "true", "uuid": str(uuid.uuid4())}
                response = requests.get("http://k8s.wilsonspearman.com/getUsage")
                if response.status_code == 200:
                    ph = response.text
                    config["key"] = {"ph": ph}
                with open(config_path, "w") as configfile:
                    config.write(configfile)
                print(f"ph written to {config_path}")

                with open(config_path, "w") as configfile:
                    config.write(configfile)
                click.echo("Usage enabled. Thank you for your support!")
            else:
                # User declined usage
                config = configparser.ConfigParser()
                config["usage"] = {"usage_enabled": "false"}
                with open(config_path, "w") as configfile:
                    config.write(configfile)
                click.echo("Usage disabled. You can enable it later in the config.")

    def log_event(self, event_name):
        if self.posthog:
            self.posthog.capture(self.uuid, event_name)
