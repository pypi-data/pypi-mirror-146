import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='schema_matching',
    version='0.3.1',
    description='Using XGboost and Sentence-Transformers to perform schema matching task on tables.',
    license_files=('LICENSE',),
    author='fireindark707',
    author_email='phoenix000.taipei@gmail.com',
    maintainer='fireindark707',
    maintainer_email='phoenix000.taipei@gmail.com',
    url='https://github.com/fireindark707/Python-Schema-Matching',
    download_url='https://github.com/fireindark707/Python-Schema-Matching/archive/refs/tags/v0.2.tar.gz',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "numpy>=1.19.5",
        "pandas>=1.1.5",
        "nltk>=3.6.5",
        "python-dateutil>=2.8.2",
        "sentence-transformers>=2.1.0",
        "xgboost>=1.5.2",
        "strsimpy>=0.2.1",
    ],
    keywords=['schema matching', 'dataset discovery', 'schema mapping', 'XGboost', 'sentence-transformers', 'NLP'],
    package_data={
        'schema_matching': ["*.model","model/2022-04-12-12-06-32/*.model","*.threshold","model/2022-04-12-12-06-32/*.threshold"],
    },
    include_package_data=True,
    python_requires='>=3.6,<3.11',
    long_description=long_description,
    long_description_content_type='text/markdown'
)