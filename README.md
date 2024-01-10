

# Analysis of the impact of incorrectly labeled training sets in the medical domain. 

## Authors 

Hugo Alcalde (s222700) : https://github.com/hugoalcalde

Berta Plandolit (s222552) : https://github.com/bertaplandolit 

Christof Haye (s222577) : https://github.com/Christooof

## Project Descriptions

In this project, we will develop an MLOps pipeline for an image classification problem focused on brain hemorrhage prediction on CTs. The primary objective is to assess the impact of incorrect labels in the training set. To achieve this, we will conduct a series of experiments, randomly changing a percentage of the training labels, and evaluate the resulting accuracy in the test and validation sets. This analysis aims to simulate real-world scenarios, particularly prevalent in the medical domain, where data sets are rarely 100% accurate. The goal is to determine whether the model can still generalize results and make accurate predictions despite imperfect training data.

The original dataset, sourced from Kaggle (https://www.kaggle.com/datasets/felipekitamura/head-ct-hemorrhage), comprises head CTs. The classification model identifies the presence of an hemorrhage in the provided pictures.

For the implementation, we plan to utilize the following frameworks, models and tools:

- The selected model will be a 2D DenseNet, which is a Convolutional Neural Network (CNN) which uses residual connections in each of the layers and that has shown excellent performance in classification tasks. 

- For the implementation of the model, we will use a Pytorch-based third-party package (https://monai.io/), which is freely available collaborative frameworks built for accelerating research and clinical collaboration in Medical Imaging.

- Due to the goal of the project, which is not obtaining good modeling results but to analyze the impact of errors in datasets, reproducibility and scalability are two key points to make sure the pipeline we propose is applicable to other datasets and to make sure that the changes in the accuracy of the network are due to the experimental changes we are making in the training data. For that, we will use cookiecutter for code structure organization, which will ensure easy comparisons between the trained models, and Docker images, that will provide us of a common and controlled environment for training the different models. 

In other words, in this project, Machine Learning Operations (MLOps) tools are used for creating an expandable workflow for the analysis of the impact of changes in the training dataset for Deep Learning models applied to classification tasks. 



## Project structure

The directory structure of the project looks like this:

```txt

├── Makefile             <- Makefile with convenience commands like `make data` or `make train`
├── README.md            <- The top-level README for developers using this project.
├── data
│   ├── processed        <- The final, canonical data sets for modeling.
│   └── raw              <- The original, immutable data dump.
│
├── docs                 <- Documentation folder
│   │
│   ├── index.md         <- Homepage for your documentation
│   │
│   ├── mkdocs.yml       <- Configuration file for mkdocs
│   │
│   └── source/          <- Source directory for documentation files
│
├── models               <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks            <- Jupyter notebooks.
│
├── pyproject.toml       <- Project configuration file
│
├── reports              <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures          <- Generated graphics and figures to be used in reporting
│
├── requirements.txt     <- The requirements file for reproducing the analysis environment
|
├── requirements_dev.txt <- The requirements file for reproducing the analysis environment
│
├── tests                <- Test files
│
├── imperfect_trainings  <- Source code for use in this project.
│   │
│   ├── __init__.py      <- Makes folder a Python module
│   │
│   ├── data             <- Scripts to download or generate data
│   │   ├── __init__.py
│   │   └── make_dataset.py
│   │
│   ├── models           <- model implementations, training script and prediction script
│   │   ├── __init__.py
│   │   ├── model.py
│   │
│   ├── visualization    <- Scripts to create exploratory and results oriented visualizations
│   │   ├── __init__.py
│   │   └── visualize.py
│   ├── train_model.py   <- script for training the model
│   └── predict_model.py <- script for predicting from a model
│
└── LICENSE              <- Open-source license if one is chosen
```

Created using [mlops_template](https://github.com/SkafteNicki/mlops_template),
a [cookiecutter template](https://github.com/cookiecutter/cookiecutter) for getting
started with Machine Learning Operations (MLOps).
