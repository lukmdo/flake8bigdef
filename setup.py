import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


P = __import__('flake8bigdef')


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name=P.NAME,
    version=P.__versionstr__,
    description="Plugin for flake8 - function size checker",
    keywords='flake8 function-size',
    author='lukmdo',
    author_email='me@glukmdo.com',
    url='https://github.com/lukmdo/flake8-bigdef',
    license='MIT',
    py_modules=['flake8bigdef'],
    zip_safe=False,
    install_requires=['flake8'],
    entry_points={
        'flake8.extension': [
            'flake8bigdef = flake8bigdef:Checker',
        ],
    },
    tests_require=["pytest"],
    cmdclass = {'test': PyTest},
)
