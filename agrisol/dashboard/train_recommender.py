# train_recommender.py
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Exemple de données (à remplacer par tes vraies données)
# X = [humidite, temperature, ph, lumiere, co2, niveau_eau]
X = [
    [10, 35, 7.5, 200, 400, 10],
    [80, 20, 6.0, 800, 900, 80],
    [50, 25, 8.5, 500, 600, 50],
    [30, 30, 5.0, 300, 300, 30],
    [60, 28, 7.0, 700, 800, 60],
    [40, 22, 6.5, 400, 500, 40],
]
# y = 1: irriguer, 2: ventiler, 3: corriger pH, 4: ajuster lumière, 5: ajuster co2, 0: rien
y = [1, 2, 3, 1, 4, 5]

# Pipeline avec normalisation + RandomForest
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier())
])

# Recherche d’hyperparamètres
param_grid = {
    'clf': [RandomForestClassifier(), SVC(probability=True)],
    'clf__n_estimators': [50, 100] if isinstance(pipe.named_steps['clf'], RandomForestClassifier) else [None],
    'clf__C': [1, 10] if isinstance(pipe.named_steps['clf'], SVC) else [None],
}

# Nettoyage du param_grid pour GridSearchCV
param_grid_clean = []
for clf in [RandomForestClassifier(), SVC(probability=True)]:
    if isinstance(clf, RandomForestClassifier):
        param_grid_clean.append({'clf': [clf], 'clf__n_estimators': [50, 100]})
    else:
        param_grid_clean.append({'clf': [clf], 'clf__C': [1, 10]})

grid = GridSearchCV(pipe, param_grid_clean, cv=3)
grid.fit(X, y)

print("Best params:", grid.best_params_)
print("Best score:", grid.best_score_)

# Sauvegarde du modèle
joblib.dump(grid.best_estimator_, "recommender_model.joblib")