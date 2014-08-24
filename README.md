Pyort
=====

An open url shortener for geeks by geeks


## Prerequisites


### External libs for Pillow

See: https://pillow.readthedocs.org/en/latest/installation.html#simple-installation

```
$ sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
```


### Virtualenv

You should have a virtualenv ready with either Python 2.7.x or 3.x


### Database

This app is configured with PostgreSQL/MySQL in mind.


### Configuration

Under your project's settings folder you'll find a `config.json` file. Fill it out with the needed
values. Alternatively you can also create a `config-user.json` for configurations specific to a
particular environment.

You'll also see a `config-sample.json` in the source file to serve as a starter. Rename and fill it
out accordingly.


### Server settings

TODO


## Demo

```
http://pyort-demo.mattlebrun.com
```
