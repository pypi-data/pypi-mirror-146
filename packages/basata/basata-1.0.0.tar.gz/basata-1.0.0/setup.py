from setuptools import setup, find_packages

def readme():
    with open("README.md", encoding="utf8") as f:
        README = f.read()
    return README

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='basata',
    version='1.0.0',
    description='BASATA - Code less while gaining more',
    long_description=readme(),
    long_description_content_type="text/markdown",
    license='MIT',
    author="Tarek K. Ghanoum",
    author_email='ta.ghanoum@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages('basata'),
    package_dir={'': 'basata'},
    url='https://github.com/sg-tarek/BASATA',
    keywords='ML AI Supervised TimeSeries Unsupservised',
    install_requires=required
)