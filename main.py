import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import subprocess

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")
        self.text_area = tk.Text(self.root, bg="#1a1d23", fg="white", font=("Arial", 12), wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.file_name = ""
        self.syntax_highlight()

        self.menubar = tk.Menu(self.root, bg="#1a1d23", fg="white")
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_code, bg="#4c5154", fg="white")
        self.run_button.pack(side=tk.LEFT)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_code, bg="#4c5154", fg="white")
        self.edit_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_file, bg="#4c5154", fg="white")
        self.save_button.pack(side=tk.LEFT)

        self.help_button = tk.Button(self.root, text="Help", command=self.help, bg="#4c5154", fg="white")
        self.help_button.pack(side=tk.LEFT)

        self.root.config(menu=self.menubar)

    def open_file(self):
        self.file_name = filedialog.askopenfilename()
        if self.file_name:
            with open(self.file_name, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)

    def save_file(self):
        if self.file_name:
            with open(self.file_name, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Success", "File saved successfully!")

    def save_as_file(self):
        self.file_name = filedialog.asksaveasfilename()
        if self.file_name:
            with open(self.file_name, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Success", "File saved successfully!")

    def exit(self):
        self.root.destroy()

    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        try:
            process = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode()
            error = process.stderr.read().decode()
            if output:
                self.text_area.insert(tk.END, output + '\n')
            if error:
                messagebox.showerror("Error", error)
            messagebox.showinfo("Success", "Code executed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_code(self):
        code = self.text_area.get(1.0, tk.END)
        # Implement code editing functionality here
        pass

    def help(self):
        # Implement help functionality here
        pass

    def syntax_highlight(self):
        # Implement syntax highlighting functionality here
        pass

class ExecutionPanel:
    def __init__(self, root, code_editor):
        self.root = root
        self.code_editor = code_editor
        self.terminal = tk.Text(self.root, bg="#1a1d23", fg="white", font=("Arial", 12))
        self.terminal.pack(fill=tk.BOTH, expand=1)

    def run_code(self):
        code = self.code_editor.text_area.get(1.0, tk.END)
        try:
            process = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode()
            error = process.stderr.read().decode()
            if output:
                output_thread = Thread(target=self.insert_output_to_terminal, args=(output,))
                output_thread.start()
            if error:
                messagebox.showerror("Error", error)
            messagebox.showinfo("Success", "Code executed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_output_to_terminal(self, output):
        for line in output.splitlines():
            line += '\n'
            if line != '\n':
                self.code_editor.terminal.insert(tk.END, line)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1a1d23")
    root.title("Python IDE")
    code_editor = CodeEditor(root)
    execution_panel = ExecutionPanel(root, code_editor)
    root.mainloop()
