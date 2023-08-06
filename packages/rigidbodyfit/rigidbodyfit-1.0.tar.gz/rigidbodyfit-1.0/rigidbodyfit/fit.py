""" All infrastructure to perform a rigid body fit of structure to density """
import numpy as np

import rich.progress

import scipy.interpolate
import scipy.optimize

import mrcfile

import rigidbodyfit.structure
import rigidbodyfit.logger
import rigidbodyfit.transformations


class OverlapOptimizer:
    def __init__(self, gridpoints, voxels, coordinate_transformator):
        self.coordinate_transformator = coordinate_transformator
        self.interpolator = scipy.interpolate.RegularGridInterpolator(
            gridpoints, voxels, bounds_error=False, fill_value=0.)

    def calculate_with_shift_and_rotation(self, shift_rotation):

        shift_and_orientation = rigidbodyfit.transformations.ShiftAndOrientation(shift_rotation)

        mobile_rotated_shifted = self.coordinate_transformator.apply(
            shift_and_orientation.shift, shift_and_orientation.orientation)

        return -np.average(self.interpolator(mobile_rotated_shifted))


def origin_vector(density):

    origin = np.array(density.header.origin.tolist())

    if np.all(origin == 0):
        origin[0] = density.header.nxstart * density.voxel_size['x']
        origin[1] = density.header.nystart * density.voxel_size['y']
        origin[2] = density.header.nzstart * density.voxel_size['z']

    return origin


def align_structure_to_density(
    density_filename,
    structure_filename,
    sampling_depth,
    excluded_atoms_pattern=rigidbodyfit.structure.DEFAULT_EXCLUDED_ATOMS,
    log=rigidbodyfit.logger.create_rich_logger()):

    # read density data and determine voxel size and shift vector from it
    log.info("Reading density ...")

    density = mrcfile.open(density_filename)
    voxels = density.data.T

    density_origin_vector = origin_vector(density)
    density_grid = tuple([
        density.voxel_size.tolist()[i] * np.arange(voxels.shape[i]) +
        density_origin_vector[i] for i in range(3)
    ])
    density_extend = np.array(density.voxel_size.tolist()) * voxels.shape

    log.info("done")

    log.info("Reading structure file ...")
    structure = rigidbodyfit.structure.Structure(structure_filename,
                                                 excluded_atoms_pattern)
    log.info(
        f"selected {structure.coordinates.size // 3} atoms for fitting, ignoring atom names containing {excluded_atoms_pattern}"
    )

    log.info("Optimising shift and rotatation ...")

    mobile_coordinates = rigidbodyfit.transformations.Transformator(
        structure.coordinates,
        density_origin=density_origin_vector,
        density_extent=density_extend)

    overlap = OverlapOptimizer(voxels=voxels,
                               coordinate_transformator=mobile_coordinates,
                               gridpoints=density_grid)

    number_iterations = pow(2, sampling_depth)
    if sampling_depth < 0:
        log.info("Negative sampling-depth value reset to unity.")
        number_iterations = int(1)

    with rich.progress.Progress() as progress:

        optimizer_task = progress.add_task(
            f"optimizing using {number_iterations} iterations",
            total=number_iterations)

        def print_fun(x, f, accepted):
            progress.advance(optimizer_task, advance=1)

        result = scipy.optimize.basinhopping(
            overlap.calculate_with_shift_and_rotation, [0.5] * 6,
            stepsize=0.01,
            niter=number_iterations,
            minimizer_kwargs={'method': 'L-BFGS-B'},
            callback=print_fun)

    log.info(
        f"Best average voxel value at structure coordinates : {-result.fun:.4f} ."
    )

    bestFit = rigidbodyfit.transformations.ShiftAndOrientation(result.x)

    all_coordinates = structure.all_coordinates()

    structure.set_coordinates(
        mobile_coordinates.apply_to_other(bestFit.shift, bestFit.orientation,
                                          all_coordinates))
    best_fit_as_affine_projection = mobile_coordinates.as_affine_projection(
        bestFit.shift, bestFit.orientation)

    return structure, best_fit_as_affine_projection
