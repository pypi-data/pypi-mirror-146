from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A simple spelling bee game'
LONG_DESCRIPTION = 'A game that takes a word and gets images related to it. Prompts for input and records your scores. '

# Setting up
setup(
    name="spelling-bee-game",
    version=VERSION,
    author="ChurningLava",
    author_email="snoopydankl@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python'],
    keywords=['python', 'spelling-bee','game']
)