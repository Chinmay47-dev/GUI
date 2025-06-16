from flask import Flask, render_template, request
from low1 import update_graph
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        motor_data = {
            "frequency": request.form.get('frequency'),
            "voltage": request.form.get('voltage'),
            "power": request.form.get('power'),
            "current": request.form.get('current'),
            "rpm": request.form.get('rpm'),
            "pf": request.form.get('pf')
        }
        # You can process motor_data here if needed
    
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
    
