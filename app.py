from flask import Flask, render_template, request
from prediction import get_rubber_shim_data, get_customer_feedback_data, predict_breakage

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/rubber_shim_data')
def rubber_shim_data():
    data = get_rubber_shim_data()
    return render_template('rubber_shim_data.html', production_data=data)

@app.route('/customer_feedback')
def customer_feedback():
    data = get_customer_feedback_data()
    return render_template('customer_feedback.html', feedback_data=data)

@app.route('/predict', methods=['POST'])
def predict():
    diameter = float(request.form.get('diameter', 0))
    screw_params = request.form.get('screw_params', 'Type A')
    handlebar_width = float(request.form.get('handlebar_width', 0))

    breakage = predict_breakage(diameter, screw_params, handlebar_width)
    result = "likely to break" if breakage else "unlikely to break"

    return render_template('predict.html', diameter=diameter, screw_params=screw_params, handlebar_width=handlebar_width, result=result)

if __name__ == '__main__':
    app.run(debug=True)
