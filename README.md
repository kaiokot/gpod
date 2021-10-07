# gpod - Growth Picture of the Day

A project "inspired" on [growlab](https://github.com/alexellis/growlab) by [@alexellis](https://github.com/alexellis/) and  [NASA apod](https://apod.nasa.gov/) :laughing: :laughing:

gpod is a camera module to monitor the growth of seeds and vegetable gardens in general.

With the objective is to closely monitor the development of the plants and collect environment data and share their evolutions.

Using the Azure Cognitive Services to describe the pictures taken to make things more interesting...

And then create some really cool time lapses :smile:

First POC

Update 1:
-   :camera_flash: Take pic with 1min interval.
-   :computer: Use Azure Cognitive Services to describe image saved.
-   :file_folder: Save local file image + json with descriptions.
-   :cloud: Publish preview image + json to a github page : [gpod preview](https://kaiokot.github.io/gpod-preview)


Update 2:
-   :camera_flash: Add support to ip cams using Rtsp.
-   :camera_flash: 📸 Add multi camera and config support.
-   :cloud:  Add preview from multicamera.

Update 3:
-   🌡️ Add BMP280 Temperature, Pressure, & Altitude Sensor support.

Update 4:
-   🎥 Add TimeLapse feature using ffmpeg.


## References

[fswebcam](http://manpages.ubuntu.com/manpages/bionic/man1/fswebcam.1.html)

[Azure Cognitive Services](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-describing-images)

[Github Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

[ffmpeg](https://ffmpeg.org)

[BMP280 Temperature, Pressure, & Altitude Sensor](https://pypi.org/project/bmp280/)

[GitHub - Managing deploy keys](https://docs.github.com/en/developers/overview/managing-deploy-keys) - Tks to [Marcos Khoriati](https://github.com/khoriati) 😄👍