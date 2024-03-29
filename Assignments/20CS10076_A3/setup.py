from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    
    name='20CS10076_my_package',  
    version='0.0.1',  
    description='A small Python project for Instance Segmentation and Detection',  
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    author='Vishal Ravipati',  
    author_email='indiavishal3@gmail.com',  
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},  
    packages=find_packages(where='src'),  
    python_requires='>=3.6, <4',
    install_requires=['PIL', 'numpy', 'matplotlib', 'os', 'sys'],  
    entry_points={  
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)