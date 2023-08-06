import pandas as pd


def predict(instances: pd.DataFrame, model):
    print("-" * 50)
    print("here in user pipeline")
    print("-" * 50)

    preds = model.predict(instances)

    result = pd.DataFrame(data={"Signal": preds}, index=instances.index)
    result.index.name = instances.index.name
    print(result)
    return result
