# String search and replace
configs_xxx = "XXX"

with open(r'ne.dat', 'r') as file:
    energy = []
    for line in file:
        a = line.split()
        energy.append(str(a[1]))

with open(r'configs.fit.fixed', 'r') as file:
        data = file.read()
        for i in range(len(energy)):
            data = data.replace(configs_xxx, energy[i], 1)

with open(r'configs.fit.fixed', 'w') as file:
    file.write(data)
