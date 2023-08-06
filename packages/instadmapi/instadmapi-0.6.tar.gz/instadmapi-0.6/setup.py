from setuptools import setup, find_packages


setup(
    name='instadmapi',
    version='0.6',
    license='MIT',
    author="Police",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/police/dmapi',
    keywords='example project',
    install_requires=[
        'discord',
        'requests',
        'instagrapi',
        'user_agent',
      ],

)
