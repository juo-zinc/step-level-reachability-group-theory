# Step-Level Reachability: A Group-Theoretic Analysis

This repository contains a rigorous group-theoretic study of
*step-level reachability* in a constrained discrete system, motivated by
the Roux method for the 3×3 Rubik’s Cube.

The main result shows that the set of corner configurations reachable
under fixed block constraints forms a semidirect product
S4 semidirect (Z/3Z)^3
yielding exactly 648 reachable corner states.

---

## Mathematical Content

The work is formulated entirely in the language of group theory and
includes:

- A precise definition of a block-preserving stabilizer subgroup
- A natural projection homomorphism onto corner permutation and
  orientation data
- A general generating criterion for semidirect products
- Explicit generators realizing full step-level reachability

Once the explicit generators are established, the core argument is
purely theoretical.

---

## Structure of the Repository

- `paper/`
  - `main.tex` — LaTeX source of the manuscript
  - `main.pdf` — Compiled PDF for easy reading
- `code/`
  - `full_cubie_tracking.py` — Python script for finite,
    computer-assisted verification of explicit move sequences

The Python script is used only to verify finite, explicit cases; it does
not replace any part of the theoretical argument.

---

## Intended Audience

This repository is intended for readers with background in abstract
algebra, group actions, or discrete mathematics. Familiarity with the
Rubik’s Cube is *not* required to follow the main mathematical ideas.

---

## License

This project is released under the MIT License.
