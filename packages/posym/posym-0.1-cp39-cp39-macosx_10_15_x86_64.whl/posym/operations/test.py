import numpy as np
from scipy.spatial.transform import Rotation as R
from symgroupy import Symgroupy
import matplotlib.pyplot as plt
from itertools import permutations


def get_perpendicular(vector):
    for i, v in enumerate(vector):
        if np.abs(v) < 1e-5:
            v1 = np.zeros_like(vector)
            v1[i] = 1
            v2 = np.cross(vector, v1).tolist()

            return v1, v2

    for i, v in enumerate(vector):
        if np.abs(v) >= 1e-5:

            vr = np.array(vector).copy()
            vr[i] = -vr[i]

            v1 = np.cross(vector, vr).tolist()
            v2 = np.cross(vector, v1).tolist()

            return v1, v2


def rotation(angle, rotation_axis):

    rotation_vector = angle * np.array(rotation_axis) / np.linalg.norm(rotation_axis)
    rotation = R.from_rotvec(rotation_vector)

    return rotation.as_matrix()


def prepare_vector(positions, vector):

    #return np.dot(positions.T, positions) - np.dot(vector.T, positions)
    return np.array(vector) + np.array(positions)


def reflection(reflection_axis):

    reflection_axis = np.array(reflection_axis) / np.linalg.norm(reflection_axis)

    axis1, axis2 = get_perpendicular(reflection_axis)

    return np.outer(axis1, axis1) + np.outer(axis2, axis2) - np.outer(reflection_axis, reflection_axis)


def inversion():
    return -np.identity(3)


water = [[ 0.00000000e+00,  0.00000000e+00,  2.40297090e-01],
         [-1.43261539e+00, -1.75444785e-16, -9.61188362e-01],
         [ 1.43261539e+00,  1.75444785e-16, -9.61188362e-01],
         #[1, 0, 0]
         ]
water = np.array(water)*0.5
symbols = ['O', 'H', 'H']

rotation_axis = [0, 0, 1]


from pyqchem import get_output_from_qchem, Structure, QchemInput
from pyqchem.parsers.parser_frequencies import basic_frequencies
import matplotlib.pyplot as plt
from pyqchem.errors import OutputError



molecule = Structure(coordinates=water,
                     symbols=symbols,
                     charge=0,
                     multiplicity=1)

qc_input = QchemInput(molecule,
                      jobtype='freq',
                      exchange='hf',
                      basis='sto-3g',
                      )

parsed_data, ee = get_output_from_qchem(qc_input, parser=basic_frequencies, read_fchk=True)

opt_molecule = ee['structure']

print(' structure')
water = np.array(opt_molecule.get_coordinates())
print('Final energy:', parsed_data['scf_energy'])

mode = np.array(parsed_data['modes'][2]['displacement'])
complete_modes = [np.array(m['displacement']) for m in parsed_data['modes']]

with open('test_rot.xyz', 'w') as f:
    for angle in np.arange(0, 2*np.pi, 0.1):

        rotated_water = np.dot(rotation(angle, rotation_axis), water.T).T

        f.write('{}\n\n'.format(len(rotated_water) + 1))
        for r, l in zip(rotated_water, symbols):
            f.write(l + ' {:5.2f} {:5.2f} {:5.2f}\n'.format(*r))

        v1 = water[1] - water[0]
        r1 = water[2]

        #print(prepare_vector(r1, v1))

        rotated_vector = np.dot(rotation(angle, rotation_axis), prepare_vector(r1, v1))
        rotated_position = rotated_vector + rotated_water[2]

        f.write('C' + ' {:5.2f} {:5.2f} {:5.2f}\n'.format(*rotated_position))
        # print(np.dot(rotated_vector, v1))

with open('test_ref.xyz', 'w') as f:

    print(reflection(rotation_axis))

    reflected_water = np.dot(reflection(rotation_axis), water.T).T

    for coor in [water, reflected_water]:
        f.write('{}\n\n'.format(len(coor)))
        for r, l  in zip(coor, symbols):
            f.write(l + ' {:5.2f} {:5.2f} {:5.2f}\n'.format(*r))


class Operation:
    def __init__(self, coordinates):
        self._coordinates = coordinates

        self._measure_mode = []
        self._measure_coor = []

    def get_permutation(self, operation):
        operated_coor = np.dot(operation, self._coordinates.T).T

        coor_list = []
        permu_list = []
        for iter in permutations(enumerate(operated_coor), len(operated_coor)):
            permu_coor = np.array([c[1] for c in iter])
            iter_num = [c[0] for c in iter]

            coor_list.append(np.average(np.linalg.norm(np.subtract(self._coordinates, permu_coor), axis=0)))
            permu_list.append(iter_num)

        return np.min(coor_list), permu_list[np.nanargmin(coor_list)]

    def get_measure(self):

        return np.array(self._measure_mode)
        # return np.average(self._measure_total_modes, axis=1)

    def get_coor_measure(self):
        #  normalization

        sum_list = []
        for r1 in self._coordinates:
            for r2 in self._coordinates:
                subs = np.subtract(r1, r2)
                sum_list.append(np.dot(subs, subs))
        d = np.average(sum_list)

        return np.average(self._measure_coor)/d


class Rotation(Operation):
    def __init__(self, coordinates, modes, axis, order):
        super().__init__(coordinates)

        self._axis = axis
        self._order = order

        for angle in np.arange(2*np.pi/order, 2*np.pi, 2*np.pi/order):
            operation = rotation(angle, rotation_axis)
            operated_coor = np.dot(operation, self._coordinates.T).T

            for mode in modes:

                operated_mode = np.dot(operation, prepare_vector(self._coordinates, mode).T).T - operated_coor
                norm_1 = np.linalg.norm(mode, axis=1)

                mesure_coor, permu  = self.get_permutation(operation)

                permu_mode = np.array(operated_mode)[permu]
                norm_2 = np.linalg.norm(permu_mode, axis=1)

                self._measure_mode.append(np.average(np.divide(np.diag(np.dot(mode, permu_mode.T)), norm_1 * norm_2)))
                self._measure_coor.append(mesure_coor)


class Rotation_old:
    def __init__(self, coordinates, modes, axis, order):
        self._axis = axis
        self._order = order
        self._coordinates = coordinates

        self._measure_total_modes = []
        for mode in modes:
            self._measure_mode = []
            self._measure_coor = []

            for angle in np.arange(2*np.pi/order, 2*np.pi, 2*np.pi/order):
                operation = rotation(angle, rotation_axis)

                operated_coor = np.dot(operation, self._coordinates.T).T
                operated_mode = np.dot(operation, prepare_vector(self._coordinates, mode).T).T - operated_coor
                norm_1 = np.linalg.norm(mode, axis=1)

                mode_list = []
                coor_list = []
                for iter_coor, iter_modes in zip(permutations(operated_coor, len(operated_coor)),
                                                 permutations(operated_mode, len(operated_coor))):

                    permu_coor = np.array(iter_coor).reshape(len(self._coordinates), -1)
                    permu_mode = np.array(iter_modes).reshape(len(self._coordinates), -1)

                    coor_list.append(np.average(np.linalg.norm(np.subtract(self._coordinates, permu_coor), axis=0)))

                    norm_2 = np.linalg.norm(permu_mode, axis=1)
                    mode_list.append(np.average(np.divide(np.diag(np.dot(mode, permu_mode.T)), norm_1 * norm_2)))

                self._measure_mode.append(mode_list[np.nanargmin(coor_list)])
                self._measure_coor.append(np.min(coor_list))

            self._measure_total_modes.append(self._measure_mode)

    def get_measure(self):
        print(self._measure_mode)
        return np.average(self._measure_total_modes, axis=1)

    def get_coor_measure(self):

        # normalization
        sum_list = []
        for r1 in self._coordinates:
            for r2 in self._coordinates:
                subs = np.subtract(r1, r2)
                sum_list.append(np.dot(subs, subs))
        d = np.average(sum_list)

        return np.average(self._measure_coor)/d


r = Rotation_old(water, complete_modes, rotation_axis, 2)
print('measure mode: ', r.get_measure())
print('measure coor', r.get_coor_measure())

print('---------')

r = Rotation(water, complete_modes, rotation_axis, 2)
print('measure mode: ', r.get_measure())
print('measure coor', r.get_coor_measure())

exit()

mode = complete_modes[2]

sum_list = []
for r1 in water:
    for r2 in water:
        subs = np.subtract(r1, r2)
        sum_list.append(np.dot(subs, subs))

d = np.average(sum_list)

measures = []
modes = []
for a in np.arange(0, 2*np.pi, 0.01):

    operation = rotation(a, rotation_axis)
    #operation = reflection([1, 0, 0])

    operated_water = np.dot(operation, water.T).T
    rotated_vector = np.dot(operation, prepare_vector(water, mode).T).T - operated_water
    print(rotated_vector)
    print('mode')
    print(mode)

    # print(mode[1], rotated_vector[0])
    norm = np.linalg.norm(mode, axis=1)
    #norm2 = np.linalg.norm(rotated_vector, axis=1)

    #mode_list = np.average(np.divide(np.diag(np.dot(mode, rotated_vector.T)), norm * norm2))
    #print('->', mode_list)

    #exit()
    mode_list = []
    measure_list = []
    for iter_water, iter_modes in zip(permutations(operated_water, len(operated_water)),
                                       permutations(rotated_vector, len(operated_water))):
        #print(iter_water)
        new_water = np.array(iter_water).reshape(len(water), -1)
        mode_water = np.array(iter_modes).reshape(len(water), -1)

        measure_list.append(np.average(np.linalg.norm(np.subtract(water, new_water), axis=0)))

        norm2 = np.linalg.norm(mode_water, axis=1)
        mode_list.append(np.average(np.divide(np.diag(np.dot(mode, mode_water.T)), norm * norm2)))
        #print('->', mode_list)

    #exit()
    #mode_list = np.multiply(mode_list, 1 - np.array(measure_list)/d)
    print('----')
    measures.append(np.min(measure_list)/d)
    modes.append(mode_list[np.nanargmin(measure_list)])
    #modes.append(np.max(mode_list))

overlap = (1 - np.array(measures))

#print(modes)
#exit()
plt.plot(np.arange(0, 2*np.pi, 0.01), measures, label='measure')
plt.plot(np.arange(0, 2*np.pi, 0.01), modes, label='modes')
#plt.plot(np.arange(0, 2*np.pi, 0.01), measure, label='measure')
plt.plot(np.arange(0, 2*np.pi, 0.01), overlap, '--', label='overlap')
plt.legend()

print(water)

a = Symgroupy(coordinates=water, group='ci')
print('csm', a.csm/100)

plt.show()
