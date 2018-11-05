from setuptools import setup, find_packages


config = {
    'name': 'hoagthee',
    'description': 'Hoagie-based rewards as a service in Slack',
    'author': 'Adam Wentz',
    'author_email': 'adam@adamwentz.com',
    'version': '0.0.1',
    'packages': find_packages(),
    'entry_points': {'console_scripts': ['hoagtheebot=hoagthee.cli:main']},
    'install_requires': [
        'rtmbot',
        'redis',
        'six',
    ]
}

setup(**config)
