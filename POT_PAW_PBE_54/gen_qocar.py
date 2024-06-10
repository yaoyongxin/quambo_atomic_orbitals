import numpy, os
import matplotlib.pyplot as plt
import fortranformat as ff



def get_waves(path):
    lines = open(path, "r").readlines()
    data = []
    keys = ["grid", "pseudo wavefunction", "ae wavefunction"]
    mode = 0
    for line in lines:
        if any(key in line[:20] for key in keys):
            mode = 1
            data.append([])
        elif mode == 1:
            if line[1].isalpha():
                mode = 0
                continue
            data[-1].extend(numpy.asarray(line.strip().replace("  ", " ").split(" "), dtype=float))
    return data


def chk_data(data, inds):
    print(f"{len(data)} entries.")
    cs = ['k', 'r', 'b', 'm', 'g']
    for i, ind in enumerate(inds):
        plt.plot(data[0], data[ind*2+1], ls='-', color=cs[i], label=str(i))
        plt.plot(data[0], data[ind*2+2], ls='--', color=cs[i])
    plt.legend()
    plt.show()


def chk_data_all(data):
    for ind in range(len(data)//2):
        plt.plot(data[0], data[ind*2+1], ls='-')
        plt.plot(data[0], data[ind*2+2], ls='--')
    plt.show()


def save_qocar(data, path, inds, lls):
    dname = path.split("/")[-2]
    if not os.path.isdir(dname):
        os.mkdir(dname)

    lineformat = ff.FortranRecordWriter('(2E20.12)')
    with open(f"{dname}/QOCAR", "w") as f:
        f.write(f"& {dname}  {len(lls)}  {len(data[0])} a ! ELEMENT  LDIM  NMAX\n")
        f.write("& " + " ".join(["T"]*len(lls)) + "\n")
        f.write("& " + " ".join(["0.0"]*len(lls)) + "\n")
        for ind, ll in zip(inds, lls):
            f.write(f"& {ll} = L\n")
            f.write(lineformat.write(numpy.vstack((data[0], data[ind*2+1])).T.reshape(-1))+"\n")
        f.write("&")


if __name__ == "__main__":
    path = "../../vasp_pot/POT_PAW_PBE_54/Gd/POTCAR"
    # Rare earth, 5s, 6s, 5p, 5d, 4f
    inds = [0, 1, 2, 4, 6]
    lls = [0, 0, 1, 2, 3]

    # s, p
    # inds = [0, 2]
    # lls = [0, 1]

    data = get_waves(path)
    chk_data(data, inds)
    chk_data_all(data)
    save_qocar(data, path, inds, lls)
