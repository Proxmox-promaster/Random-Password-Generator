import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x500")
        self.file_path = "history.json"

        # Настройки пароля
        tk.Label(root, text="Длина пароля:").pack(pady=5)
        self.len_slider = tk.Scale(root, from_=4, to_=32, orient="horizontal")
        self.len_slider.set(12)
        self.len_slider.pack(pady=5)

        self.use_upper = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Заглавные буквы", variable=self.use_upper).pack()

        self.use_digits = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Цифры", variable=self.use_digits).pack()

        self.use_spec = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Спецсимволы", variable=self.use_spec).pack()

        # Кнопка и вывод
        tk.Button(root, text="Сгенерировать", command=self.generate).pack(pady=10)
        self.res_entry = tk.Entry(root, font=("Arial", 12), justify="center")
        self.res_entry.pack(pady=5, fill="x", padx=20)

        # История
        tk.Label(root, text="История (последние 10):").pack(pady=10)
        self.hist_list = tk.Listbox(root, height=8)
        self.hist_list.pack(pady=5, fill="both", padx=20)

        self.load_history()

    def generate(self):
        length = self.len_slider.get()
        chars = string.ascii_lowercase
        if self.use_upper.get(): chars += string.ascii_uppercase
        if self.use_digits.get(): chars += string.digits
        if self.use_spec.get(): chars += string.punctuation

        password = "".join(random.choice(chars) for _ in range(length))
        
        self.res_entry.delete(0, tk.END)
        self.res_entry.insert(0, password)
        self.save_history(password)

    def save_history(self, pwd):
        history = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                history = json.load(f)
        
        history.append(pwd)
        history = history[-10:] # Ограничение 10 записей
        
        with open(self.file_path, "w") as f:
            json.dump(history, f)
        
        self.update_listbox(history)

    def load_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.update_listbox(json.load(f))

    def update_listbox(self, history):
        self.hist_list.delete(0, tk.END)
        for p in reversed(history):
            self.hist_list.insert(tk.END, p)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
