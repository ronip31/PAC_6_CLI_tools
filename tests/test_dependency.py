import unittest
import tempfile
import os
from collections import defaultdict
from analyzer.dependency_analyzer import get_external_imports, analyze_repository

class TestDependencyAnalyzer(unittest.TestCase):

    def setUp(self):
        # Cria diretório temporário para os testes
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = self.test_dir.name

    def tearDown(self):
        # Limpa os arquivos temporários ao final
        self.test_dir.cleanup()

    def create_temp_file(self, content, filename="test.py"):
        file_path = os.path.join(self.test_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def test_no_imports(self):
        content = "print('hello world')"
        path = self.create_temp_file(content)
        counter = defaultdict(int)
        get_external_imports(path, counter)
        self.assertEqual(len(counter), 0)

    def test_standard_library_import(self):
        content = "import os\nimport sys\nfrom math import sqrt"
        path = self.create_temp_file(content)
        counter = defaultdict(int)
        get_external_imports(path, counter)
        self.assertEqual(len(counter), 0)

    def test_external_imports(self):
        content = "import numpy\nfrom pandas import DataFrame\nimport requests"
        path = self.create_temp_file(content)
        counter = defaultdict(int)
        get_external_imports(path, counter)
        self.assertEqual(counter['numpy'], 1)
        self.assertEqual(counter['pandas'], 1)
        self.assertEqual(counter['requests'], 1)

    def test_mixed_imports(self):
        content = "import os\nimport numpy\nfrom pandas import DataFrame"
        path = self.create_temp_file(content)
        counter = defaultdict(int)
        get_external_imports(path, counter)
        self.assertEqual(len(counter), 2)
        self.assertIn('numpy', counter)
        self.assertIn('pandas', counter)

    def test_syntax_error_file(self):
        content = "import os\nthis is not valid python"
        path = self.create_temp_file(content)
        counter = defaultdict(int)
        get_external_imports(path, counter)
        self.assertEqual(len(counter), 0)

    def test_analyze_repository_multiple_files(self):
        self.create_temp_file("import numpy", filename="file1.py")
        self.create_temp_file("import requests", filename="file2.py")
        self.create_temp_file("import os", filename="file3.py")  # stdlib

        result = analyze_repository(self.test_path)
        self.assertEqual(result['numpy'], 1)
        self.assertEqual(result['requests'], 1)
        self.assertNotIn('os', result)

if __name__ == "__main__":
    unittest.main()
