# DDS File Importer (Windows only)
A Python plugin for use in [Krita](https://krita.org).

## What is DDS File Importer?
A Python plugin made specifically for [Krita](https://krita.org) that resorts to [Microsoft's texconv](https://github.com/Microsoft/DirectXTex/wiki/Texconv) to convert image files to/from DDS.

## Functionalities
When executed, this plugin will import the selected DDS file into Krita as either a _TGA_, _PNG_ or _TIF_ file (you choose which one in the window that appears). The original _TGA_/_PNG_/_TIF_ file is erased, so any change performed to the file must be saved either through _File_ > _Save As_, or use the _Tools_ > _Scripts_ > _Export as DDS_ (if you have installed my [DDS File Exporter](https://github.com/esuriddick/Programming/tree/main/Python/Krita/DDS_File_Exporter)).

## Download, Install & Execute
### Download
+ **[ZIP ARCHIVE - v1.1](https://github.com/esuriddick/Programming/raw/main/Python/Krita/DDS_File_Importer/Downloads/DDS_File_Importer_v1.1.zip)**
+ **[ZIP ARCHIVE - v1.0](https://github.com/esuriddick/Programming/raw/main/Python/Krita/DDS_File_Importer/Downloads/DDS_File_Importer_v1.0.zip)**

### Installation
There are two different ways to install Python plugins in [Krita](https://krita.org):
#### First Method
1. Open [Krita](https://krita.org) and go to _Tools_ > _Scripts_ > _Import Python Plugins..._, and select the **DDS_File_Importer.zip** archive.
2. Restart [Krita](https://krita.org).
3. Go to _Settings_ > _Configure Krita..._ > _Python Plugin Manager_, and click the checkbox to the left of the field that says **DDS File Importer**.
4. Restart [Krita](https://krita.org).

#### Second Method
1. Extract the content within the folder **DDS_File_Importer** to the folder **pykrita** (typically located here: C:\Users\USERNAME\AppData\Roaming\krita, where **USERNAME** should be replaced with your Windows username).
2. Restart [Krita](https://krita.org).
3. Go to _Settings_ > _Configure Krita..._ > _Python Plugin Manager_, and click the checkbox to the left of the field that says **DDS File Importer**.
4. Restart [Krita](https://krita.org).

### Execute
Go to the menu item _Tools_ > _Scripts_, and press the option named _Import DDS_. Choose the desired format to convert the DDS file into, and then it will appear in Krita.

### Tested platforms
I have tested version 1.0 and 1.1 of this plugin in version 5.1.5 of [Krita](https://krita.org).

## Change log
_[2023-11-05] Version 1.2_
- Changed one of the arguments in the command line from '-srgbi' to '-srgb' to avoid darkening when importing specific formats of DDS (namely the ones ending with "_SRGB").
- Updated the Texconv file packed with the plugin.

_[2023-09-04] Version 1.1_
- Added a dialog window to pop-up when executing this script to allow you to select the format to convert the DDS file into.

_[2023-09-04] Version 1.0_
- Initial version released.

## License
As identified in this repository, all of the work shared in this repository is under the GNU General Public License v3.0. Be aware that Texconv is shared under [MIT License](https://opensource.org/license/mit/).

_Summary of the GNU General Public License v3.0_: Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

**_I kindly ask Krita developers to consider this plugin as an example of how to incorporate this functionality directly into Krita. I explicitly allow the use of this code in Krita by Krita developers without any of the conditions stated under the GNU General Public License v3.0._**
