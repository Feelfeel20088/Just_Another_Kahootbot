from setuptools import setup, find_packages

setup(
    name="just_another_kahootbot",
    version="v0.2.0-alpha",
    packages=find_packages(),
    install_requires=[
        "quart==0.20.0",
        "websockets==15.0.1",
        "httpx==0.28.1",
        "hypercorn==0.17.3",
        "orjson==3.10.16",
        "pydantic==2.11.1"
    ],
    entry_points={
        'console_scripts': [
            'just_another_kahootbot = justAnotherKahootBot.__main__:main',
        ],
    },
)
