input_file = "input_xabc"
output_file = "input_new"
ref_energy = [-3233.597872877419377, -3233.532946475688732, -3233.530968466364357, -3233.524213783323830]
threshold_wavenumber = 2000
hartree_to_wavenumber = 219474.63137

with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
    for line in fin:
        parts = line.split()
        energies = list(map(float, parts[-4:]))
        rel_cm = [(e - ref_energy[i]) * hartree_to_wavenumber for i, e in enumerate(energies)]

        if any(val <= threshold_wavenumber for val in rel_cm):
            fout.write(line)
