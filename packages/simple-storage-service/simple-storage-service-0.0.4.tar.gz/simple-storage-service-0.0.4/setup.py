import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple-storage-service',
    version='0.0.4',
    author='Lucas Nascimento Huati Corrêa',
    author_email='lucas@educat.net.br',
    description='Assist in the handling of files on storages from different providers.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/r13/educat-community/simple-storage-service',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'boto3==1.20.10',
        'azure-storage-blob==2.0.1',
        'google-cloud-storage==1.36.0',
    ],
)
