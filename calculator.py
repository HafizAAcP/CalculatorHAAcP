import tkinter as tk
import sympy as sp

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        self.expression = ""
        self.text_input = tk.StringVar()
        self.history = []

        self.entry = tk.Entry(root, textvariable=self.text_input, font=('Arial', 20, 'bold'), bd=30, insertwidth=4, width=18, borderwidth=4)
        self.entry.grid(row=0, column=0, columnspan=6)

        # Listbox untuk histori
        self.history_listbox = tk.Listbox(root, font=('Arial', 12))
        self.history_listbox.grid(row=1, column=6, rowspan=6, padx=(10, 0), pady=(5, 0))

        # Tombol untuk menghapus histori
        self.clear_history_button = tk.Button(root, text="Clear History", font=('Arial', 12), command=self.clear_history)
        self.clear_history_button.grid(row=7, column=6, padx=(10, 0), pady=(5, 0))

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/', 'AC', 'DEL',
            '4', '5', '6', '*', '(', ')',
            '1', '2', '3', '-', '%', 'π',
            '0', ',', '=', '+', '√1', '√2',
            '√3', '√4', '√5', '^', '^1', '^2', '^3', '^4', '^5',
            '^6', '^7', '^8', '^9', '^10', '^0',
            'ANS', 'exp', 'tan', 'e', 'log', 'cos',
            'ln', 'sin', 'inv', '!'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            self.create_button(button, row_val, col_val)
            col_val += 1
            if col_val > 5:
                col_val = 0
                row_val += 1

    def create_button(self, value, row, col):
        button = tk.Button(self.root, text=value, padx=20, pady=20, font=('Arial', 18, 'bold'), 
                           command=lambda: self.button_click(value))
        button.grid(row=row, column=col)

    def button_click(self, value):
        if value == "=":
            try:
                expression_to_evaluate = self.expression.replace(',', '.')
                expression_to_evaluate = expression_to_evaluate.replace('%', '/100')
                expression_sympy = sp.sympify(expression_to_evaluate)
                total = expression_sympy.evalf()
                formatted_total = self.format_number(total)

                # Simpan ke histori
                history_entry = f"{self.expression} = {formatted_total}"
                self.history.append(history_entry)
                self.history_listbox.insert(tk.END, history_entry)

                self.text_input.set(formatted_total)
                self.expression = formatted_total
            except Exception as e:
                self.text_input.set("Error")
                self.expression = ""
        elif value == "AC":
            self.expression = ""
            self.text_input.set("")
        elif value == "DEL":
            self.expression = self.expression[:-1]
            self.text_input.set(self.expression)
        elif value == "π":
            self.expression += str(sp.pi.evalf()).replace('.', ',')
            self.text_input.set(self.expression)
        elif value == "ANS":
            if self.history:
                ans_value = self.history[-1].split('=')[1].strip()
                if self.expression and self.expression[-1].isdigit():
                    self.expression += f"*{ans_value}"
                else:
                    self.expression += ans_value
                self.text_input.set(self.expression)
        elif value == "exp":
            self.expression += str(sp.exp(1).evalf()).replace('.', ',')
            self.text_input.set(self.expression)
        elif value == "!":
            try:
                num = int(self.expression.replace(',', '.'))
                result = sp.factorial(num)
                formatted_result = self.format_number(result.evalf())
                self.text_input.set(formatted_result)
                self.expression = formatted_result
            except Exception as e:
                self.text_input.set("Error")
                self.expression = ""
        elif value in ["sin", "cos", "tan", "log", "ln", "inv"]:
            try:
                if value == "sin":
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = sp.sin(num).evalf()
                elif value == "cos":
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = sp.cos(num).evalf()
                elif value == "tan":
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = sp.tan(num).evalf()
                elif value == "log":
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = sp.log(num, 10).evalf()
                elif value == "ln":
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = sp.ln(num).evalf()
                elif value == "inv":
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = 1 / num
                formatted_result = self.format_number(result)
                self.text_input.set(formatted_result)
                self.expression = formatted_result
            except Exception as e:
                self.text_input.set("Error")
                self.expression = ""
        elif value == "^":
            self.expression += "^"
            self.text_input.set(self.expression)
        elif value.startswith('√'):
            try:
                degree = int(value[1])
                num = sp.sympify(self.expression.replace(',', '.'))
                if num < 0 and degree % 2 == 0:
                    raise ValueError("Even root of negative number")
                result = num ** (1 / degree)
                formatted_result = self.format_number(result.evalf())
                self.text_input.set(formatted_result)
                self.expression = formatted_result
            except Exception as e:
                self.text_input.set("Error")
                self.expression = ""
        elif value.startswith('^'):
            try:
                degree = int(value[1:])
                if degree == 0:
                    self.expression = "1"
                    self.text_input.set("1")
                else:
                    num = sp.sympify(self.expression.replace(',', '.'))
                    result = num ** degree
                    formatted_result = self.format_number(result.evalf())
                    self.text_input.set(formatted_result)
                    self.expression = formatted_result
            except Exception as e:
                self.text_input.set("Error")
                self.expression = ""
        else:
            self.expression += str(value)
            self.text_input.set(self.expression)

    def format_number(self, number):
        number_str = f"{number:.10f}"  # Format to avoid scientific notation
        parts = number_str.split('.')
        integer_part = parts[0]
        decimal_part = parts[1].rstrip('0')  # Remove trailing zeros

        formatted_integer_part = f"{int(integer_part):,}".replace(',', '.')

        if not decimal_part:
            return formatted_integer_part  # Format integer part only

        return f"{formatted_integer_part},{decimal_part}"

    def clear_history(self):
        self.history_listbox.delete(0, tk.END)
        self.history.clear()

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
