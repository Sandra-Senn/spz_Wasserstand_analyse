import nbformat
from nbconvert import PythonExporter

# Notebook laden
with open('notebooks/4_vorhersage.ipynb', 'r', encoding='utf-8') as f:
    notebook = nbformat.read(f, as_version=4)

# Zu Python konvertieren
exporter = PythonExporter()
python_code, _ = exporter.from_notebook_node(notebook)

# Speichern
with open('notebooks/4_vorhersage.py', 'w', encoding='utf-8') as f:
    f.write(python_code)