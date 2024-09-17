## 2024-09-?? - New model, python API, CLI (in Rust), and Rust bindings

TODO: clean up.

We are releasing a number of new things, and they are ready for testing!

News:
- A new ML model with support for [200+ content types](./assets/models/standard_v2_1/README.md).
- A new CLI written in Rust. This replaces the previous CLI written in python. More information [here](./docs/command_line_interface.md).
- A crate for applications written in rust, see [docs](./docs/rust.md).
- Python package 0.6.0-rc.0: a new model with support for 200+ content types, a CLI written in Rust, and a revamped Python API with a few breaking changes, see the [changelog](./python/CHANGELOG.md)! Get it with `pip install magika==???`.


## 2024-02-15 - Initial Release

- Magika goes open source, with model v1 (~100 supported content types), a python API, a CLI written in python, and an experimental module in tfjs.