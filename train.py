import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

data = pd.read_csv('rubber_shim_data.csv')

label_encoder = LabelEncoder()
data['ScrewParams'] = label_encoder.fit_transform(data['ScrewParams'])

X = data[['Diameter', 'HandlebarWidth', 'ScrewParams']]
y = data['Breakage']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open('rubber_shim_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('screw_params_encoder.pkl', 'wb') as encoder_file:
    pickle.dump(label_encoder, encoder_file)

print("Model and encoder saved successfully.")
