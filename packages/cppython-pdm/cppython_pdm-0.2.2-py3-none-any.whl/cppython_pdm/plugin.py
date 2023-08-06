"""
TODO
"""

from typing import Type

from cppython.project import Project as CPPythonProject
from cppython.project import ProjectConfiguration
from cppython_core.schema import GeneratorDataType, Interface
from pdm import Core, Project
from pdm.models.candidates import Candidate
from pdm.signals import post_install


class CPPythonPlugin(Interface):
    """
    TODO
    """

    def __init__(self, core: Core) -> None:

        self.project = None
        post_install.connect(self.on_post_install)

    def read_generator_data(self, generator_data_type: Type[GeneratorDataType]) -> GeneratorDataType:
        """
        TODO
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        TODO:
        """

    def on_post_install(self, project: Project, candidates: dict[str, Candidate], dry_run: bool):
        """
        TODO
        """
        verbose = bool(project.core.ui.verbosity)

        if verbose:
            project.core.ui.echo("CPPython: Entered 'on_post_install'")

        self.project = project

        pdm_pyproject = project.pyproject

        if pdm_pyproject is None:
            if verbose:
                project.core.ui.echo("CPPython: Project data was not available")
            return

        configuration = ProjectConfiguration(verbose)
        cppython_project = CPPythonProject(configuration, self, pdm_pyproject)

        cppython_project.install()

    def print(self, string: str) -> None:

        if self.project:
            self.project.core.ui.echo(string)
