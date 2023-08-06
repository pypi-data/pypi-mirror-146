from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["numpy", "pandas"]

setup(
    name="rankia",
    version="0.0.1",
    author="Fusion Power AI",
    author_email="eyal@fusionpower.ai",
    description="Recommender systems for ranked lists in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=[],
    url="https://github.com/fpai/rankia",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    # package_data={'datasets': ['rankia/resources/*']},
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)
