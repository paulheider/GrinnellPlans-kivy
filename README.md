GrinnellPlans-kivy
==================

A [Kivy app](https://www.kivy.org "Kivy's Homepage") for interfacing with [GrinnellPlans](https://github.com/grinnellplans/grinnellplans-php/ "GrinnellPlan's Code Repo")

Liscensing
----------

Following the current Plans codebase, this code is released under [GPL v. 3](http://www.gnu.org/licenses/gpl.txt):

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Roadmap
-------



Contributing
------------

Submit bugs and ideas to `[heider]` on Plans or via [this repo's issues page](https://github.com/paulheider/GrinnellPlans-kivy/issues)

Building from Source
--------------------

### Android

Android compatible versions can be built with [Buildozer](https://github.com/kivy/buildozer "Buildozer's Code Repo") using the included `buildozer.spec` file:

```bash
## Build a deployable APK
buildozer android_new debug

## Build and deploy an APK to a connected device
buildozer android_new debug deploy

## Build, deploy, and run an APK to a connected device
buildozer android_new debug deploy run
```

#### Permissions

1. Internet

   Internet access is necessary to login, pull the autofinger lists, and pull plans from the Plans database
   
2. USB Storage
   
   The app saves configuration details locally, which requires read/modify/delete permissions.


### iOS

(untested)

### Linux

The application can be run from the terminal on a linux machine:

```bash
python main.py
```

### Windows

(untested)
