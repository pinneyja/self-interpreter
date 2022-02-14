from interpreting.Interpreter import Interpreter
import pytest

@pytest.fixture(scope="session")
def interpreter():
	interpreter = Interpreter()
	interpreter.initializeBootstrap()
	return interpreter