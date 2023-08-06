import pandas as pd


def predict(instances: pd.DataFrame, model):
    print("-" * 50)
    print("here in user pipeline")
    print("-" * 50)

    result = model.predict(instances)
    print(result)
    return result
