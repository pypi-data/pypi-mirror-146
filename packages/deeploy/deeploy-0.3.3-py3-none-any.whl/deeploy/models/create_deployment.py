from typing import Optional, Any, List

from pydantic import BaseModel


class CreateDeployment(BaseModel):
    """Class that contains the options for creating a deployment
    """  # noqa
    name: str
    description: Optional[str]
    repository_id: Optional[str]
    branch_name: Optional[str]
    commit: Optional[str]
    commit_message: Optional[str]
    contract_path: Optional[str]
    has_example_input: Optional[bool]
    example_input: Optional[List[Any]]
    example_output: Optional[Any]
    input_tensor_size: Optional[str]
    output_tensor_size: Optional[str]
    model_type: Optional[Any]
    model_serverless: Optional[bool] = False
    explainer_type: Optional[Any]
    explainer_serverless: Optional[bool] = False

    def to_request_body(self):
        return {
            'name': self.name,
            'description': self.description,
            'repositoryId': self.repository_id,
            'exampleInput': self.example_input,
            'exampleOutput': self.example_output,
            'modelType': self.model_type,
            'modelServerless': self.model_serverless,
            'explainerType': self.explainer_type,
            'explainerServerless': self.explainer_serverless,
            'branchName': self.branch_name,
            'commit': self.commit,
            'contractPath': self.contract_path,
        }
