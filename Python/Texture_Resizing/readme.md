# Texture Resizing
A Python script that allows to downscale / reduce the resolution of a texture file. It should be noted that this tool applies the same texture resolution to both the width and height of the image, meaning that it is best used for image files where the width and height are equal to each other (e.g., 1024x1024, 2048x2048, etc.).

## Functionalities
When executed, a window will pop up with the following options:
- Select the image file to downscale. Main image formats are supported, but you can try to select a different format by selecting "All files" in the drop-down menu when selecting an image file to try any other image format.
- The target resolution of the image. It should be noted that this tool only downscales images, meaning that, even if you insert a higher resolution than the one of the original image, it will not lead to an increase of the image.
- The resampling method to be used during the downscaling process. There are four options available:
    - Bilinear (default): incorporates values from the four closest pixels. This method strikes a balance between speed and visual quality, making it a popular choice in many applications.
    - Nearest: uses the nearest pixel's value. While it's the fastest of the four available resampling methods, it might not always offer the best visual output.
    - Bicubic: employs bicubic interpolation over a 4x4 pixel grid. While it is slower than 'Bilinear', it's favored for its smoother enlargements.
    - Lanczo: leverages Lanczos interpolation across an 8x8 pixel neighborhood.
    Overall, Lanczos and Bicubic are often considered the best quality options, with Lanczos slightly edging out Bicubic in terms of sharpness and detail preservation

Once you are ready, you may press the "Submit" button.

When the process is finished, a new window will appear that allows you to either preview the image or save it. You may close this window once you are done.

## Change Log
_[2024-12-18] Version 1.0_
- Initial version released.

## License
As identified in this repository, all of the work shared in this repository is under the GNU General Public License v3.0.

_Summary of the GNU General Public License v3.0_: Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.
