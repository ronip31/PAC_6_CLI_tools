import pytest

def run():
    pytest.main(["tests/"])

def run_verbose():
    pytest.main(["-v", "tests/"])

def run_failures():
    pytest.main(["--lf", "tests/"])
