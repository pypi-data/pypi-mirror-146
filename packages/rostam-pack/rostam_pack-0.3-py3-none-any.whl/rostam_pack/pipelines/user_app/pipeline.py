from kedro.pipeline import Pipeline, node
from .nodes import *

def create_pipeline():
    return Pipeline([
        node(
            func=dummy_node,
            inputs=dict(instances="instances", model="pipeline_inference_model"),
            outputs="predications",
            tags=["user_app"]
        )
    ])