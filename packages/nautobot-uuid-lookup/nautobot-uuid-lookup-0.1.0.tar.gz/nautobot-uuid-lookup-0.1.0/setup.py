#!/usr/bin/env python

import setuptools

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

if __name__ == "__main__":
    setuptools.setup(
        name='nautobot-uuid-lookup',
        author='Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen',
        version='0.1.0',
        license='Apache-2.0',
        url='https://gitlab-ce.gwdg.de/gwdg-netz/nautobot-plugins/nautobot-uuid-lookup',
        description='A Nautobot plugin for finding things by UUID',
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages('.'),
        include_package_data=True,
        install_requires=[],
        zip_safe=False,
)
