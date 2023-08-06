from pathlib import Path
import shutil
from setuptools import setup as _setup, find_packages


root = Path(__file__).parent
PKG = root.name


def clean():
    for path in (root / "src").iterdir():
        if path.suffix == ".egg-info":
            shutil.rmtree(path)
    for path in root.iterdir():
        if path.suffix == ".egg-info":
            shutil.rmtree(path)
    shutil.rmtree(root / "build", ignore_errors=True)


pkgs = find_packages("src")


def setup(*args, **kwargs):
    clean()
    readme = (root / "README.md").read_text()
    _setup(
        *args,
        long_description=readme,
        long_description_content_type="text/markdown",
        author="Jose A.",
        author_email="jose-pr@coqui.dev",
        url=f"https://github.com/jose-pr/{PKG}",
        package_dir={"": "src"},
        py_modules=[PKG],
        install_requires=Path("requirements.txt").read_text().splitlines(),
        **kwargs,
    )
    clean()


setup(
    name=PKG,
    version=Path("VERSION").read_text(),
    description=Path("DESCRIPTION").read_text(),
)
