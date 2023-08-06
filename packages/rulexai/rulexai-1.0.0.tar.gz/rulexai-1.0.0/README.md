# RuleXAI

RuleXAI is a rule-based aproach to explain the output of any machine learning model. It is suitable for classification, regression and survival tasks. 

## Instalation

RuleXAI can be installed from PyPI

```bash
pip install rulexai
```

Or you can clone the repository and run:
```bash
pip install .
```

## Model agnostic example
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd

from rulexai.explainer import Explainer


# load iris dataset
data = load_iris()
df = pd.DataFrame(data['data'], columns=data['feature_names'])
df['class'] = data['target']


# train a SVM classifier
X_train,X_test,y_train,y_test = train_test_split(df.drop(columns=["class"]), df["class"], test_size=0.2, random_state=0)
svm = SVC(kernel='rbf', probability=True)
svm.fit(X_train, y_train)


# use Explainer to explain model output
explainer =  Explainer(X = X_train,model_predictions = y_train.astype(str), type = "classification")
explainer.explain()
```

## Sample notebooks

* **[Classification]()**  - in this notebook, the data from https://www.kaggle.com/c/titanic is analysed to show the advantages and possibilities of using the RuleXAI library for in-depth analysis of the dataset for classification task. The use of RuleXAI to explain rule-based and tree-based models was also compared. 
   
* **[Regression]()** - notebook showing the use of RuleXAI to explain rule-based regression model
   
* **[Survival]()** - notebook showing the use of RuleXAI to explain rule-based survival model
    
* **[Black-box model]()** explainability - the purpose of this notebook is to demonstrate the possibility of using RuleXAI to explain any black box models.
     
* **[Transformation]()** - notebook showing the use of RuleXAI to transform a dataset. Often datasets contain missing values and nominal values. Most available algorithms do not support either missing values or nominal values. Many algorithms require the data to be rescaled beforehand. The RuleXAI library is able to convert a dataset with nominal and missing values into a binary dataset containing as attributes the conditions describing the dataset and as values “1” when the condition is satisfied for the example and “0” when the condition is not satisfied.
   

## Documentation
Full documentation is available [here]()

