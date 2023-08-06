from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from setuptools import find_packages, setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Framework :: aiohttp",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

current_directory = Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

version_path = current_directory / "mikomusic" / "_version.py"
module_spec = spec_from_file_location(version_path.name[:-3], version_path)
version_module = module_from_spec(module_spec)
module_spec.loader.exec_module(version_module)

setup(
    name="Kinop",
    version=version_module.__version__,
    description="Music cog for discord bots. Supports YouTube, YoutubeMusic, SoundCloud and Spotify.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=classifiers,
    keywords="musicbot",
    project_urls={
        "Bug Reports": "https://github.com",
        "Source": "https://github.com",
    },
)
