# Herramienta genérica para ingesta de data, procesamiento con llms y llenado de plantillas.

## Justificación

- Oportundad de atender una necesidad: pérdida de conocimiento crítico por jubilación o retiro de personal altamente calificado (expertos).
- Falta de mano de obra para realizar recopilación de información, desgrabado de entrevistas y diseño de planes de acción para captura y transferencia de conocimiento crítico.
- Potencialidad del mismo pipeline (Ingest - Process - Deliver)  para disponibilizar información relacionada a otra información disponible actualmente pero no estructurada o integrada a procesos (sitematizada). 

## Objetivo

La hipótesis que manejamos es que el proceso de identificación, captura y transferencia de conocimiento crítico asociado a personas se puede agilizar utilizando inteligencia artificial. Sustentan ésto que:

- Existe amplia variedad de registros (texto, audio, video) en distintos repositorios no catalogados, o compartimentada por proyectos y servicios.

- Hemos verificado que la mayor parte de los grupos tienen algún mecanismo de transferencia en curso pero que no cuenta con un marco organizacional transversal y por lo tanto:
	- si el registro y transferncia resulta exitoso es en gran parte gracias al esfuerzo individual
	- la empresa no se beneficia, no aprende, de éstos esfuerzos individuales porque no tiene registro explícito de los mismos
	- en caso de fracaso o desvío no se cuenta con indicadores o soporte.

## Metodología

Proponemos un flujo de trabajo que consiste básicamente en uno o varios ciclos de **ingesta, procesamiento y entrega** (ingest, process, deliver). El resultado final, en éste caso particular, es un *plan de acción para captura y transferencia* del conocimiento crítico de una persona en particular.

### Flujo de trabajo:

1. Recopilación de información relacionada a la persona: documentación, grabaciones de audio y video, etc.

2. Creación de una una entrevista personalizada a partir de una guía genérica para realizar entrevistas creada por gestión del concimiento (producto) y de la información recopilada y aumentada en los pasos anteriores. (Requiere auditoría de CTO). 

3. Realización de entrevista y grabado de audio. (Ver posibilidad de agregar marcas de tiempo o destacados durante la grabación).

4. Transcripción de la entrevista a texto plano (desgrabación).

5. Procesamiento de información: resumen extractivo y abstractivo, índice temático, identificación de entidades y relaciones, complejidad léxica y tecnicismos, análisis semántico emocional, análisis de privacidad, etc.

6. Llenado de planilla genérica para identificación de conocimientos críticos de la persona. Se parte de una planilla genérica estructurada (creación GeCo) y se utiliza la información recopilada en la entrevista y la anterior. (Requiere auditoría experto y CTO).

7. Generación de un plan de acción particular para el experto en cuestión a partir de toda la información previa (DB + planilla) y de un paquete de herramientas y metodologías estándar provistas por GeCo. (Requiere auditoría CTO, experto y partes involucradas).

## Roles y funciones

* GeCo: proveedor de metodología y herramientas, receptor de feedback de metodología.
* IA: proveedor de herramienta IA
* CTO: responsable de la ejecución, receptor y dueño de los entregables, propietario de los datos.
* Partner GeCo: ejecutor del flujo, gestor de calendario y prespuesto.

## A continuación

* Explicitar entregables: resumen entrevista, planilla conocimientos 
* Definir KPIs y matriz RACI.

## Diagrama
![Imágen del diagrama](documentos/diagramas/Diagrama.svg)
