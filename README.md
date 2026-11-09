# EnergyMonitoring

A prototype for analysing and visualising the energy consumption of industrial welding machines. It was built around the data model of a welding portal with robots, which is exposed over OPC UA, and it explores how that data can be turned into insights about where energy is spent and where it can be saved.

## Background

> Pemamek has the problem that they currently can not provide insights regarding energy consumption and energy saving potential of the welding machines to their customers. Our solution should deliver additional insights about energy consumption and provide optimization suggestions and automated solutions.

The goal is to give machine owners a clear picture of:

- how much energy a welding machine consumes in total,
- how that energy splits between **active** (welding) and **idle** time,
- how much energy is wasted while the machine is idle, which is the main source of saving potential.

## Project status

This is an early-stage prototype (school/project work from February 2024). It has two independent parts:

| File | What it does | Data source |
|---|---|---|
| `GUI.py` | Simulates a day of energy consumption, calculates totals and shows plots | Randomly generated |
| `main.py` | Reads the sample OPC UA export and prints hourly welding energy figures | `Resources/stopcua.json` |

The two parts are not yet connected: the plots currently run on simulated data, not on the JSON export.

## Features

### `GUI.py` – consumption simulation and visualisation

- Generates 24 hours of simulated consumption at 5-second intervals (17,280 samples). Active consumption is normally distributed (mean 16, standard deviation 0.7).
- Inserts random idle periods, during which consumption drops to a constant low value (2). The random seed is fixed (`45`), so results are reproducible.
- Calculates, and prints to the console:
  - total energy consumption (trapezoidal integration over time),
  - total active time and idle time in hours,
  - idle energy and active energy.
- Shows a Matplotlib figure with three panels:
  1. A 6-hour zoom of the consumption curve over time.
  2. A pie chart of idle vs. active **time**.
  3. A pie chart of idle vs. active **energy**.

### `main.py` – OPC UA data parsing

- Loads `Resources/stopcua.json` and extracts the machine, vision and hourly time data.
- Reads the hourly welding energy consumption and the robot welding time, then prints the welding energy per hour.

## Data model

The sample files in `Resources/` follow the naming of the machine's OPC UA structures (Hungarian-style prefixes such as `arr` for arrays, `st` for structs, `f` for floats, `n` for integers, `s` for strings and `dt` for date/times).

### `Resources/stopcua.json` – live machine data

- **`stMachineData`**: machine name and time, failure/warning/info message lists, number of running robots, and 24-value arrays of hourly energy consumption for the portal, the robots and welding.
- **`stVisionData`**: vision system status, timestamp, operator and station IDs, image/scan counters and stop source.
- **`stTimeVariablesHourly`**: hourly running time of the robots and portal, welding time, scanning time and waiting time.

### `Resources/stpersistopcua.json` – persisted production data

- **`arrstPanelData`**: per-workpiece weld counts and weld lengths (total, `Pf`, `Pb`), robot-specific figures, job list progress, panel start/end times and status.
- **`arrstRobotData`**: robot state flags (`bRunning`, `bWeldOn`, `bError`, `bIdle`) and daily weld counts and lengths.
- **`arrstTimeVariablesDaily`**: daily running and welding time per robot, plus portal running, scanning and waiting time.

## Getting started

### Requirements

- Python 3.8 or newer
- `numpy`, `pandas`, `matplotlib`

```bash
pip install numpy pandas matplotlib
```

### Run

```bash
git clone https://github.com/NProgrammerR/EnergyMonitoring.git
cd EnergyMonitoring

python GUI.py     # simulation, console output and plots
python main.py    # parse the sample OPC UA export
```

Run `main.py` from the repository root, because it opens `./Resources/stopcua.json` with a relative path.

On NumPy 2.0 or newer, `GUI.py` may need `np.trapz` replaced with `np.trapezoid`, since `trapz` was renamed.

## Repository structure

```
EnergyMonitoring/
├── GUI.py                       # simulation, calculations and plots
├── main.py                      # parses the sample OPC UA export
├── Resources/
│   ├── stopcua.json             # sample live machine data
│   └── stpersistopcua.json      # sample persisted production data
└── README.md
```

## Ideas for further development

- Feed the real OPC UA data (or a live OPC UA connection) into the calculations and plots instead of simulated values.
- Break consumption down by portal, robot and welding, using the hourly arrays already in the data model.
- Detect idle periods automatically and suggest optimisations, such as powering down equipment after a set idle time.
- Add a proper dashboard or GUI for customers to browse the results.

## Notes

- The sample data is example/test data, not real customer measurements.
- Energy units are not specified in the sample data. The simulation labels the energy pie chart in kWh, so check the units before relying on any numbers.
