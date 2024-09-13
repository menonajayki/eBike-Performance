import pandas as pd
import random
from datetime import datetime, timedelta

n_samples = 10000

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_rubber_shim_data(n):
    diameters = [random.randint(20, 40) for _ in range(n)]
    months = [random_date(datetime(2022, 1, 1), datetime(2024, 1, 1)).strftime('%Y-%m') for _ in range(n)]
    screw_types = ['Type A', 'Type B', 'Type C']
    screw_sizes = [random.choice(screw_types) + f' / {random.randint(4, 6)}mm' for _ in range(n)]
    handlebar_widths = [random.randint(640, 800) for _ in range(n)]

    return pd.DataFrame({
        'ShimID': range(1, n+1),
        'Diameter (mm)': diameters,
        'Production Month': months,
        'Screw Parameters': screw_sizes,
        'Handlebar Width (mm)': handlebar_widths
    })

def generate_feedback_data(rubber_shim_df):
    feedback_list = []
    breakage_list = []

    for _, row in rubber_shim_df.iterrows():
        diameter = row['Diameter (mm)']
        screw = row['Screw Parameters'].split('/')[0].strip()
        handlebar_width = row['Handlebar Width (mm)']

        if diameter > 30 or screw == 'Type B':
            breakage = random.choices([True, False], weights=[0.7, 0.3])[0]
        else:
            breakage = random.choices([True, False], weights=[0.2, 0.8])[0]

        # Generate customer feedback
        feedback = "Positive, no issues" if not breakage else random.choice([
            "Shim broke after 2 months", "Crack appeared", "Shim worn out quickly"
        ])

        feedback_list.append(feedback)
        breakage_list.append("Yes" if breakage else "No")

    return pd.DataFrame({
        'ShimID': rubber_shim_df['ShimID'],
        'Customer Feedback': feedback_list,
        'Breakage (Yes/No)': breakage_list
    })

# Generate and save datasets
rubber_shim_data = generate_rubber_shim_data(n_samples)
feedback_data = generate_feedback_data(rubber_shim_data)

# Save to CSV
rubber_shim_data.to_csv('rubber_shim_data.csv', index=False)
feedback_data.to_csv('customer_feedback_data.csv', index=False)

print("Datasets generated and saved as 'rubber_shim_data.csv' and 'customer_feedback_data.csv'.")
