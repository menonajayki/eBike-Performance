from flask import Flask, render_template, request
from prediction import get_performance_data, predict_maintenance

app = Flask(__name__)


@app.route('/')
def dashboard():
    data = get_performance_data()
    return render_template('dashboard.html', data=data)


@app.route('/predict', methods=['POST'])
def predict():
    value = float(request.form.get('value', 0))
    threshold = float(request.form.get('threshold', 0))
    component_type = request.form.get('component_type', 'Unknown')
    needs_maintenance = predict_maintenance(value, threshold)
    result = "needs maintenance" if needs_maintenance else "does not need maintenance"

    return render_template('predict.html', value=value, threshold=threshold, result=result,
                           component_type=component_type)


if __name__ == '__main__':
    app.run(debug=True)
