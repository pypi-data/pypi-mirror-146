# TimeAwarePC: A Python Package for Finding Causal Connectivity from Time Series Data  [![Documentation Status](https://readthedocs.org/projects/timeawarepc/badge/?version=latest)](https://timeawarepc.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/timeawarepc.svg)](https://badge.fury.io/py/timeawarepc)
**TimeAwarePC** is a Python package that implements the Time-Aware PC Algorithm for finding the **Causal Functional Connectivity** from time series data, based on recent research in directed probabilistic graphical modeling with time series [[1]](#Citation). The package also includes implementations of Granger Causality and the PC algorithm.

<p align="center">
[<img src="https://github.com/shlizee/TimeAwarePC/blob/main/imgs/Schematic.png" width="500" height="250"/>](https://github.com/shlizee/TimeAwarePC/blob/main/imgs/Schematic.png)
</p>

## Installation

You can get the latest version of Time-Aware PC by cloning the repository:

```
git clone -b main https://github.com/shlizee/TimeAwarePC.git
cd TimeAwarePC
pip install .
```

## Requirements
- Python >=3.6
- Python packages automatically checked and installed as part of the setup. To use Granger Causality, additional dependency of ```nitime``` which can be installed by ```pip install nitime```.
- R >=4.0
- R package ```kpcalg``` and its dependencies. They can be installed in R or RStudio as follows:
```
install.packages("BiocManager")
BiocManager::install("graph")
BiocManager::install("RBGL")
install.packages("pcalg")
install.packages("kpcalg")
```
<!-- - In addition, if you like to use Granger Causality functions in this package, please separately install nitime as follows:
```
pip install nitime
``` -->

## Documentation

[Documentation is available at readthedocs.org](https://timeawarepc.readthedocs.io/en/latest/)

## Tutorial

See the [tutorial.py](https://github.com/shlizee/TimeAwarePC/blob/main/timeawarepc/tutorial.py) for a quick tutorial of the main functionalities of this library and check if it is installed properly. 
<!-- 
## Documentation

[Documentation is available at readthedocs.org](https://timeaware-pc.readthedocs.io/en/latest/) -->

## Contributing

Your help is absolutely welcome! Please do reach out or create a feature branch!

## Citation

Biswas, R., & Shlizerman, E. (2022). Statistical Perspective on Functional and Causal Neural Connectomics: The Time-Aware PC Algorithm. https://arxiv.org/abs/2204.04845

Biswas, R., & Shlizerman, E. (2021). Statistical Perspective on Functional and Causal Neural Connectomics: A Comparative Study. Frontiers in Systems Neuroscience. https://doi.org/10.3389/fnsys.2022.817962


## References

R Clay Reid. (2012) From functional architecture to functional connectomics. Neuron, 75(2):209–217.

Smith, S. M., Miller, K. L., Salimi-Khorshidi, G., Webster, M., Beckmann, C. F., Nichols, T. E., ... & Woolrich, M. W. (2011). Network modelling methods for FMRI. Neuroimage, 54(2), 875-891.

Judea Pearl. (2009) Causality. Cambridge University press.

Markus Kalisch and Peter Bhlmann. (2007) Estimating high-dimensional directed acyclic graphs with the pc-algorithm. In The Journal of Machine Learning Research, Vol. 8, pp. 613-636.

Peter Spirtes, Clark N Glymour, Richard Scheines, and David Heckerman. (2000) Causation, prediction, and search. MIT press.



