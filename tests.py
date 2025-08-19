from functions import get_files_info
import unittest

class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_current_dir(self):
        result = get_files_info("calculator", ".")
        print(result)
        self.assertEqual(result, 
"""Result for current directory:
 - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True""")

    def test_calculator_pkg_dir(self):
        result = get_files_info("calculator", "pkg")
        print(result)
        self.assertEqual(result, 
"""Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False""")
        
    def test_calculator_bin_dir(self):
        result = get_files_info("calculator", "/bin")
        print(result)
        self.assertEqual(result, 
"""Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory""")
        
    def test_calculator_outside_dir(self):
        result = get_files_info("calculator", "../")
        print(result)
        self.assertEqual(result, 
"""Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory""")
        
if __name__ == "__main__":
    unittest.main()