import sys
import re
import matplotlib.pyplot as plt

color_list = [
        # scanf, sizeof, color
        ( "0", "1",  "yellow" ),
        ( "1", "1",  "orange" ),
        ( "0", "0",  "lime" ),
        ( "1", "0",  "cyan" ),
        ]

def do_plot(nb, data, base_name):
    # data = {
    #        "avr": { "y":[], "col":[] },
    #        "usr": { "y":[], "col":[] },
    #        "sys": { "y":[], "col":[] },
    #        }
    fig = plt.figure()
    # avr
    ax1 = fig.add_subplot(1,4,1)
    ax1.scatter([nb for _ in data["avr"]["y"]], data["avr"]["y"],
                 color=data["avr"]["col"], alpha=0.8)
    ax1.set_xticks([nb])
    ax1.set_xticklabels(["avr"])
    ax1.set_ylim([3.25, 8.25])
    ax1.set_ylabel("average (s)")
    # usr
    ax2 = fig.add_subplot(1,4,2)
    ax2.scatter([nb for _ in data["usr"]["y"]], data["usr"]["y"],
                 color=data["usr"]["col"], alpha=0.8)
    ax2.set_xticks([nb])
    ax2.set_xticklabels(["usr"])
    ax2.set_ylim([0.30, 0.70])
    ax2.set_ylabel("user (s)")
    # sys
    ax3 = fig.add_subplot(1,4,3)
    ax3.scatter([nb for _ in data["sys"]["y"]], data["sys"]["y"],
                 color=data["sys"]["col"], alpha=0.8)
    ax3.set_xticks([nb])
    ax3.set_xticklabels(["sys"])
    ax3.set_ylim([1.20, 2.45])
    ax3.set_ylabel("sys (s)")
    # for legend
    ax4 = fig.add_subplot(1,4,4)
    ax4.scatter(1, 5, color="black")
    ax4.set_xlim([0, 2])
    ax4.set_ylim([4, 6])
    ax4.set_xticks([1])
    ax4.set_xticklabels([])
    ax4.set_yticks([5])
    ax4.set_yticklabels([])
    #ax4.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
    #ax4.tick_params(axis="y", which="both", bottom=False, top=False, labelbottom=False)
    ax4.annotate("no scanf, sizeof", size=5, color="black",
                 xy=(0.4, 5.0), xytext=(0.4, 5.3),
                 bbox=dict(boxstyle="square", fc="yellow", ec="yellow"))
    ax4.annotate("scanf, sizeof", size=5, color="black",
                 xy=(0.4, 5.2), xytext=(0.4, 5.2),
                 bbox=dict(boxstyle="square", fc="orange", ec="orange"))
    ax4.annotate("no scanf, textlen", size=5, color="black",
                 xy=(0.4, 5.1), xytext=(0.4, 5.1),
                 bbox=dict(boxstyle="square", fc="lime", ec="lime"))
    ax4.annotate("scanf, textlen", size=5, color="black",
                 xy=(0.4, 5.0), xytext=(0.4, 5.0),
                 bbox=dict(boxstyle="square", fc="cyan", ec="cyan"))
    #
    fig.tight_layout()
    plt.savefig("{}-{:02d}.png".format(base_name, nb))
    plt.show()

def find_color(a, b):
    for x in color_list:
        if x[0] == a and x[1] == b:
            return x[2]
    raise ValueError("ERROR: invalid type of a (or b)")

#
# main
#
if len(sys.argv) == 1:
    print("Usage: plot.py (file)")
    exit(1)

csv_file = sys.argv[1]
base_name = csv_file.rsplit(".", 1)[0]

re_sep = re.compile("^## NB_TEST=(\d+)")
base_data = []
with open(csv_file) as fd:
    for line in fd:
        line = line.strip()
        r = re_sep.match(line)
        if r:
            base_data.append({"nb_test": r.group(1), "data": []})
            data_list = base_data[-1]["data"]
            continue
        base_data[-1]["data"].append(line.split(","))

for z in base_data:
    print(z)
    nb = int(z["nb_test"])
    data = {
            "avr": { "y":[], "col":[] },
            "usr": { "y":[], "col":[] },
            "sys": { "y":[], "col":[] },
            }
    """
    for d in sorted(z["data"], key=lambda x:x[2], reverse=True):
        data["avr"]["y"].append(d[2])
        data["avr"]["col"].append(find_color(d[0], d[1]))
    for d in sorted(z["data"], key=lambda x:x[3], reverse=True):
        data["usr"]["y"].append(d[3])
        data["usr"]["col"].append(find_color(d[0], d[1]))
    for d in sorted(z["data"], key=lambda x:x[4], reverse=True):
        data["sys"]["y"].append(d[4])
        data["sys"]["col"].append(find_color(d[0], d[1]))
    """
    # e.g. 0,0,6.524981,6.52,0.54,2.05
    for d in z["data"]:
        data["avr"]["y"].append(float(d[2]))
        data["avr"]["col"].append(find_color(d[0], d[1]))
    for d in z["data"]:
        data["usr"]["y"].append(float(d[4]))
        data["usr"]["col"].append(find_color(d[0], d[1]))
    for d in z["data"]:
        data["sys"]["y"].append(float(d[5]))
        data["sys"]["col"].append(find_color(d[0], d[1]))
    #
    do_plot(nb, data, base_name)

