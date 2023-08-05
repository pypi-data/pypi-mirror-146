from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='CREATURE_WORLD_BUILDER_LITE',
    version='1',
    packages=['CREATURE_WORLD_BUILDER_LITE'],
    url='https://github.com/DigitalCreativeApkDev/CREATURE_WORLD_BUILDER_LITE',
    license='MIT',
    author='DigitalCreativeApkDev',
    author_email='digitalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of the offline strategy RPG "Creature World Builder Lite" '
                'on command line interface.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "CREATURE_WORLD_BUILDER_LITE=CREATURE_WORLD_BUILDER_LITE.creature_world_builder_lite:main",
        ]
    }
)