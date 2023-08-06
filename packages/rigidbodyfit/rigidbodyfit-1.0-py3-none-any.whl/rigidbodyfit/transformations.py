import json

import numpy as np

import scipy.spatial.transform


class ShiftAndOrientation:
    def __init__(self, combined_vector):
        self.shift = combined_vector[:3]
        self.orientation = combined_vector[3:]


def three_d_vector_to_rotation(vector):
    return scipy.spatial.transform.Rotation.from_quat(
        cube_to_quaternion(vector))


def cube_to_quaternion(vector):
    # https://www.ri.cmu.edu/pub_files/pub4/kuffner_james_2004_1/kuffner_james_2004_1.pdf
    # defines the mapping that is used here as:
    #
    # s = rand();
    # σ1 = √1−s;
    # σ2 = √s;
    # θ1 = 2π ∗ rand();
    # θ2 = 2π ∗ rand();
    # x = sin(θ1) ∗σ1;
    # y = cos(θ1) ∗σ1;
    # z = sin(θ2) ∗σ2;
    # w = cos(θ2) ∗σ2;
    # return (w, x, y,z)
    #
    # Note that they use a different quaternion convention,
    # so we return (x, y, z, w) instead

    def shift_into_cube(x):
        if x % 2 == 0:
            return x - np.floor(x)
        return 1 - x + np.floor(x)

    vector_in_cube = np.array(list(map(shift_into_cube, vector)))
    sigma_1 = np.sqrt(1 - vector_in_cube[0])
    sigma_2 = np.sqrt(vector_in_cube[0])
    theta_1 = 2 * np.pi * vector_in_cube[1]
    theta_2 = 2 * np.pi * vector_in_cube[2]
    return np.array([
        np.sin(theta_1) * sigma_1,
        np.cos(theta_1) * sigma_1,
        np.sin(theta_2) * sigma_2,
        np.cos(theta_2) * sigma_2
    ])


class AffineProjection:
    def __init__(self, shift, rotation):
        self.shift = shift
        self.rotation = rotation

    def toJSON(self):
        AA_to_nm = 0.1

        asDict = {
            "shift_in_nm": (AA_to_nm * self.shift).tolist(),
            "orientation_quaternion": self.rotation.as_quat().tolist(),
            "orientation_matrix": self.rotation.as_matrix().tolist()
        }
        return json.dumps(asDict,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


class Transformator:
    def __init__(self, coordinates, density_origin, density_extent):
        self.coordinates = coordinates
        self.coordinates_center = np.average(self.coordinates, axis=0)
        self.density_origin = density_origin
        self.density_extent = density_extent

    def apply(self, shift, mrp):
        # move structure to coordinate center, rotate there, then move to density origin and extra shift
        rotation = three_d_vector_to_rotation(mrp)

        return rotation.apply(
            self.coordinates - self.coordinates_center
        ) + self.density_origin + shift * self.density_extent

    def apply_to_other(self, shift, mrp, other_coordinates):

        rotation = three_d_vector_to_rotation(mrp)

        return rotation.apply(
            other_coordinates - self.coordinates_center
        ) + self.density_origin + shift * self.density_extent

    def as_affine_projection(self, shift, mrp):
        """As the transformator rotates around the center of geometry of the
           given coordinates, the corresponding affine transformation that
           rotates around the coordinate system origin needs to take this
           difference in center of rotation into account.

        Args:
            shift : shift vector
            quaternion : rotation around center of geometry

        Returns:
            AffineProjection : a transformation that corresponds to the given
                               shift and quaternion
        """

        rotation = three_d_vector_to_rotation(mrp)
        rotation_shift = -rotation.apply(self.coordinates_center)
        return AffineProjection(rotation=rotation,
                                shift=self.density_origin +
                                shift * self.density_extent + rotation_shift)
