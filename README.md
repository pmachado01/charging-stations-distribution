# Charging stations distribution for e-mobility
This study addresses the critical need for sustainable urban development by focusing on the strategic distribution of charging stations for electric vehicles (EVs). Leveraging modeling and simulation, the paper extracts and examines behavioral information to guide effective decision-making for problem-solving. The challenge lies in bridging the modeling to reality, considering the scarcity of available data, the distinctive charging dynamics of EVs, and market uncertainties. The current study effectively analyzes the distribution of charging stations in Porto, evaluating factors that influence the electric vehicle charging system through the simulation of various scenarios. These scenarios include unexpected increases in the quantity of EVs and reductions in EVs' range, providing valuable insights for optimizing infrastructure in alignment with urban dynamics.

[Paper](./docs/Charging_stations_distribution_for_e_mobility.pdf)

https://github.com/pmachado01/charging-stations-distribution/assets/57841600/c5122a77-8590-43c0-b54c-96ea08b54dce

| Name | Email |
| ---- | ----- |
| Francisco Cerqueira | up201905337@edu.fe.up.pt
| Luís Matos | up201905962@edu.fe.up.pt
| Pedro Machado | up201906712@edu.fe.up.pt

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Installation

### Prerequisites
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [Make](https://www.gnu.org/software/make/)

### Setup
1. Clone the repository
```bash
git clone git@github.com:pmachado01/charging-stations-distribution.git
```
2. Install the dependencies
```bash
pip install -r requirements.txt
```

## Usage
The simulation is hosted at `http://localhost:8521/`.

### Pipeline
To run the entire pipeline of the project, execute the following command in the root directory:
```bash
make CALCULATE_DISTANCE_MATRIX=true
```
To avoid calculating the distance matrix, in case it was previously calculated, you can set the above flag to `false`.

### Individual Components
To run individual components of the pipeline, you can specify the make label corresponding to that component:
```bash
make {COMPONENT}
```
where `{COMPONENT}` can be one of the following: `data_processing`, `simulation`, or `analysis`.

### Clean
To erase the processed data and logs, you can execute the command:
```bash
make clean
```

## Project Structure
```python
charging-stations-distribution/
├── data/  # Data used in the project
│   ├── processed/  # Generated data after the data processing step
│   └── raw/  # Raw data from INE, Electromaps, and Idealista
├── docs/  # Documentation files (report and presentation)
├── logs/  # Generated log files from data analysis
├── src/  # Simulation folder
│   ├── analysis/  # Scripts used for data analysis
│   ├── processing/  # Scripts used for data processing
│   ├── simulation/  # Folder containing simulation modules
│   │   ├── agents/  # Agents used in the simulation
│   │   ├── model.py  # Model used in the simulation
│   │   ├── server.py  # Server configurations
│   │   └── run.py  # File to run the simulation
│   └── simulation/  # Folder containing utility code (Project constants and file loading)
├── Makefile  # Makefile used to execute the project pipeline
└── requirements.txt  # Project dependencies
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
