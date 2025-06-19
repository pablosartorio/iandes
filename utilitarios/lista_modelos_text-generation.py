from huggingface_hub import list_models

# Filtrar modelos de summarization en español
summarization_models = list_models(
    filter="summarization",
    language="es",  # Filtra por español
    sort="downloads",  # Ordena por popularidad
    direction=-1,  # Descendente (más descargados primero)
    limit=10  # Muestra los 10 más relevantes
)

for model in summarization_models:
    print(model.id)
