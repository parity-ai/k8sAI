from setuptools import setup, find_packages

setup(
    name="k8sAI",
    version="0.1.2",
    packages=find_packages(),
    description="A simple example package",
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
    ],
    entry_points="""
        [console_scripts]
        k8sAI=k8sAI.main:main
    """,
)
