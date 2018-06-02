# RL

A grid world is one of the canonical examples in reinforcement learning literature. This repository contains one such game where the goal is for an agent to discover treasure without falling into a pit of fire or other hazardous obstacles along the way. The purpose of this project is to implement reinforcement learning algorithms using a functional approach.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You'll need the following to be able to build and run the code

- OCaml 4.06.0
- [Base](https://github.com/janestreet/base)
- [Dune](https://github.com/ocaml/dune)

### Installing

After the appropriate packages are installed, you can build the project with dune

```
dune build @install
```

and run it with

```
./_build/default/bin/main.exe
```

## Running the tests

To run the tests using dune run

```
dune runtest
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
