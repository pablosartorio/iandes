from google import genai

# Inicializas tu cliente (aquí con la API key ya configurada en la variable de entorno)
client = genai.Client()

# Listar todos los modelos base disponibles
print("Modelos disponibles:")
for model in client.models.list():
    # Cada 'model' es un objeto con atributos como 'name', 'display_name', etc.
    print(f"  • {model.name}")

