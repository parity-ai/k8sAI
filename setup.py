from setuptools import setup, find_packages

setup(
    name='KubeGPT',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'langchain',
        'langchain-chroma',
        'langchain_openai',
        'prompt_toolkit'
    ],
    entry_points='''
        [console_scripts]
        kubegpt=kubegpt.main:main
    ''',
)
