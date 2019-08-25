from flask import Flask, render_template, url_for, redirect
import re
import random
import html
import os
from IFSFGL import *


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/generator')
def choose():
    C1 = Translate(0.5,0.15) @ Rotate(np.pi/4) @ Scale(1/4)
    C2 = Scale(1/2)
    C3 = Translate(-.5,0.15) @ Rotate(-np.pi/4) @ Scale(1/4)
    C4 = Rotate(-np.pi/6) @ Scale(1/2)
    C5 = Rotate(np.pi/6) @ Scale(1/2)

    CT = [C1, C2, C3, C4, C5]

    crab = Fractal(CT)

    crab.add_points(1_000_000)
    crab.save_pic()

    return render_template('generator.html', name='Trash')



if __name__ == "__main__":
    app.run(port=5002)
