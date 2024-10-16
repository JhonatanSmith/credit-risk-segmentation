# credit-risk-segmentation
Repository for Bancolombia admission test.

`Nota` Debido a que los tiempos para realizar la prueba no fueron suficientes, los analisis han quedado incompletos. Sin embargo en cada apartado se ha dado una idea general de como ha sido el workflow, que se ha hecho, las discusiones planteadas. 

## Project Structure

- `credit-risk-segmentation/`
  - `data/`
    - `raw/` - Where all raw data is stored
    - `processed/` - Processed data, in case we need to modify the original structure for better analysis
      `model/` - Data ready to modelling
      - `poutput/` - Model's prediciton
  - `notebooks/`
    - `preprocessing.ipynb` - The fun part: where everything is a mess only I would understand
    - `feature selection.ipynb` - A slightly cleaner mess compared to the step before
    - `model_training.ipynb` - When everything seems like Disneyworld for data modeling... or maybe not
  - `scripts/`
    - `preprocessing.py` - Scripts to run once we fully understand the entire problem context and automatizate the tasks
    - `train_model.py` - Script for training the model
    - `evaluate_model.py` - Script for evaluating the trained model
  - `models/`
    - `trained_model.pkl` - Serialized model information (stored as binary data)
    - - `Arquitectura propuesta.md` - Markdown made with ChatGPT to propose an API REST Architecture
  - `docs/`
    - `report.md` - Well... we're doing all this for a reason, right? Here’s the explanation of our results. Or it should be if i had the time...
  - `requirements.txt` - It's better to work with a virtual environment. We don't want to end up running `sudo rm -rf /`
  - `README.md` - General project information, including the file you're reading right now and a brief explanation of analysis done
  - `.gitignore` - Files and folders we don't want to upload to our beloved friend: GitHub


# Comentarios finales

`Insights`

1) Los datos no cuentan con informacion demografica relacionada al cliente. Variables como la edad, sexo o ingresos podrian ser significativas a la hora de responder la pregunta de interes.

2) La calidad de los datos no ha sido l aadecuada. De casi 30 mil datos, las tablas con la que se ha trabajado se reduce a 2 mil (train). Lo mismo para las de test

3) Por temas de tiempo, el unico algoritmo que pudo ser ejecutado fue XGboost para clasificacion. Se hizo un analisis SHAPE para identificar las variables que son mas immportantes. Queda pendiente la asignacion de categorias. Diferentes algoritmos querian ser probados.

4) Se ha asumido un workflow de desarollo de analitica. Por eso se ha asignado esta estructura a los folders y archivos. **La logica y analisis del problema** fue ejecutada en el apartado de notebooks, ordenados como 1,2,3 y un nombre diciente del mismo. La carpeta **scripts** posee el pipeline de ejecucion del analisis. Ideialmente, todo se deberia de unificar en un scrip en la carpeta raiz que se llamase 'run_incumplimiento.py' que ejecutaria todos los ecripts y guardaria los resultados como s edio en la estructura del proyecto.

5) En un escenario ideal, la prueba de hubiese finalizado en sui totalidad con recomendaciones y un modelo serializado para la ejecucion. Una API que consuma los resultados del modelo y lo ejecute en tiempo real podria ser una buena practica. Paara esto, Flask o FastAPI crean herramientas web que permiten el despliegue de estos servicios. Para mayor informacion, ver mi peril personal en el proyecto de Currency Converter y el despliegue de API's.

6) Chat GPT solo ha sido usado para **consultas asociadas a estructura de codigo** es decir, formatear siguiendo PEP8 (reglas de programacion estandarizada en pyhton) **y** la respuesta fuinal del script de uso de una API para desplegar el modelo

*FYI:*
(https://github.com/JhonatanSmith/Currency-Converter)
