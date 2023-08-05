from setuptools import setup

setup(
    name="epy00",
    version='0.0.1',
    packages=['epy00'],
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        demo=epy00.app:main
    ''',
)
