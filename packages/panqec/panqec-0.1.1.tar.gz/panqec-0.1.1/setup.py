from setuptools import setup, find_packages

requirements = [
    'PyMatching',
    'tqdm',
    'python-dotenv',
    'pandas',
    'flask',
    'ldpc'
]

setup(
    name='panqec',
    version='0.1.1',
    license='MIT',
    description='Simulation and visualization of quantum error correcting codes',
    url='http://github.com/panqec/panqec',
    author='Eric Huang',
    email='ehuang1@perimeterinstitute.ca',
    packages=find_packages(),
    zip_safe=False,
    requirements=requirements,
    scripts=['bin/panqec'],
)