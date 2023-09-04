# DDS File Exporter
A Python plugin for use in [Krita](https://krita.org).

## What is DDS File Exporter?
A Python plugin made specifically for [Krita](https://krita.org) that resorts to [Microsoft's texconv](https://github.com/Microsoft/DirectXTex/wiki/Texconv) to convert image files to/from DDS.

## Functionalities
When executed, this plugin will export the current selected open document into a _PNG_ image file in a temporary folder. Afterwards, this image file is converted to DDS and stored in the selected location. Finally, the _PNG_ image file is erased.

Inside the plugin folder, there is a file called **settings.ini** that contains the conversion settings used when the script is executed. You may use notepad to modify the file and configure the compression used or whether mip maps are generated, which should be the two most relevant settings. Nevertheless, there are also other options available such as force compatibility with DX9 or DX10.

## Download, Install & Execute
### Download
+ **[ZIP ARCHIVE - v1.0.0]()**

### Installation
There are two different ways to install Python plugins in [Krita](https://krita.org):
#### First Method
1. Open [Krita](https://krita.org) and go to **Tools** > **Scripts** > **Import Python Plugins...**, and select the **DDS_File_Exporter.zip** archive.
2. Restart [Krita](https://krita.org).
3. Go to **Settings** > **Configure Krita...** > **Python Plugin Manager**, and click the checkbox to the left of the field that says **DDS File Exporter**.
4. Restart [Krita](https://krita.org).

#### Second Method
1. Extract the content within the folder **DDS_File_Exporter** to the folder **pykrita** (typically located here: C:\Users\<USERNAME>\AppData\Roaming\krita).
2. Restart [Krita](https://krita.org).
3. Go to **Settings** > **Configure Krita...** > **Python Plugin Manager**, and click the checkbox to the left of the field that says **DDS File Exporter**.
4. Restart [Krita](https://krita.org).

### Execute
Once you have a document selected in [Krita](https://krita.org), go to the menu item _Tools_ > _Scripts_, and press the option named _Export as DDS_. A window will pop-up to ask you the name and location of where to save the file.

### Tested platforms
I have tested version 1.0 of this plugin in version 5.1.5 of [Krita](https://krita.org).

## Change log
_[2023-09-04] Version 1.0_
- Initial version released.

## License
As identified in this repository, all of the work shared in this repository is under the GNU General Public License v3.0. Be aware that Texconv is shared under [MIT License](https://opensource.org/license/mit/).

_Summary of the license_: Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

**_I kindly ask Krita developers to consider this plugin as an example of how to incorporate this functionality directly into Krita. I explicitly allow the use of this code in Krita without any of the conditions stated under the GNU General Public License v3.0._**
