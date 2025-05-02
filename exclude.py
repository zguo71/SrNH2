input_file = "input"
output_file = "input.new"
ref_energy = -3233.597872877419377
threshold_wavenumber = 2000
hartree_to_wavenumber = 219474.63137

with open(input_file, 'r') as f:
    lines = f.readlines()

with open(output_file, 'w') as f:
    for line in lines[4:]:
        abse = float(line.split()[-1])
        rele = abse - ref_energy
        rele_cm = rele * hartree_to_wavenumber
        if rele_cm <= threshold_wavenumber:
            f.write(line)



    
