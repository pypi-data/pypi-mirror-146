from distutils.core import setup

setup(
    name='sync_to_async',
    packages=['sync_to_async'],
    version='0.1.1',
    license='MIT',
    description='Simple python decorator that will convert your sync function into async function',
    author='Menoua Esk',
    author_email='menooa2013@gmail.com',
    url='https://github.com/menooa25/sync_to_async/',
    download_url='https://github.com/menooa25/sync_to_async/archive/refs/heads/main.zip',
    keywords=['SYNC TO ASYNC', 'CONVERT SYNC TO ASYNC', 'CONVERT SYNC', 'CONVERT ASYNC', 'SYNC', 'ASYNC'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
