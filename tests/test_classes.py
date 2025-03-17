from analyzer.analyze_classes import count_classes

def test_count_classes():
    code = "class MinhaClasse:\n    pass"
    assert count_classes(code) == 1

    multiple_classes = "class A:\n    pass\nclass B:\n    pass"
    assert count_classes(multiple_classes) == 2

    no_class_code = "def funcao():\n    pass"
    assert count_classes(no_class_code) == 0
