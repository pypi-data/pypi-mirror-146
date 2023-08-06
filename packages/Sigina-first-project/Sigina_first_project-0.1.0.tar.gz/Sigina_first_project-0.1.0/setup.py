from setuptools import find_packages, setup

setup(
    name='Sigina_first_project',
    version='0.1.0',
    author='Sigina',
    author_mail='sigina.cirja@gmail.com',
    packages=[],
    packages_dir={
        "": "scr/"
    },
    include_package_data=True,
    description="Says Hello from Sigina",
    install_requires="dinsoay"
)