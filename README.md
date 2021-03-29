# Interactive Folding Visualizer
IFV is a tool for visualizing RNA secondary structures and protein binding sites.

## Table of Contents

* [Requirements](#requirements)
* [Usage](#usage)
* [Contact](#contact)
* [License](#license)

## Requirements

In the requirements.txt all required packages are listed.

To install your packages using requirements.txt, execute the following:
1. Open a terminal or command prompt
2. Navigate to the folder with your requirements.txt
3. ``` pip3 install -r requirements.txt```
4. You are done installing dependencies

## Usage:

```
python3 ifv.py
```

optional input arguments
```
    -i, --input     Input directory containing the 4 folders: annotation, data, transcript and config.
                    Add new files according to the following principle:
                        annotation - 12-column .bed format
                        data - 4-column .bedgraph format and 6-column .bed format
                        transcript - transcript containing the sequence and foldings with corresponding energy
                        config - regions.txt and heatmaps.txt containing colors for the visualization
```
## File Examples
TODO

## Contact

For questions or problems, please feel free to write an email and I will get back to you as soon as possible.

[msohn@techfak.uni-bielefeld.de](mailto:msohn@techfak.uni-bielefeld.de)
.

## License

* The dash package is licensed under the [MIT license](https://github.com/plotly/dash/blob/dev/LICENSE).
* The visdccc package is licensed under the [MIT license](https://github.com/jimmybow/visdcc/blob/master/LICENSE.txt).
* The plotly package is licensed under the [MIT license](https://github.com/plotly/plotly.py/blob/master/LICENSE.txt).
* The sklearn package is licensed under the [3-Clause BSD license](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING).
* IFV is licensed under the [MIT license](https://github.com/masohn/IFV/blob/main/LICENSE).
