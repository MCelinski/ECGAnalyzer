<!--
repo name: ECGAnalyzer
description: An awesome README template to jumpstart your projects!
github name:  MCelinski
link: https://github.com/MCelinski/ECGAnalyzer
logo path: readmeimages/ecgg.png
screenshot: readmeimages/ss1.png
email: michalcelinski00@gmail.com
-->



<!-- PROJECT LOGO -->
<br />
<p align="center">
    <a href="LINK">
        <img src="readmeimages/ecgg.png" alt="Logo" width="80" height="80">
    </a>
    <p align="center">
        <b>ECGAnalyzer</b>
        <br />
    </p>




<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project
This is Graphical interface for visualization and processing of ECG WFDB signals.
[![Product Name Screen Shot][product-screenshot]](readmeimages/ss1.png)

## Features
- Import a WFDB file and plot ecg signal in 
single or cascade mode.
- Show info about signal and patient.
- Analyze R-R distance and HR. 
- FFT Filtering.
- Relload next seconds of signals.
- Read Annotation from .atr file.
- Add your own annotation.
- Save image of signal.
## Installation

1. Clone the repo
```sh
git clone https://github.com/MCelinski/ECGAnalyzer.git
```
2. Install requriements.txt
```sh
pip install -r /path/to/requirements.txt
```
3. Run python file
```JS
python ECGAnalyzer.py
```
## Usage

To use ECGAnalyzer 
* Choose type of view you want to watch ECG signal
* Load WFDB .dat file 
[![Loading data][loading-data]](readmeimages/ss2.png)

To Add Annotation
* With loaded signal on single mode click load annotation
* Click Add Annotaion and input the time in s and Symbol of annotation (Must be a char)
* Click Add annotation
[![Adding Annotation][add-annotation]](readmeimages/ss3.png)

:bangbang: Important :bangbang:

If you want to impoort another data first you must chose view mode again to reload the canvas. Otherwise bugs may appeares.




## Contact

Michał Celiński 
Email: michalcelinski00@gmail.com

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: readmeimages/ss1.png
[loading-data]: readmeimages/ss2.png
[add-annotation]: readmeimages/ss3.png

