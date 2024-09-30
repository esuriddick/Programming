# Texture Packing
A Python script that allows to pack different channels of different images into specific channels of a single image.

## What is Texture Packing?
Texture Packing refers to the bundling of specific channels of textures (Red, Green, Blue, Alpha) into other channels. This is a technique commonly used in videogame development to reduce the number of textures loaded and, thus, improve performance.

## Functionalities
When executed, a window will pop up with the following options:
- Select the image file to be used for the target channel. Main image formats are supported, but you can try to select a different format by selecting "All files" in the drop-down menu when selecting an image file to try any other image format.
- Source channel to extract from the image selected.
- In case no image is selected for a specific target channel, the user can select whether the target channel should be filled with a black (default) or white image.

Once the image file(s) that you want to extract a specific channel from have been selected, you may press the "Submit" button.

When the process is finished, a new window will appear that allows you to either preview the image or save it. You may close this window once you are done.

## Change Log
_[2024-10-01] Version 1.0_
- Initial version released.

## License
As identified in this repository, all of the work shared in this repository is under the GNU General Public License v3.0.

_Summary of the GNU General Public License v3.0_: Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.
