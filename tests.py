import unittest
from unittest.mock import patch
from io import StringIO
from emulator import ShellEmulator
class TestShellEmulator(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_ls(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/dir1/": 'dir',
            "/dir2/": 'dir',
            "/file1.txt": 'file',
            "/dir1/file2.txt": 'file'
        }
        emulator.cwd = "/"
        emulator.cmd_ls()
        output = mock_stdout.getvalue().strip().split("\n")
        self.assertIn("dir1/", output)
        self.assertIn("dir2/", output)
        self.assertNotIn("file2.txt", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cd(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/dir1/": 'dir',
            "/dir2/": 'dir',
            "/file1.txt": 'file',
        }
        emulator.cwd = "/dir1/"
        emulator.cmd_cd("/dir1/non_existent_dir")
        output = mock_stdout.getvalue().strip()
        self.assertIn("cd: /dir1/non_existent_dir: No directory", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cd2(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/dir1/": 'dir',
            "/dir2/": 'dir',
            "/file1.txt": 'file',
        }
        emulator.cwd = "/"
        emulator.cmd_cd("/")
        output = mock_stdout.getvalue().strip()
        self.assertIn("Changed directory to /", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cd3(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/dir1/": 'dir',
            "/dir2/": 'dir',
            "/file1.txt": 'file',
        }
        emulator.cwd = "/"
        emulator.cmd_cd("/dir1")
        output = mock_stdout.getvalue().strip()
        self.assertIn("Changed directory to /dir1", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cd4(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/dir1/": 'dir',
            "/dir2/": 'dir',
            "/file1.txt": 'file',
        }
        emulator.cwd = "/"
        emulator.cmd_cd("/dir2")
        output = mock_stdout.getvalue().strip()
        self.assertIn("Changed directory to /dir2", output)
    @patch("sys.stdout", new_callable=StringIO)
    def test_date(self, mock_stdout):
        """Тест на команду date"""
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.cmd_date()
        output = mock_stdout.getvalue().strip()
        self.assertRegex(output, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    @patch("sys.stdout", new_callable=StringIO)
    def test_mkdir(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/dir1/": 'dir',
        }
        emulator.cmd_mkdir("dir2")
        self.assertIn("/dir2/", emulator.vfs)
        emulator.cmd_mkdir("dir1")
        output = mock_stdout.getvalue().strip()
        self.assertIn("mkdir: cannot create directory 'dir1': File exists", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_tac(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/file1.txt": 'file',}
        with patch("zipfile.ZipFile.open", return_value=StringIO("line1\nline2\nline3\n")):
            emulator.cmd_tac("file1.txt")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "line3\n\nline2\n\nline1")

    @patch("sys.stdout", new_callable=StringIO)
    def test_tac2(self, mock_stdout):
        emulator = ShellEmulator("test_user", "C:/Users/User/vfs.zip", None)
        emulator.vfs = {
            "/file1.txt": 'file',}
        with patch("zipfile.ZipFile.open", return_value=StringIO("line3\nline2\nline1\n")):
            emulator.cmd_tac("file1.txt")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "line1\n\nline2\n\nline3")

if __name__ == "__main__":
    unittest.main()
