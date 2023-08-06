from setuptools import setup

setup(
    entry_points={
        'console_scripts': ['odm-report-shot-coverage=odm_report_shot_coverage.scripts.report:main'],
    }
)
