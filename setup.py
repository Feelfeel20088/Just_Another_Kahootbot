from setuptools import setup, find_packages

setup(
    name="just_another_kahootbot",
    version="v0.2.0-alpha",
    packages=find_packages(), # Automatically find all packages in the project
    entry_points={
        'console_scripts': [
            'just_another_kahootbot = .justAnotherKahootBot.__main__:main',
        ],
    },
)
