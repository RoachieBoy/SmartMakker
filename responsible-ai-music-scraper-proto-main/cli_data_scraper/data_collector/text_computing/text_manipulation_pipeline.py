from dataclasses import dataclass
from typing import Callable, List, Union


@dataclass
class TextManipulationPipeline:
    """
    A pipeline of text manipulation passes to clean up text.
    """
    passes: {
        str: (
            Union[
                Callable[[str], str],
                Callable[[str, any], str],
                Callable[[str, any, any], str],
                Callable[[str, any, any, any], str]
            ],
            []
        )
    }

    def add_pass(
            self,
            pass_id: str,
            function: Union[
                Callable[[str], str],
                Callable[[str, any], str],
                Callable[[str, any, any], str],
                Callable[[str, any, any, any], str]
            ],
            arguments: [] = None
    ) -> None:
        """
        Add a pass to the pipeline.

        :param pass_id: The id of the pass.
        :param function: The function to run.
        :param arguments: The arguments to pass to the function.
        """

        self.passes[pass_id] = (function, arguments)

    def add_passes(
            self,
            passes_input:
            {
                str:
                    (
                            Union[
                                Callable[[str], str],
                                Callable[[str, any], str],
                                Callable[[str, any, any], str],
                                Callable[[str, any, any, any], str]
                            ],
                            []
                    )
            }
    ) -> None:
        """
        Add a set of passes to the pipeline.
        
        :param passes_input: a dictionary of pass id's and a tuple of the function and extra call arguments.
        """
        self.passes.update(passes_input)

    def remove_pass(self, pass_id: str) -> None:
        """
        Remove a pass from the pipeline.

        :param pass_id: The id of the pass to remove.
        """

        self.passes.pop(pass_id)

    def run_pipeline(self, to_modify: str | List[str]) -> List[str]:
        """
        Run the pipeline on the given input.

        :param to_modify: The input to the pipeline.
        :return: The output of the pipeline as a list of strings.
        """

        if isinstance(to_modify, str):
            to_modify = [to_modify]

        for pass_function in self.passes.values():
            if pass_function[1] is not None:

                for i, text in enumerate(to_modify):
                    to_modify[i] = pass_function[0](text, *pass_function[1])
            else:

                for i, text in enumerate(to_modify):
                    to_modify[i] = pass_function[0](text)

        return to_modify
