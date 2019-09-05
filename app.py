from flask import Flask, render_template, url_for, redirect
import re
import random
import html
import os
import sys

from IFSFGL import *
# from RFG import *

app = Flask(__name__)

if not os.path.exists("static/saved_fractals"):
    os.makedirs("static/saved_fractals")


@app.route('/master_list')
def master():
    pictureDictionary = {}
    generatorLinkDictionary = {}
    # try:
    # find URLS for saved images
    for file in os.listdir('static/saved_fractals/'):
        if os.fsdecode(file).endswith('.png'):
            pictureDictionary[os.fsdecode(file)[:-4]] = url_for('static', filename= 'saved_fractals/' + os.fsdecode(file))

    # read in link list
    text = ''.join(line.strip() for line in open('static/saved_fractals/links.txt','r').readlines())
    for line in re.split('!', text.strip()):
        if r'<' in line:
            both = re.split(r'<', line)
            generatorLinkDictionary[both[0].strip()] = re.sub(' ', '', both[1].strip())

    # except:
    #     error = sys.exc_info()[1]
    #     return render_template('error.html', error=error)
    return render_template('master.html', pictureDictionary=pictureDictionary, generatorLinkDictionary=generatorLinkDictionary)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/generator/full')
@app.route('/generator')
def generator_full():
    return render_template('generator.html')

@app.route('/generator/word_fractal')
def generator_word_fractal():
    return render_template('word_fractal.html')



# @app.route('/random_fractal')
# def random():
#     name, transformations, transformations, weights= random_fractal()
#
#     size = 10
#     color = '(0,0,255)'
#     number = 100_000
#
#     return redirect(f'/output/name={name}/transformations={transformations}/weights={weights}>/size={size}/color={color}/number={number}')



@app.route('/output/word_fractal/name=<string:name>/word=<string:word>/size=<int:size>/color=<string:color>/number=<int:number>')
def word(name, word, size, color, number):
    transformations = []
    try:
        # Check Name
        if name == 'None':
            raise ValueError('Web_Generator in app.py output(): You must name your fractal.')
        else:
            name = name.replace(' ', '') + '_' + str(int(time.time()))

        # Check word
        if word == 'None':
            raise ValueError('app.py in word(): You must give the generator a word for your fractal.')
        else:
            transformations = word_fractal(word)

        # make weights
        weights = make_eq_weights(len(transformations)) # take care of it here since we have to send to output.html

        #check size

        # check color
        if color == 'None':
            color = (0,0,255)
        else:
            color = eval(color)

        # check number
        if number==0:
            number = 100_000


        opNormMess = check_transformations(transformations)

        myFractal = Fractal(transformations, weights=weights, size=size, color=color)
        myFractal.add_points(number)

        myFractal.save_pic(f'static/saved_fractals/{name}.png')

        with open('static/saved_fractals/links.txt', 'a') as links:
            links.write(f'{name} < ' + re.sub('\n', '', re.sub(' ', '', f"/output/word_fractal/name={name[:-11]}/word={word}/size={size}/color={color}/number={number}")) + '\n ! \n\n')


        length=len(transformations)

    except:
        error = sys.exc_info()[1]
        return render_template('error.html', error=error)
    return render_template('output.html', name=name, transformations=transformations, weights=weights, size=size, color=color, number=number, URL = url_for('static', filename='saved_fractals/' + name + '.png'), opNormMess=opNormMess, length=length)





@app.route('/output/name=<string:name>/transformations=<string:transformations>/weights=<string:weights>/size=<int:size>/color=<string:color>/number=<int:number>')
def output(name, transformations, weights, size, color, number):
    try:
        # Check Name
        if name == 'None':
            raise ValueError('app.py in output(): You must name your fractal.')
        else:
            name = name.replace(' ', '') + '_' + str(int(time.time()))

        # Check transformations
        if transformations == 'None': # leave error message for IFSFGL
            transformations = None
        else:
            transformations = [eval(func.replace('&','@').replace('FS','/')) for func in re.split('>', transformations)]

        # check weights
        if weights == 'None':
            weights = make_eq_weights(len(transformations)) # take care of it here since we have to send to output.html
        else:
            weights = np.array([eval(num) for num in re.split(',', weights)])

        #check size

        # check color
        if color == 'None':
            color = (0,0,255)
        else:
            color = eval(color)

        # check number
        if number==0:
            number = 100_000

        opNormMess = check_transformations(transformations)

        myFractal = Fractal(transformations, weights=weights, size=size, color=color)
        myFractal.add_points(number)
        myFractal.save_pic(f'static/saved_fractals/{name}.png')

        with open('static/saved_fractals/links.txt', 'a') as links:
            links.write(f'{name} < ' + re.sub('\n', '', re.sub(' ', '', f"/output/name={name[:-11]}/transformations={transformations}/weights={weights}/size={size}/color={color}/number={number}")) + '\n ! \n\n')


        length=len(weights)

    except:
        error = sys.exc_info()[1]
        return render_template('error.html', error=error)

    return render_template('output.html', name=name, transformations=transformations, weights=weights, size=size, color=color, number=number, URL = url_for('static', filename='saved_fractals/' + name + '.png'), opNormMess=opNormMess, length=length)


if __name__ == "__main__":
    app.run(port=5002)
