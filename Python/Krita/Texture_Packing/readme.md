# Texture Packing
A Python plugin for use in [Krita](https://krita.org).

## What is Texture Packing?
A Python plugin made specifically for [Krita](https://krita.org) that allows bundling specific channels of textures (Red, Green, Blue) into other channels. This is a technique commonly used in videogame development to reduce the number of textures called and, thus, improve performance.

## Functionalities
When executed, this plugin will open a window asking what should be the size of the final texture (no scaling is done, so the input files should all be of this size), what channel from the provided texture should be used, and what input files should be used.

## Download, Install & Execute
### Download
+ **[ZIP ARCHIVE - v1.0](https://github.com/esuriddick/Programming/raw/main/Python/Krita/DDS_File_Importer/Downloads/DDS_File_Importer_v1.0.zip)**

### Installation
There are two different ways to install Python plugins in [Krita](https://krita.org):
#### First Method
1. Open [Krita](https://krita.org) and go to _Tools_ > _Scripts_ > _Import Python Plugins..._, and select the **Texture_Packing.zip** archive.
2. Restart [Krita](https://krita.org).
3. Go to _Settings_ > _Configure Krita..._ > _Python Plugin Manager_, and click the checkbox to the left of the field that says **Texture Packing**.
4. Restart [Krita](https://krita.org).

#### Second Method
1. Extract the content within the **Texture_Packing.zip** archive to the folder **pykrita** (typically located here: C:\Users\USERNAME\AppData\Roaming\krita, where **USERNAME** should be replaced with your Windows username).
2. Restart [Krita](https://krita.org).
3. Go to _Settings_ > _Configure Krita..._ > _Python Plugin Manager_, and click the checkbox to the left of the field that says **Texture Packing**.
4. Restart [Krita](https://krita.org).

### Execute
Go to the menu item _Tools_ > _Scripts_, and press the option named _Texture Packing_. Unfortunately, the Python code has to be completed before some final steps are taken, otherwise Krita crashed every time I tried. Once the Python code is completed, it will let you know where is the final script located in your system for you to copy it and use inside _Tools_ > _Scripts_ > Scripter. This final script will make it so that each channel only has the information defined by the user, including the alpha channel.

### Tested platforms
I have tested version 1.0 of this plugin in version 5.2.2 of [Krita](https://krita.org).

## Change log
_[2023-09-04] Version 1.0_
- Initial version released.

## License
As identified in this repository, all of the work shared in this repository is under the GNU General Public License v3.0.

_Summary of the GNU General Public License v3.0_: Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.
