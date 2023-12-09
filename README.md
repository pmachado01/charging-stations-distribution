# Charging stations distribution for e-mobility
[Brief Description]

[Some images]

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
To start the MESA server, run the following command:
```bash
mesa runserver simulation
```
Then, open your browser and go to `http://localhost:8521/`.

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
