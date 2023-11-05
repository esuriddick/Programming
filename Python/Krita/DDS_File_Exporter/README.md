# DDS File Exporter (Windows only)
A Python plugin for use in [Krita](https://krita.org).

## What is DDS File Exporter?
A Python plugin made specifically for [Krita](https://krita.org) that resorts to [Microsoft's texconv](https://github.com/Microsoft/DirectXTex/wiki/Texconv) to convert image files to/from DDS.

## Functionalities
When executed, this plugin will export the current selected open document into either a _TGA_, _PNG_ or _TIF_ image file in a temporary folder. Afterwards, this image file is converted to DDS and stored in the selected location. Finally, the temporary _TGA_/_PNG_/_TIF_ image file is erased.

## Download, Install & Execute
### Download
+ **[ZIP ARCHIVE - v1.1](https://github.com/esuriddick/Programming/raw/main/Python/Krita/DDS_File_Exporter/Downloads/DDS_File_Exporter_v1.1.zip)**
+ **[ZIP ARCHIVE - v1.0](https://github.com/esuriddick/Programming/raw/main/Python/Krita/DDS_File_Exporter/Downloads/DDS_File_Exporter_v1.0.zip)**

### Installation
There are two different ways to install Python plugins in [Krita](https://krita.org):
#### First Method
1. Open [Krita](https://krita.org) and go to _Tools_ > _Scripts_ > _Import Python Plugins..._, and select the **DDS_File_Exporter.zip** archive.
2. Restart [Krita](https://krita.org).
3. Go to _Settings_ > _Configure Krita..._ > _Python Plugin Manager_, and click the checkbox to the left of the field that says **DDS File Exporter**.
4. Restart [Krita](https://krita.org).

#### Second Method
1. Extract the content within the folder **DDS_File_Exporter** to the folder **pykrita** (typically located here: C:\Users\USERNAME\AppData\Roaming\krita, where **USERNAME** should be replaced with your Windows username).
2. Restart [Krita](https://krita.org).
3. Go to _Settings_ > _Configure Krita..._ > _Python Plugin Manager_, and click the checkbox to the left of the field that says **DDS File Exporter**.
4. Restart [Krita](https://krita.org).

### Execute
Once you have a document selected in [Krita](https://krita.org), go to the menu item _Tools_ > _Scripts_, and press the option named _Export as DDS_. A window will pop-up to ask you the name and location of where to save the file.

### Tested platforms
I have tested version 1.0 and 1.1 of this plugin in version 5.1.5 of [Krita](https://krita.org).

## Change log
_[2023-11-05] Version 1.2_
- Made it clear in the dialog menu that 'BC7_UNORM' is DXT10.
- Added an option whether to allow separate alpha channels or use a single one.

_[2023-09-06] Version 1.1_
- Cleaned up the code further (removed modules that were not in use, and leftovers in the error message boxes).
- You no longer require to have or modify a _settings.ini_ file. The execution of the script will provide a window with options for: 1) intermediate file format to convert to DDS (default is TGA); 2) compression type (default is BC7 UNORM, also known as DXT10); 3) whether to generate MIP maps or not (default is to generate); and 4) whether to force DX9/DX10 headers or not (default is not to force either of these headers).

_[2023-09-04] Version 1.0_
- Initial version released.

## License
As identified in this repository, all of the work shared in this repository is under the GNU General Public License v3.0. Be aware that Texconv is shared under [MIT License](https://opensource.org/license/mit/).

_Summary of the GNU General Public License v3.0_: Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

**_I kindly ask Krita developers to consider this plugin as an example of how to incorporate this functionality directly into Krita. I explicitly allow the use of this code in Krita by Krita developers without any of the conditions stated under the GNU General Public License v3.0._**
