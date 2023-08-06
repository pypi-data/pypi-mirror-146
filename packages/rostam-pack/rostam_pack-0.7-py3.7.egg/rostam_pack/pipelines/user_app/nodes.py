import pandas as pd


def predict(instances: pd.DataFrame, model):
    print("-" * 50)
    print("here in user pipeline")
    print("-" * 50)

    preds = model.predict(instances)

    result = pd.DataFrame(data={"Signal": preds}, index=instances.index)
    result.index.name = instances.index.name

    result[result["Signal"] > 0.5] = 1
    result[result["Signal"] <= 0.5] = -1

    print(result)
    return result
