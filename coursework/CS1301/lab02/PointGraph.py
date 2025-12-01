import matplotlib.pyplot as plt

def plot_points(csv_file):
    xs, ys = [], []
    try:
        with open(csv_file) as f:
            f.readline()  # skip header: "x,y" -- If no header, will just skip one line of position data
            for line in f:
                x_str, y_str = line.strip().split(",")
                xs.append(float(x_str))
                ys.append(float(y_str)) # make two parallel lists of each x and y value

        plt.scatter(xs, ys, c='blue', marker='o') # plot our points

        plt.axhline(0, color='black', linewidth=0.8) # add our axis
        plt.axvline(0, color='black', linewidth=0.8)

        plt.gca().set_aspect('equal', adjustable='box') # keep axis ration the same so we don't stretch points

        plt.xlim(min(xs) - 20, max(xs) + 20) # add some buffer room so our graph has space
        plt.ylim(min(ys) - 20, max(ys) + 20)

        plt.xlabel("X Direction") # add labels
        plt.ylabel("Y Direction")
        plt.title("Where does the robot go?")
        plt.show()
    except FileNotFoundError:
        print("I couldn't find the file \"PositionData.csv\"! (Make sure that it is named correctly and in the same folder)")

# Run
plot_points("PositionData.csv")