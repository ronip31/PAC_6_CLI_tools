from analyzer.analyze_comments import count_comments

def test_count_comments():
    code = "# Comentário\nprint('Hello')\n# Outro comentário\n"
    assert count_comments(code) == 2

    no_comment_code = "print('Sem comentários')\nprint('Outro print')\n"
    assert count_comments(no_comment_code) == 0

    mixed_code = "# Primeiro\nprint('Code')\n  # Indentado\n# Final\n"
    assert count_comments(mixed_code) == 3
