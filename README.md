# germina-bridge-gen

Small Python CLI that generates bridges from a bundle manifest (`bundle.json`) using Jinja templates.

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Command format:

```bash
python germina-bridge-gen.py <target> <manifest> <output>
```

Arguments:

- `target`: currently only `cpp`
- `manifest`: path to input `bundle.json`
- `output`: path to generated header file


## Development

Run local help:

```bash
python germina-bridge-gen.py --help
```

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
