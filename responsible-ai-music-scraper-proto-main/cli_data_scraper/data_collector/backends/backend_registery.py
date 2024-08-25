from abc import ABC, abstractmethod


class ScraperBackend(ABC):
    """
    Abstract class for scraper backends.
    """

    def __init__(self) -> None:
        self._name: str = "NO NAME"

    @property
    def backend_name(self) -> str:
        """
        :return: The name of the initialized backend.
        """
        return self._name

    @abstractmethod
    def initialise(self, initialisation_arguments: (str, str)) -> None:
        """
        Initialize the backend with the given arguments.

        :param initialisation_arguments: The arguments to initialize the backend with.
        :return: None
        """

        self._name = initialisation_arguments[0]

    @abstractmethod
    def run(self) -> [str]:
        """
        Run the backend.

        :return: String list of the results.
        """

        pass


available_backends: {str: ScraperBackend} = {}


def register_backend(backend_id):
    """
    Register a backend in the backend registry.

    :param backend_id: The id of the backend to register.
    :return: The decorator.
    """
    def decorator(cls):
        available_backends[backend_id] = cls()

        return cls

    return decorator


def get_backend(backend_id: str) -> ScraperBackend:
    """
    Get a backend from the backend registry.

    :param backend_id: The id of the backend to get.
    :return: The backend.
    """

    if available_backends.keys().__contains__(backend_id):
        return available_backends[backend_id]
    else:
        print("Backend with id " + backend_id + " not found in registry.")
