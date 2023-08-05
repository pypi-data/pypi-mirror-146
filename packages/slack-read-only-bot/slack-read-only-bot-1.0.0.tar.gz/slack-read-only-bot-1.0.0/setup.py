#!/usr/bin/env python

from setuptools import setup
import os.path


try:
    DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(DIR, "README.md"), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description=None


setup(
    name="slack-read-only-bot",
    version="1.0.0",
    description="Make Slack channels read-only by restricting which users can post to them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pR0Ps/slack-read-only-bot",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.6,<4",
    install_requires=[
        "slackclient>=1.1.0,<2.0.0",
        "pyyaml>=5.4.1,<7.0.0",
    ],
    py_modules=["slack_read_only_bot"],
    entry_points={
        "console_scripts": [
            "slack-read-only-bot=slack_read_only_bot:main"
        ]
    },
)
