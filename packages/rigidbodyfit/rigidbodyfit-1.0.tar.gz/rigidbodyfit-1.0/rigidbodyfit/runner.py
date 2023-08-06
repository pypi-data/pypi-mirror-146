""" Run the command line interface """
import importlib.metadata

import rich.console

import rigidbodyfit.arguments
import rigidbodyfit.fit
import rigidbodyfit.logger


def run():
    """ run the command line interface """

    # set up the console for printing
    console = rich.console.Console()

    # derive the program version via git
    try:
        version = importlib.metadata.version("rigidbodyfit")
    except importlib.metadata.PackageNotFoundError:
        version = "Unknown"

    command_line_arguments = (
        rigidbodyfit.arguments.get_command_line_arguments(version))

    log = rigidbodyfit.logger.create_rich_logger()

    structure, bestFitAsAffine = rigidbodyfit.fit.align_structure_to_density(
        command_line_arguments.density, command_line_arguments.structure,
        command_line_arguments.sampling_depth, command_line_arguments.exclude,
        log)
    # use input structure as template for output
    structure.full_structure.to_pdb(command_line_arguments.output_structure)

    command_line_arguments.output_transform.write(bestFitAsAffine.toJSON())
