# Charging stations distribution for e-mobility
[Paper Abstract]
[Paper Link]

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
- [Documentation](#documentation)
- [Future Work](#future-work)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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
│   ├── electromaps/  # Data from electromaps
│   ├── ine/  # Data from INE
├── docs/  # Documentation
├── simulation/  # Simulation folder
│   ├── agents/  # Agents used in the simulation
│   ├── model.py  # Model used in the simulation
│   ├── server.py  # Server configurations
│   ├── run.py  # File to run the simulation
└── requirements.txt  # Project dependencies
```

## Documentation
[Documentation]

## Future Work
[Future Work]

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
[Acknowledgments]
