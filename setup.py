from reviewboard.extensions.packaging import setup
from setuptools import find_packages

PACKAGE = "cc_counter"
VERSION = "0.65"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Calculates the cyclomatic complexity of functions",
    author="Kelvin Fann, Chris Lang",
    packages=find_packages(),
    entry_points={
        'reviewboard.extensions':
            '%s = cc_counter.extension:CCCounter' % PACKAGE,
    },
	package_data={
		'cc_counter': [
			'templates/cc_counter/*.html',
		],
	}
)
