import concurrent

from data_collector.data_io.run_configuration import RunConfiguration
from data_collector.text_computing.text_container import TextContainer
from data_collector.backends.backend_registery import get_backend, ScraperBackend
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

initialised_scrapers: {str: ScraperBackend} = {}


def run_pipeline() -> TextContainer:
    """
    Run the pipeline and return the final text container

    :return: The final text container containing the text from all the scrapers
    """
    container = TextContainer(creation_data=datetime.now(), text_table={})

    with ThreadPoolExecutor() as executor:
        future_to_backend = {
            executor.submit(backend.run): backend for backend in initialised_scrapers.values()
        }

        for future in concurrent.futures.as_completed(future_to_backend):
            backend = future_to_backend[future]

            try:
                result = future.result()
            except Exception as exc:
                print(f"{backend.backend_name} generated an exception: {exc}")
            else:
                container.text_table[backend.backend_name] = result

    return container


def build_pipeline(run_configuration: RunConfiguration) -> None:
    """
    Build the pipeline based on the run configuration
    :param run_configuration: The run configuration holding the information about the scrapers to run
    :return: None
    """

    for scraper_backend_type in run_configuration.backend_arguments.keys():
        # Get the backend from the registry and create new instance
        backend = type(get_backend(scraper_backend_type))()

        # Initialize the backend with the given arguments
        backend.initialise(run_configuration.backend_arguments[scraper_backend_type])

        # Add the backend to the initialized scrapers
        initialised_scrapers[backend.backend_name] = backend
