
def dummy_node(instances, model):
    print("-" * 50)
    print("here in user pipeline")
    print("-" * 50)

    result = model.predict(instances)
    print(result)
    return result

