#!/usr/bin/python3 -O


from setuptools import find_packages, setup

if setup is not None:
    # setup must be imported before cythonize
    from distutils.extension import Extension

    from Cython.Build import cythonize


_PACK_NAME = "MAB_algorithm"
_VERSION = "0.0.2"


def main():
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()

    with open('requirements.txt', 'r', encoding='utf-8') as f:
        install_requires = f.read().strip().split('\n')

    setup(
        name=_PACK_NAME,
        version=_VERSION,
        author="Antares",
        author_email="Antares0982@gmail.com",
        license="MIT",
        platforms=["Windows", "Linux"],
        description="A modern multi-armed bandits library.",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/Antares0982/MAB-algorithm-template",
        ext_modules=cythonize([Extension("mabCutils", [
            f"{_PACK_NAME}/mabCutils.pyx",
            f"{_PACK_NAME}/src/cutils.cpp"
        ])]),
        options={'build_ext': {"build_lib": _PACK_NAME}},
        install_requires=install_requires,
        package_data={_PACK_NAME: ["*.so", "*.pyi"]},
        packages=find_packages()
    )


if __name__ == "__main__":
    main()
