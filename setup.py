from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="Hotel_Reservation_MLOPS_1",
    version="0.1",
    author="Nasir",
    packages=find_packages(),
    install_requires=requirements,
)