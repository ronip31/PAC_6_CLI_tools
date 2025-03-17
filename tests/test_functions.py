from analyzer.analyze_functions import count_functions

def test_count_functions():
    code = "def minha_funcao():\n    pass"
    assert count_functions(code) == 1

    multiple_functions = "def a():\n    pass\ndef b():\n    pass"
    assert count_functions(multiple_functions) == 2

    no_function_code = "print('Hello')"
    assert count_functions(no_function_code) == 0
