# credit-risk-segmentation
Repository for Bancolombia admission test.

## Project Structure

- `credit-risk-segmentation/`
  - `data/`
    - `raw/` - Where all raw data is stored
    - `processed/` - Processed data, in case we need to modify the original structure for better analysis
  - `notebooks/`
    - `EDA.ipynb` - The fun part: where everything is a mess only I would understand
    - `preprocessing.ipynb` - A slightly cleaner mess compared to the step before
    - `model_training.ipynb` - When everything seems like Disneyworld for data modeling... or maybe not
  - `scripts/`
    - `preprocessing.py` - Scripts to run once we fully understand the entire problem context
    - `train_model.py` - Script for training the model
    - `evaluate_model.py` - Script for evaluating the trained model
  - `models/`
    - `trained_model.pkl` - Serialized model information (stored as binary data)
  - `docs/`
    - `report.md` - Well... we're doing all this for a reason, right? Here’s the explanation of our results
    - `system_design.md` - Theoretical description of the system that will make the model results available.
      - (This section aims to describe a high-level design for exposing the model's results through APIs or other platforms, like a website or mobile app.)
  - `results/`
    - `predictions.csv` - Model's predictions: the main output of our efforts
  - `requirements.txt` - It's better to work with a virtual environment. We don't want to end up running `sudo rm -rf /`
  - `README.md` - General project information, including the file you're reading right now
  - `.gitignore` - Files and folders we don't want to upload to our beloved friend: GitHub
