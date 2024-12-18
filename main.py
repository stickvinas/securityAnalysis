from flask import Flask, redirect, render_template, request, send_from_directory
from flask_cors import CORS

from calc_and_draw_pc import CalculationDrawServicePC

app = Flask(__name__)
CORS(app, origins="*")

calcS_pc = CalculationDrawServicePC()


@app.route('/check')
def check():
    return "check"


@app.route('/')
def index():
    return render_template('lab4.html')


@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

@app.route('/calcAndDraw_pc', methods=['POST'])
def calc_and_draw_pc():
    #  Получение данных с фронт энда
    content = request.json
    X, Y = calcS_pc.calculate(content)
    
    print("Received data:", content)
    
    # Отрисовка графиков
    path1, path2 = calcS_pc.save_plots(Y)
    
    print("Sending response with image paths:", path1, path2)  

    return {
        "image1": path1,
        "image2": path2
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
