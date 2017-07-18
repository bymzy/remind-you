from setuptools import setup, find_packages


setup(
    name = 'remind_you',
    version = '0.1',
    packages = find_packages(),
    authors = 'mingzhengying',
    description = 'remind you something!!!',
    entry_points = {
        'console_scripts': [
            'save_word = remind_you.cmds:save_word_cmd',
            ]
    }
)

