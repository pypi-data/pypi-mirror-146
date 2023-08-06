from setuptools import setup

from ssl_metrics_github_issue_spoilage import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ssl-metrics-github-issue-spoilage",
    packages=["ssl_metrics_github_issue_spoilage"],
    version=version.version(),
    description="SSL Metrics - GitHub Issues Analysis",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issue-spoilage/issues",
        "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issue-spoilage",
    },
    keywords=[
        "git",
        "github",
        "software engineering",
        "metrics",
        "software systems laboratory",
        "ssl",
        "loyola",
        "loyola university chicago",
        "luc",
    ],
    python_requires=">=3.9",
    install_requires=[
        "intervaltree>=3.1.0",
        "numpy>1.21.2",
        "matplotlib>=3.4.3",
        "pandas>=1.3.3",
        "progress>=1.6",
        "python-dateutil>=2.8.2",
        "requests>=2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "ssl-metrics-github-issue-spoilage-compute = ssl_metrics_github_issue_spoilage.main:main",
            "ssl-metrics-github-issue-spoilage-graph = ssl_metrics_github_issue_spoilage.graph:main",
        ]
    },
)
