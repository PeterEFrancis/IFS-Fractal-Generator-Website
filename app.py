from flask import Flask, render_template, url_for, redirect
import re
import random
import html
import os
from IFSFGL import *
import sys


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/generator/')
@app.route('/generator')
def generator():
    return render_template('generator.html')

@app.route('/output/name=<string:name>/transformations=<string:transformations>/weights=<string:weights>/size=<int:size>/color=<string:color>/number=<int:number>')
def output(name, transformations, weights, size, color, number):
    try:
        name = name.replace(' ', '') + '_' + str(int(time.time()))
        transformations = [eval(func.replace('&','@').replace('FS','/')) for func in re.split('>', transformations)[1:]]

        opnormMSG = check_transformations(transformations)

        weights = np.array([eval(num) for num in re.split(',', weights)])
        color = eval(color)

        myFractal = Fractal(transformations, weights=weights, size=size, color=color)
        myFractal.add_points(number)
        myFractal.save_pic(f'static/{name}.png')

    except:
        error = sys.exc_info()
        return render_template('output.html', name=name, transformations=transformations, weights=weights, size=size, color=color, number=number, URL = url_for('static', filename=name + '.png'), opnormMSG=opnormMSG, error=error)

    return render_template('output.html', name=name, transformations=transformations, weights=weights, size=size, color=color, number=number, URL = url_for('static', filename=name + '.png'), opnormMSG=opnormMSG)




@app.route('/crab_example')
def crab():
    C1 = Translate(0.5,0.15) @ Rotate(np.pi/4) @ Scale(1/4)
    C2 = Scale(1/2)
    C3 = Translate(-.5,0.15) @ Rotate(-np.pi/4) @ Scale(1/4)
    C4 = Rotate(-np.pi/6) @ Scale(1/2)
    C5 = Rotate(np.pi/6) @ Scale(1/2)

    CT = [C1, C2, C3, C4, C5]

    crab = Fractal(CT, size=20)

    crab.add_points(1_000_000)
    crab.save_pic(path='static/Crab.png')

    return render_template('generator.html', URL=url_for('static', filename='Crab.png'))



if __name__ == "__main__":
    app.run(port=5002)
