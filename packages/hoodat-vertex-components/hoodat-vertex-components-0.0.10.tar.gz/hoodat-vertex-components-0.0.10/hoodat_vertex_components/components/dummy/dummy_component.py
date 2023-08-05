from kfp import dsl
from kfp.dsl.types import GCSPath
from kfp.dsl.types import String


@dsl.component
def dummy_op(input1: String(), input2: GCSPath()) -> {"output1": GCSPath()}:
    """
    Dummy component for illustrative purposes
    """
    output1 = "/tmp/python_dummy_op/output1_path"
    return dsl.ContainerOp(
        name="Dummy op",
        image="dummy-image",
        command=[
            "python",
            "runner.py",
            "--input1",
            input1,
            "--input2",
            input2,
            "--output1",
            output1,
        ],
        file_outputs={"output1": output1},
    )
