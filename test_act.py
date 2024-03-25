import numpy as np
import matplotlib.pyplot as plt

config = {
    "initial_value": 3500,
    "decrease_rate": 0.1,
    "time_seconds": np.arange(0, 33 * 10, 1),
    "immute": 0.75,
    "damage": 0,
    "self_increment": 0
}

heart = False

x_values = [config["initial_value"] - config["damage"]]
for i in config["time_seconds"]:
    decr = 200 + config["initial_value"] * 0.035 + (x_values[-1] * config["decrease_rate"] + 20) * config["immute"]
    incr = config["self_increment"] + config["initial_value"] * 0.016 if heart else 0
    x_values.append(
        x_values[-1] + (incr - decr) / 33)

x_values.pop(-1)

# 绘制曲线
plt.figure(figsize=(10, 6))
plt.plot(config["time_seconds"] / 33, x_values, marker='o', linestyle='-', color='b')

end_sec = 8
point = (end_sec, x_values[33 * end_sec])
plt.plot(point[0], point[1], marker='o', markersize=10, color='red')
# 添加文本注释
plt.text(point[0], point[1], str(round(point[1], 1)), fontdict={'family': 'serif', 'size': 16, 'color': 'black'},
         ha='center',
         va='center')

plt.title(f'Value of x, immute = {config["immute"]}, damage =  {config["damage"]}')
plt.xlabel('Time (seconds)')
plt.ylabel('Value of x')
plt.grid(True)
plt.savefig("result.png")
plt.show()
