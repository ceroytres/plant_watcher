# Setup Simple Luxmeter

## Requirements
This part can be run on a your personal machine or Raspberry Pi.

* OS: MacOS, Windows, Linux, Raspbian Buster
* Python 
* Scipy
* Optional [Sklearn]   

## Steps
1. Using a multimeter using measure the resistance across the photoresistor, and measure the correpsonding lux level using a luxmeter. Record values in a csv file with resistance being the first column, and lux being the second column as shown below:
```
R0,L0
R1,L1
```
2. In order to create a fitted lux model
```bash
./tools/fit_lux_lr.py --input <input data path> --output <output model path> 
```
and optional flag maybe passed ```--robust``` which fits to the collected data using [Huber regression](https://scikit-learn.org/stable/modules/linear_model.html#huber-regression) instead of least squares. 

### Resources
* List luxmeter apps:
    - For iOS, [Lux Light Meter Pro](https://itunes.apple.com/us/app/lux-light-meter-pro/id1292598866?mt=8)
    - [Full list](https://www.photoworkout.com/best-light-meter-apps/)

### Reference
This simple luxmeter is based on:

[Williams, David. “Design a Luxmeter Using a Light Dependent Resistor - Projects.” All About Circuits, 15 Dec. 2015, www.allaboutcircuits.com/projects/design-a-luxmeter-using-a-light-dependent-resistor/. ](www.allaboutcircuits.com/projects/design-a-luxmeter-using-a-light-dependent-resistor/)