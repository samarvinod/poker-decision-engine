from setuptools import setup, find_packages

setup(
    name="poker-decision-engine",
    version="0.1.0",
    description="A poker decision engine that evaluates game situations and recommends optimal actions",
    author="",
    packages=find_packages(),
    install_requires=[
        "treys>=0.1.8",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "poker-engine=poker_engine.engine.decision_engine:main",
        ],
    },
)

