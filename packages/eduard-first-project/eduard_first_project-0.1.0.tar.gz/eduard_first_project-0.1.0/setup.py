from setuptools import find_packages, setup

setup(
    name="eduard_first_project",
    version="0.1.0",
    author="Eduard Gabriel Lupascu",
    author_email="eduardglupascu@gmail.com",
    packages=["eduard_first_project"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="Says Hello",
    install_requires="dinosay"
)