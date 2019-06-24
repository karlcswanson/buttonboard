# Buttonboard
Buttonboard is a simple Raspberry Pi based OSC controller for D3 Media Servers.


## Hardware
* Raspberry Pi
* [Raspberry Pi Screw Terminal Breakout Module](https://www.amazon.com/gp/product/B01M27459S/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
* [PoE Micro USB Power Supply](https://www.amazon.com/gp/product/B01MDLUSE7/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)

## Software
### Installation
Install python3-pip package manager
```
$ sudo apt-get update
$ sudo apt-get install git python3-pip
```

Download buttonboard
```
$ git clone https://github.com/karlcswanson/buttonboard.git
```

Install buttonboard package dependencies
```
$ cd buttonboard/
$ pip3 install -r requirements.txt
```
