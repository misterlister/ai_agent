from functions import get_files_info, get_file_content
import unittest

class TestGetFilesInfo(unittest.TestCase):
    def test_get_content_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        self.assertTrue("def main():" in result)
        
    def test_get_content_pkg_calc(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertTrue("def _apply_operator(self, operators, values)" in result)
        
    def test_get_content_bin_cat(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertTrue(result.startswith("Error:"))
        
    def test_get_content_does_not_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)
        self.assertTrue(result.startswith("Error:"))

        
if __name__ == "__main__":
    unittest.main()