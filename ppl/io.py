import tkinter as tk
import sys


SIZE = 35


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('PPL')
        self.geometry("290x1200")
        self.text = tk.Text(self, wrap="word", width=SIZE)
        self.text.place(relheight=.45)
        #self.text.pack(side="top", pady=5, padx=5, expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")

        self.text_instance = tk.Text(self, wrap="word",  width=SIZE)
        self.text_instance.place(relheight=.45, rely=.45)

        self.text_instance.tag_configure("stderr", foreground="#b22222")

        self.entry = tk.Entry(self,  width=SIZE)
        self.msg = tk.Label(self, text='')

        self.msg.place(relheight=.05, rely=.90)
        self.entry.place(relheight=.05, rely=.95)


app = ExampleApp()


def write(s):
    app.text.configure(state="normal")
    app.text.delete(1.0, tk.END)
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
