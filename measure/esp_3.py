from lab_lib import *
from errorlib import measure

FONDO_SCALA = 0.16
dv = FONDO_SCALA / (2 ** 8)

R_M = measure('R_M', 982000.0, 'R')
R_ck = measure('R_ck', 99219.6, 'R')
R_k = measure('R_k', 1001.4, 'R')
R10_1 = measure('R10_1', 9.963, 'R')
R10k_1 = measure('R10k_1', 9906, 'R')
R10_2 = measure('R10_2', 10.003, 'R')
R10k_2 = measure('R10k_2', 9926.4, 'R')

print R_M, 'R_M'
print R_ck, 'R_ck'
print R_k, 'R_k'
print R10_1, 'R10_1'
print R10k_1, 'R10k_1'
print R10_2, 'R10_2'
print R10k_2, 'R10k_2'


# Direct measurament offset
V_off = measure('V_off', -1.484 * 10 ** -3, 'V')

print 'Direct measurament V offset:', V_off

# Amplified measurament with bias current


V_out = measure('V_out', -1.3265, 'V')
v = V_out.value / (1 + R10k_1.value / R10_1.value)
V_off_1 = measure('V_off_1', v)
V_off_1.calculate_error('V_out / (1 + R10k_1 / R10_1)', [V_out, R10k_1, R10_1])

print 'Amplified measurament with bias current', V_off_1

# Amplified without polarized current

