""" Run the command line interface """
import logging
import shutil

import importlib.metadata

import mrcfile

import scipy.signal

import numpy as np

import rich.console
import rich.logging

import mrcsmooth.arguments


def create_rich_logger():
    FORMAT = "%(message)s"
    logging.basicConfig(level="INFO",
                        format=FORMAT,
                        datefmt="[%X]",
                        handlers=[rich.logging.RichHandler()])
    return logging.getLogger("rich")


def run():
    """ run the command line interface """

    # set up the console for printing and logging
    console = rich.console.Console()
    log = create_rich_logger()

    # derive the program version via git
    try:
        version = importlib.metadata.version("mrcsmooth")
    except importlib.metadata.PackageNotFoundError:
        version = "Unknown"

    command_line_arguments = (
        mrcsmooth.arguments.get_command_line_arguments(version))

    log.info("Reading density ...")

    # because copying mrcfile objects is hard, start out by copying the file
    shutil.copy2(command_line_arguments.density,
                 command_line_arguments.output_density)

    output_density = mrcfile.open(command_line_arguments.output_density,
                                  'r+',
                                  permissive=True)

    output_density.header.ispg = mrcfile.constants.VOLUME_SPACEGROUP

    resampled_data = output_density.data
    for resampling_step in range(command_line_arguments.passes):
        if min(resampled_data.shape) < 8:
            log.info(f"Stopping resampling at pass {resampling_step} despite "
                     f"the requested {command_line_arguments.passes} to "
                     f"have a meaningful density left.")
            break
        for axis in range(3):
            resampled_data = scipy.signal.resample(
                resampled_data, resampled_data.shape[axis] // 2, axis=axis)

    output_density.set_data(resampled_data)

    output_density.close()

    log.info("done")
