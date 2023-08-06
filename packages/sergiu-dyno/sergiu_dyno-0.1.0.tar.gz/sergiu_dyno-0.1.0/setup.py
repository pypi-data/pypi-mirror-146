from setuptools import find_packages, setup
#
# from pathlib import Path
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()

setup(
    name="sergiu_dyno",
    version="0.1.0",
    author="Matei Sergiu",
    author_email="mateisergiu777@gmail.com",
    packages=find_packages(),
    package_dir={"": "src/"},
    include_package_data=True,
    description="Prints a dinosaur",
    # long_description=long_description,
    # long_description_content_type='text/markdown'
)
