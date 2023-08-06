from setuptools import setup

setup(
    name="telepathy",
    version='1.1.1',
    author='Jordan Wildon',
    author_email='j.wildon@pm.me',
    url='https://pypi.python.org/pypi/telepathy/',
    license='LICENSE.txt',
    description='An OSINT toolkit for investigating Telegram chats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=['telepathy'],
    install_requires=[
        'Click',
        'Telethon',
        'Pandas'
    ],
    entry_points='''
        [console_scripts]
        telepathy=telepathy:cli
    ''',
)
