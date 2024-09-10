import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.ticker as ticker

# Define project tasks and dates
tasks = {
    'Foundations': [('Onboarding & Literature Review', '2025-02-01', '2025-04-30'),
                    ('Proposal Finalization', '2025-05-01', '2025-05-31')],
    'Initial Research': [('Prototypes Development', '2025-06-01', '2025-08-31'),
                         ('Major Review Prep', '2025-09-01', '2025-09-30')],
    'Advanced Research': [('Core Components', '2025-10-01', '2025-12-31'),
                          ('Testing & Validation', '2026-01-01', '2026-02-28')],
    'Refinement': [('Mid-Term Review', '2026-03-01', '2026-03-31'),
                   ('Continued Development', '2026-04-01', '2026-06-30')],
    'Finalization': [('Research Completion', '2026-07-01', '2026-08-31'),
                     ('Documentation', '2026-09-01', '2026-10-31')],
    'Defense & Completion': [('Thesis Preparation', '2026-11-01', '2026-12-31'),
                             ('Thesis Submission', '2027-01-01', '2027-01-31')]
}

# Convert dates and tasks to a DataFrame
data = []
for category, items in tasks.items():
    for task, start, end in items:
        data.append([category, task, pd.to_datetime(start), pd.to_datetime(end)])

df = pd.DataFrame(data, columns=['Category', 'Task', 'Start', 'End'])
df['Duration'] = df['End'] - df['Start']

# Plot
fig, ax = plt.subplots(figsize=(12, 8))
colors = plt.cm.tab20.colors

# Plot bars
for i, (category, group) in enumerate(df.groupby('Category')):
    for _, row in group.iterrows():
        ax.barh(row['Task'], row['Duration'].days, left=row['Start'], color=colors[i % len(colors)], edgecolor='black',
                label=category if group.index[0] == _ else "")

# Formatting
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Tasks', fontsize=12)
ax.set_title('PhD Project Timeline', fontsize=14, weight='bold')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

# Format x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.7)

# Adjust layout
plt.tight_layout()
plt.show()
