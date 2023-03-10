# ecoVAD_chirpR
## A modified version of [ecoVAD](https://github.com/NINAnor/ecoVAD)

![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)

## Introduction

This is a modified version of [ecoVAD](https://github.com/NINAnor/ecoVAD) for integration in to chirpR including models for analyzing acoustic recordings in urban environments.

ecoVAD was developed by Cretois et al. (2022) and should be cited as such.

```
Cretois, B., Rosten, C. M., & Sethi, S. S. (2022). Voice activity detection in eco-acoustic data enables privacy protection and is a proxy for human disturbance. Methods in Ecology and Evolution, 00,   1–10 .   https://doi.org/10.1111/2041-210X.14005
```

In keeping with the license requirements this version of ecoVAD is redistributed under the same license: 
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/

## Change list
- Removed Docker
- Removed poetry
- Created dependencies.txt
    - For use with a virtualenv and reticulate in R
- Removed notebooks
