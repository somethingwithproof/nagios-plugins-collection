#!/usr/bin/env python3
"""Setup script for nagios-plugins-collection."""

from setuptools import setup, find_packages

# This setup.py is maintained for backward compatibility.
# For modern Python packaging, see pyproject.toml

setup(
    name="nagios-plugins-collection",
    version="1.0.0",
    description="A collection of enterprise-grade Nagios plugins for monitoring various systems",
    author="Thomas Vincent",
    author_email="thomasvincent@gmail.com",
    url="https://github.com/thomasvincent/nagios-plugins-collection",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=[
        "httpx>=0.24.0",
        "typing-extensions>=4.5.0;python_version<'3.8'",
        "importlib-metadata>=6.6.0;python_version<'3.8'",
        "dataclasses>=0.8;python_version<'3.7'",
        "pexpect>=4.8.0",
        "pymongo>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "tox>=4.6.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "pylint>=2.17.0",
            "mypy>=1.3.0",
            "flake8>=6.0.0",
            "pydocstyle>=6.3.0",
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.1",
            "build>=0.10.0",
            "twine>=4.0.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "check_hadoop=nagios_plugins.check_hadoop:main",
            "check_monghealth=nagios_plugins.check_monghealth:main",
            "check_procs=nagios_plugins.check_procs:main",
            "check_mounts=nagios_plugins.check_ro_mounts:main",
            "check_counters_db=nagios_plugins.check_counters_db:main",
            "check_dig=nagios_plugins.check_dig:main",
            "check_etl=nagios_plugins.check_etl:main",
            "check_http500=nagios_plugins.check_http500:main",
            "check_jobs=nagios_plugins.check_jobs:main",
            "check_scribe=nagios_plugins.check_scribe:main",
            "check_statusthroughweb=nagios_plugins.check_statusthroughweb:main",
            "check_website_status=nagios_plugins.website_status_check:main",
            "check_advanced_website_status=nagios_plugins.advanced_website_status_check:main",
            "membase_stats=nagios_plugins.membase_stats:main",
            "url_monitor=nagios_plugins.url_monitor:main",
            "xml_url_checker=nagios_plugins.xml_url_checker:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
)
