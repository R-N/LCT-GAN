from setuptools import setup

setup(
    name='lct_gan',
    version='0.1.0',    
    description='',
    url='https://github.com/R-N/LCT-GAN',
    author='',
    author_email='',
    license='',
    packages=setuptools.find_packages(),
    install_requires=[
        "poetry-core>=1.0.0",
        "numpy>=1.22.3",
        "pandas>=1.4.2",
        "torch>=1.11.0",
        "torchvision>=0.12.0",
        "scikit-learn>=1.0.2",
        "scipy>=1.8.0",
        "seaborn>=0.11.2",
        "matplotlib>=3.5.2",
        "jupyter>=1.0.0",
        "tqdm>=4.64.0",
        "dython>=0.6.7",
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)