from analyzer.analyze_lines import count_lines

def test_count_lines():
    code = "print('Hello, World!')\nprint('Python!')\n"
    assert count_lines(code) == 2

    empty_code = ""
    assert count_lines(empty_code) == 0

    multiline_code = "line1\nline2\nline3\n"
    assert count_lines(multiline_code) == 3
