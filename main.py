import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from pygments import lex, highlight
from pygments.lexers import PythonLexer
from pygments.styles import get_all_styles

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
        self.style_names = get_all_styles()
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
                self.syntax_highlight()

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
            exec(code)
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
        code = self.text_area.get(1.0, tk.END)
        lexer = PythonLexer()
        formatter = HtmlFormatter()
        highlighted_code = highlight(code, lexer, formatter)
        style_names = find_style_names()
        highlighted_code.splitlines()
        for i in range(len(highlighted_code)):
            line_number = i + 1
            line_contents = highlighted_code.splitlines()[i]
            if line_contents.startswith('def '):
                line_contents = '<span style="color:blue;">' + line_contents + '</span>'
            elif line_contents.startswith('class '):
                line_contents = '<span style="color:purple;">' + line_contents + '</span>'
            elif line_contents.startswith('print'):
                line_contents = '<span style="color:orange;">' + line_contents + '</span>'
            elif line_contents.startswith('if ') or line_contents.startswith('for ') or line_contents.startswith('while '):
                line_contents = '<span style="color:green;">' + line_contents + '</span>'
            else:
                line_contents = '<span style="color:black;">' + line_contents + '</span>'
            self.text_area.insert(tk.END, str(line_number) + ' ' + line_contents + '\n')
            if i < len(highlighted_code) - 1:
                self.text_area.insert(tk.END, '\n')
                
                
class ExecutionPanel:
    def __init__(self, root, code_editor):
        self.root = root
        self.code_editor = code_editor
        self.terminal = tk.Text(self.root)
        self.terminal.pack(fill=tk.BOTH, expand=1)

    def run_code(self):
        code = self.code_editor.text_area.get(1.0, tk.END)
        try:
            output = eval(code)
            if isinstance(output, str):
                output = output + '\n'
            else:
                output = str(output) + '\n'
            self.terminal.insert(tk.END, output)
            messagebox.showinfo("Success", "Code executed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    code_editor = CodeEditor(root)
    execution_panel = ExecutionPanel(root, code_editor)
    root.mainloop()
