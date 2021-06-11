import tkinter as tk
import sys


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('PPL')
        frame = tk.Frame(self, width=800)
        frame.pack(side="top",  fill='x')
        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="left", pady=5, padx=5, fill='both', expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")

        self.text_instance = tk.Text(self, wrap="word")
        self.text_instance.pack(
            side="top", pady=5, padx='5', fill='both', expand=True)

        self.text_instance.tag_configure("stderr", foreground="#b22222")

        self.entry = tk.Entry(self)
        self.msg = tk.Label(self, text='')

        self.msg.pack(side="top")
        self.entry.pack(side="bottom", fill="both",
                        expand=True,  pady=5, padx=5)


app = ExampleApp()


def write(s):
    app.text.configure(state="normal")
    app.text.insert("end", f'{s}\n', ('stdout', ))
    app.text.configure(state="disabled")


def write_instance(s):
    app.text_instance.configure(state="normal")
    app.text_instance.delete(1.0, tk.END)
    app.text_instance.insert("end", f'{s}\n', ('stdout', ))
    app.text_instance.configure(state="disabled")


def get_input(msg):
    res = tk.StringVar(value='')
    app.msg.config(text=msg)

    def evaluate(event):
        res.set(str(app.entry.get()))
    app.entry.bind('<Return>', evaluate)

    app.wait_variable(res)
    app.entry.delete(0, tk.END)
    return res.get()
