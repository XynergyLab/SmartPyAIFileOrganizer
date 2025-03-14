from setuptools import setup, find_packages

setup(
    name="organizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.2.2",
        "Pillow==10.3.0",
        "pymediainfo==5.0.3",
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.7.0',
            'pylint>=2.17.5',
            'flake8>=6.1.0',
            'mypy>=1.5.1',
        ],
    },
    entry_points={
        'console_scripts': [
            'organizer=organizer.organizer:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A smart file organization tool",
    keywords="file organization, metadata, archiving",
    python_requires=">=3.7",
)

