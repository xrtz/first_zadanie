# import zipfile
# from datetime import datetime
# from tkinter import Tk, Text, Entry, Button, Label, END
# import argparse
#
# class ShellEmulator:
#     def __init__(self, username, vfs_zip_path, script_path):
#         self.username = username
#         self.vfs_zip_path = vfs_zip_path
#         self.script_path = script_path
#         self.cwd = "/"
#         self.vfs = {}
#         self.load_vfs()
#         self.run_start_script(script_path)
#
#     def load_vfs(self):
#         with zipfile.ZipFile(self.vfs_zip_path, 'r') as archive:
#             for file_info in archive.infolist():
#                 path = file_info.filename
#                 if not path.startswith('/'):
#                     path = '/' + path
#                 if path.endswith('/'):
#                     self.vfs[path] = 'dir'
#                 else:
#                     self.vfs[path] = 'file'
#
#     def run_start_script(self, script_path):
#         if not script_path:
#             return
#         try:
#             with open(script_path, 'r') as script:
#                 for line in script:
#                     self.execute_command(line.strip(), True)
#         except FileNotFoundError:
#             print(f"Start script not found: {script_path}")
#
#     def execute_command(self, command, from_script=False):
#         args = command.split()
#         if not args:
#             return
#         cmd, *params = args
#         if cmd == "ls":
#             self.cmd_ls()
#         elif cmd == "cd":
#             self.cmd_cd(params[0] if params else "")
#         elif cmd == "exit":
#             if not from_script:
#                 exit(0)
#         elif cmd == "date":
#             self.cmd_date()
#         elif cmd == "mkdir":
#             self.cmd_mkdir(params[0] if params else "")
#         elif cmd == "tac":
#             self.cmd_tac(params[0] if params else "")
#         else:
#             print(f"Команда не найдена: {cmd}")
#
#     def cmd_ls(self):
#         content = []
#         prefix_length = len(self.cwd.rstrip('/')) + 1
#         for path, type_ in self.vfs.items():
#             if path.startswith(self.cwd) and path != self.cwd:
#                 relative_path = path[prefix_length:]
#                 # Добавляем только первый уровень (игнорируем вложенные элементы)
#                 if '/' in relative_path.strip('/'):
#                     continue
#                 content.append(relative_path)
#         if content:
#             for item in content:
#                 print(item)
#         else:
#             print("Directory is empty")
#
#     def cmd_cd(self, path):
#         if path in ["", "/"]:
#             self.cwd = "/"
#             print(f"Changed directory to {self.cwd}")
#             return
#         if not path.startswith('/'):
#             path = self.cwd.rstrip('/') + '/' + path
#         if path.endswith('/'):
#             target = path
#         else:
#             target = path + '/'
#         if target in self.vfs and self.vfs[target] == 'dir':
#             self.cwd = target
#             print(f"Changed directory to {self.cwd}")
#         else:
#             print(f"cd: {path}: No such directory")
#
#     def cmd_date(self, *args):
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#     def cmd_mkdir(self, dirname):
#         if not dirname:
#             print("mkdir: missing directory name")
#             return
#         if not dirname.startswith('/'):
#             dirpath = self.cwd.rstrip('/') + '/' + dirname
#         else:
#             dirpath = dirname
#         if not dirpath.endswith('/'):
#             dirpath += '/'
#         if dirpath in self.vfs:
#             print(f"mkdir: cannot create directory '{dirname}': File exists")
#         else:
#             self.vfs[dirpath] = 'dir'
#             print(f"Directory '{dirname}' created")
#
#     def cmd_tac(self, filename):
#         if not filename.startswith('/'):
#             filepath = self.cwd.rstrip('/') + '/' + filename
#         else:
#             filepath = filename
#         if filepath in self.vfs and self.vfs[filepath] == 'file':
#             with zipfile.ZipFile(self.vfs_zip_path, 'r') as archive:
#                 with archive.open(filepath.lstrip('/'), 'r') as file:
#                     lines = file.readlines()
#                     for line in reversed(lines):
#                         if isinstance(line, bytes):
#                             print(line.decode().strip())
#                         else:
#                             print(line.strip())
#         else:
#             print(f"tac: {filename}: No such file")
#
#     def start_gui(self):
#         root = Tk()
#         root.title("Shell Emulator")
#         output = Text(root, height=20, width=80, bg="black", fg="white")
#         output.pack()
#         def process_command(event=None):
#             command = command_entry.get()
#             output.insert(END, f"{self.username}@shell:{self.cwd}$ {command}\n")
#             command_entry.delete(0, END)
#             self.execute_command(command)
#         command_entry = Entry(root, width=80)
#         command_entry.bind("<Return>", process_command)
#         command_entry.pack()
#         Label(root, text=f"User: {self.username}").pack(side="left")
#         root.mainloop()
#
#
# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--user", required=True)
#     parser.add_argument("--vfs", required=True)
#     parser.add_argument("--script", required=False)
#     args = parser.parse_args()
#     emulator = ShellEmulator(args.user, args.vfs, args.script)
#     emulator.start_gui()
#
# if __name__ == "__main__":
#     ##python C:\Users\User\PycharmProjects\PythonProject1\emulator.py --user test_user --vfs C:\Users\User\vfs.zip --script C:\Users\User\PycharmProjects\PythonProject1\start_script.sh
#     main()
import zipfile
from datetime import datetime
from tkinter import Tk, Text, Entry, Button, Label, END
import argparse

class ShellEmulator:
    def __init__(self, username, vfs_zip_path, script_path):
        self.username = username
        self.vfs_zip_path = vfs_zip_path
        self.script_path = script_path
        self.cwd = "/"
        self.vfs = {}
        self.output_widget = None
        self.load_vfs()
        self.run_start_script(script_path)
        self.color = "white"

    def load_vfs(self):
        with zipfile.ZipFile(self.vfs_zip_path, 'r') as archive:
            for file_info in archive.infolist():
                path = file_info.filename
                if not path.startswith('/'):
                    path = '/' + path
                if path.endswith('/'):
                    self.vfs[path] = 'dir'
                else:
                    self.vfs[path] = 'file'

    def run_start_script(self, script_path):
        if not script_path:
            return
        try:
            with open(script_path, 'r') as script:
                for line in script:
                    self.execute_command(line.strip(), True)
        except FileNotFoundError:
            self.write_output(f"Start script not found: {script_path}\n")

    def write_output(self, text):
        """Вывод текста в виджет с указанием цвета."""
        if self.output_widget:
            self.output_widget.tag_configure(self.color, foreground=self.color)
            self.output_widget.insert(END, text, self.color)
            self.output_widget.see(END)
        else:
            print(text)

    def execute_command(self, command, from_script=False):
        args = command.split()
        if not args:
            return
        cmd, *params = args
        if cmd == "ls":
            self.cmd_ls()
        elif cmd == "cd":
            self.cmd_cd(params[0] if params else "")
        elif cmd == "exit":
            if not from_script:
                exit(0)
        elif cmd == "date":
            self.cmd_date()
        elif cmd == "mkdir":
            self.cmd_mkdir(params[0] if params else "")
        elif cmd == "tac":
            self.cmd_tac(params[0] if params else "")
        elif cmd == "color":
            self.cmd_color(params)
        else:
            self.write_output(f"Command not found: {cmd}\n"
                              )

    def cmd_ls(self):
        content = []
        prefix_length = len(self.cwd.rstrip('/')) + 1
        for path, type_ in self.vfs.items():
            if path.startswith(self.cwd) and path != self.cwd:
                relative_path = path[prefix_length:]
                if '/' in relative_path.strip('/'):
                    continue
                content.append(relative_path)
        if content:
            for item in content:
                self.write_output(f"{item}\n")
        else:
            self.write_output("Directory is empty\n")

    def cmd_cd(self, path):
        if path in ["", "/"]:
            self.cwd = "/"
            self.write_output(f"Changed directory to {self.cwd}\n")
            return
        if not path.startswith('/'):
            path = self.cwd.rstrip('/') + '/' + path
        if path.endswith('/'):
            target = path
        else:
            target = path + '/'
        if target in self.vfs and self.vfs[target] == 'dir':
            self.cwd = target
            self.write_output(f"Changed directory to {self.cwd}\n")
        else:
            self.write_output(f"cd: {path}: No directory\n")

    def cmd_date(self, *args):
        self.write_output(datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))

    def cmd_mkdir(self, dirname):
        if not dirname:
            self.write_output("mkdir: missing directory name\n")
            return
        if not dirname.startswith('/'):
            dirpath = self.cwd.rstrip('/') + '/' + dirname
        else:
            dirpath = dirname
        if not dirpath.endswith('/'):
            dirpath += '/'
        if dirpath in self.vfs:
            self.write_output(f"mkdir: cannot create directory '{dirname}': File exists\n")
        else:
            self.vfs[dirpath] = 'dir'
            self.write_output(f"Directory '{dirname}' created\n")

    def cmd_tac(self, filename):
        if not filename.startswith('/'):
            filepath = self.cwd.rstrip('/') + '/' + filename
        else:
            filepath = filename
        if filepath in self.vfs and self.vfs[filepath] == 'file':
            with zipfile.ZipFile(self.vfs_zip_path, 'r') as archive:
                with archive.open(filepath.lstrip('/'), 'r') as file:
                    lines = file.readlines()
                    for line in reversed(lines):
                        if isinstance(line, bytes):
                            self.write_output(line.decode().strip() + "\n")
                        else:
                            self.write_output(line.strip() + "\n")
        else:
            self.write_output(f"tac: {filename}: No such file\n")

    def cmd_color(self, params):
        if not params:
            self.write_output("Usage: color <color> <text>\n")
            return
        self.color = params


    def start_gui(self):
        root = Tk()
        root.title("Shell Emulator")
        self.output_widget = Text(root, height=20, width=80, bg="black", fg="white")
        self.output_widget.pack()

        def process_command(event=None):
            command = command_entry.get()
            self.write_output(f"{self.username}@shell:{self.cwd}$ {command}\n")
            command_entry.delete(0, END)
            self.execute_command(command)

        command_entry = Entry(root, width=80)
        command_entry.bind("<Return>", process_command)
        command_entry.pack()
        Label(root, text=f"User: {self.username}").pack(side="left")
        root.mainloop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--vfs", required=True)
    parser.add_argument("--script", required=False)
    args = parser.parse_args()
    emulator = ShellEmulator(args.user, args.vfs, args.script)
    emulator.start_gui()


if __name__ == "__main__":
    main()
