from setuptools import setup

setup(
    name='ypack',
    version='0.1.1',
    description='A example Python package',
    url='https://github.com/YoussephAhmed/ypack',
    author='Youssef Ahmed',
    author_email='yousseffahmed@hotmail.com',
    license='BSD 2-clause',
    packages=['ypack'],
    install_requires=[
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
