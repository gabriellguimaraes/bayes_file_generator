# bayes_file_generator

`bayes_file_generator` is a small Python CLI for generating Latin hypercube design points and plain-text parameter files for heavy-ion collision simulation studies that use iEBE-MUSIC-style parameter inputs.

## Scope

The first version is:

- YAML config input.
- Uniform priors only.
- Latin hypercube sampling only.
- One `design_points.csv` file with the point index and all free parameters.
- One `bayes_file_<index>.dat` per design point containing `parameter value` lines.

## Installation

```bash
python3 -m pip install -e .
```

For development and tests:

```bash
python3 -m pip install -e .[dev]
```

## Usage

```bash
bayes-file-generator examples/basic_config.yaml
```

You can override the output directory at runtime:

```bash
bayes-file-generator examples/basic_config.yaml --output-dir ./run_output
```

## Config schema

```yaml
output_dir: ./output
random_seed: 7

sampling:
  method: latin_hypercube
  n_design_points: 4

parameters:
  - name: eta_over_s
    prior: uniform
    bounds: [0.08, 0.24]
  - name: tau0
    prior: uniform
    bounds: [0.2, 1.0]
```

Notes:

- `output_dir` is optional and defaults to `./output` relative to the config file.
- `random_seed` is optional.
- Indices are 0-based.
- Numeric values are written with a stable `%.12g`-style format.

## Output layout

Running the tool creates:

```text
output/
  design_points.csv
  bayes_files/
    bayes_file_0.dat
    bayes_file_1.dat
    ...
```

`design_points.csv` contains one header row followed by one row per design point.

Each `bayes_file_<index>.dat` contains lines like:

```text
eta_over_s 0.141337979113
tau0 0.57831948046
```

## Development

Run the test suite with:

```bash
pytest
```