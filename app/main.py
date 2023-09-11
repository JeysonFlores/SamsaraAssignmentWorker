import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint


def get_random():
    return randint(0, 10)


class App:
    def __init__(self):
        self.figure = plt.figure()
        self.graph = self.figure.subplots(3, 1)
        self.values = {
            "door": {
                "values": [],
                "dates": [],
                "graph": {
                    "title": "Door Status",
                    "ylabel": "Is Open (True/False)",
                    "xlabel": "Timestamp",
                }
            },
            "temperature": {
                "values": [],
                "dates": [],
                "graph": {
                    "title": "Temperature",
                    "ylabel": "Degrees (°C)",
                    "xlabel": "Timestamp",
                }
            },
            "humidity": {
                "values": [],
                "dates": [],
                "graph": {
                    "title": "Humidity",
                    "ylabel": "Percentage (%)",
                    "xlabel": "Timestamp",
                }
            }
        }

    def _parse_data(self, door_data, temperature_data, humidity_data):
        pass

    def _refresh(self, i):
        for idx, key in enumerate(self.values.keys()):
            self.values[key]["dates"].append(dt.datetime.now().strftime('%H:%M:%S.%f'))
            self.values[key]["values"].append(round(get_random(), 2))

            self.values[key]["dates"] = self.values[key]["dates"][-20:]
            self.values[key]["values"] = self.values[key]["values"][-20:]

            self.graph[idx].clear()
            self.graph[idx].plot(self.values[key]["dates"], self.values[key]["values"])
            self.graph[idx].set_title(self.values[key]["graph"]["title"])
            self.graph[idx].set_ylabel(self.values[key]["graph"]["ylabel"])
            self.graph[idx].set_xlabel(self.values[key]["graph"]["xlabel"])
            self.graph[idx].tick_params(axis="both", labelsize=6)

        # Format plot
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()

    def start(self):
        ani = animation.FuncAnimation(self.figure, self._refresh, interval=1000, blit=False)
        plt.show()


if __name__ == "__main__":
    app = App()
    app.start()