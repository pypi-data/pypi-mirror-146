from typing import Optional, List, Any

from pydantic import BaseModel


class UpdateOptions(BaseModel):
    """Class that contains the options for updating a model
    """  # noqa
    deployment_id: str
    """str: the id of the deployment"""  # noqa
    name: Optional[str]
    """str, optional: the display name of the deployment"""  # noqa
    description: Optional[str]
    """str, optional: the description of the deployment"""  # noqa
    model_serverless: Optional[bool]
    """bool, optional: whether to deploy the model in a serverless fashion"""  # noqa
    explainer_serverless: Optional[bool]
    """bool, optional: whether to deploy the model in a serverless fashion"""  # noqa
    example_input: Optional[List[Any]]
    """List, optional: list of example input parameters for the model"""  # noqa
    example_output: Optional[List[Any]]
    """List, optional: list of example output for the model"""  # noqa
    feature_labels: Optional[List[str]]
    """List, optional: list of feature labels for the explanations"""  # noqa
    pytorch_model_file_path: Optional[str]
    """str, optional: absolute or relative path to the .py file containing the pytorch model class definition"""  # noqa
    pytorch_torchserve_handler_name: Optional[str]
    """str, optional: TorchServe handler name. One of 
        ['image_classifier', 'image_classifier', 'object_detector', 'text_classifier']. 
        See the (TorchServe documentation)[https://github.com/pytorch/serve/blob/master/docs/default_handlers.md#torchserve-default-inference-handlers]
        for more info."""  # noqa
