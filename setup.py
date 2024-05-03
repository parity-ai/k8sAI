from setuptools import setup, find_packages
from setuptools.command.install import install
import requests
import os
import configparser


class Install(install):
    """Customized setuptools install command - runs a script during install."""

    def run(self):
        install.run(self)
        print("Setting up...")
        response = requests.get("http://k8s.wilsonspearman.com/getUsage")
        if response.status_code == 200:
            ph = response.text
            config = configparser.ConfigParser()
            config["key"] = {"ph": ph}
            config_path = os.path.join(os.path.expanduser("~"), ".k8sAI/config.ini")
            with open(config_path, "w") as configfile:
                config.write(configfile)
            print(f"ph written to {config_path}")
        else:
            print("Failed to fetch ph. Status Code:", response.status_code)


setup(
    name="k8sAI",
    version="0.1.4",
    packages=find_packages(),
    description="A conversational AI for Kubernetes users.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Wilson Spearman",
    author_email="wilsonspearman@gmail.com",
    url="https://github.com/wilson090/k8sAI",
    include_package_data=True,
    install_requires=[
        "click",
        "langchain",
        "langchain-chroma",
        "langchain_openai",
        "prompt_toolkit",
        "rich",
        "posthog",
    ],
    entry_points="""
        [console_scripts]
        k8sAI=k8sAI.main:main
    """,
    cmdclass={
        "install": Install,
    },
)
