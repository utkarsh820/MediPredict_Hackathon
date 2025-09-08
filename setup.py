from setuptools import setup, find_packages
from typing import List

def read_requirements(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#') and not line.startswith('-e')]

setup(
    name='MediPredict',
    version='0.1',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    author='Utkarsh Pandey & Shubham Sharma',
    description='The primary goal is to build a robust classification model that can assist in early and accurate disease identification.',
    license='MIT',
    keywords='medical prediction',
    url='https://github.com/yourusername/MediPredict',
)