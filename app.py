from flask import Flask, render_template, request
import tkinter as tk
import sympy as sp

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        # Tangani input pengguna dan hitung hasilnya
        expression = request.form['expression']
        result = calculate_expression(expression)
        return render_template('calculator.html', result=result)
    return render_template('calculator.html')

def calculate_expression(expression):
    # Implementasikan logika perhitungan di sini
    # Anda dapat menggunakan library sympy untuk mengevaluasi ekspresi
    pass

if __name__ == '__main__':
    app.run(debug=True)