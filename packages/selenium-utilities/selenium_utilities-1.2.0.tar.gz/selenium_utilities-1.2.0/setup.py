import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='selenium_utilities',
    version='1.2.0',
    author='Maehdakvan',
    author_email='visitanimation@google.com',
    description='Useful utilities for comfortable using selenium.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DedInc/selenium_utilities',
    project_urls={
        'Bug Tracker': 'https://github.com/DedInc/selenium_utilities/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['selenium_utilities'],
    include_package_data = True,
    install_requires = ['requests', 'lxml'],
    python_requires='>=3.6',
)