# Wedding Controller

<a id="readme-top"></a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This was a project that I made for my wedding.  It linked multiple systems together, and provided a seamless performance on the night.

Here's the general outline of what I made - this is one part of that system:

The wedding website was a django site, with accounts for everyone I invited. I had a separate part of it where the guests could choose an RGB colour, and then choose tracks by searching. I used a spotify API for this, so when they chose a track, if someone chose a similar one (say a specific mix) then they could see this and vote for that. Each guest could choose 10 tracks. I used some HTMX for this as well (first time) and it generally worked pretty well. Database stored the spotify ID/UUID/whatever for each track

Once everyone had voted, I then bought all the tracks which we were going to play - reason being that I couldn't rely on WiFi on the day, and wanted to be 100% sure it would work, plus I couldn't "DJ" from spotify tracks.

All of the tracks were then renamed including their spotify ID/UUID/whatever, so the system knew who had voted for a specific track.

I then made the playlist up in Mixxx, and trimmed tracks to fit better, and made it work musically (my wife is excellent at this, she made it really work, mix wise). Made sure it all played OK.

The other part of the system was a custom light setup, with sound-reactive LED bars I made up (using ESP8266 and WLED firmware with 150 LEDs per 'stick') with them all being controlled by a custom controller. This system read the track from the Mixxx system (via HTTP request to a flask app I wrote that read the sqlite dB from mixxx to know what track was playing), and then coloured the lights with the colours of the people who had voted for the tracks. Also if you went onto the dancefloor you could 'swipe in' via an RFID label which was in the wristbands, which also reacted to lights and were colour-controlled over DMX.

The light patterns were sometimes random, or if one was good for a specific track then I programmed that into the system.

It was all spaghetti code, and the first time I used FastAPI. The code is probably terrible, and I'm only making it public as I thought it might be useful to someone.

There are a few constants defined for API endpoints.  In my particular setup I used a dedicated router and static IPs for all the devices - the LED lights, the controller (LedFX) and so on.  All of it worked well because of this, but you would probably need to change the setup to suit.  

I recently revived this to allow me to use the lights at home - for reasons - and it just needed some tweaks to do this.  One of the changes I made was to add a simple python script that calls the random changes in colours and light patterns every 180 seconds - this is because I'm just using sonos playback at home and don't have it set up to query this to see when a track has changed.  This script is included as `timed_calls.py` - it's pretty simple but saves having to do this yourself if you just want the patterns to change every now and then without more complexity.

To get this up and running all on the same system, just change the IP addresses of the endpoints to `127.0.0.1` and you should be good to go - LedFX happily co-exists with this on my M1 macbook.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [LedFX](https://github.com/LedFx/LedFx)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Requests](https://pypi.org/project/requests/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Mixxx](https://mixxx.org/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Running install of LedFX, with lights setup as a virtual, and running in audio-reactive mode.  

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Create a Python 3.10 virtual environment (later versions may work, but this was built with Python 3.10)
   ```sh
   python3.10 -m venv venv
   source venv/bin/activate # linux/macOS
   venv/Scripts/activate.bat # windows
   ```
2. Clone the repo
   ```sh
   git clone https://github.com/djaychela/wedding_controller.git
   ```
3. Install python dependencies
   ```sh
   python -m pip install -r requirements.txt
   ```
4. Change the API endpoints appropriately in `controller/helpers/api_helpers.py` and `controller/api_calls.py` - for instance for a setup with LedFX running on the same machine as the wedding controller:
   ```python
   API_ENDPOINT = "http://127.0.0.1:8888/api/virtuals/virtual-1/effects";
   ```
5. Run the Wedding Controller.  You can do this with Uvicorn or similar, but for testing the FastAPI server will do:

   ```sh
   fastapi dev controller/main.py 
   ```
6. Endpoints defined are now accessible, such as

    ```
    http://127.0.0.1:8000/state/change_effect
    ```
    Which will change the effect currently running in LedFX

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To set this up locally, change all API endpoints to point at `127.0.0.1`, and set up a virtual in LedFX, called virtual-1.  

You will need to disable the calls to the other virtual and also to the 'bands' - these were radio-controlled wristbands whose colour could be set via an API call to an ESP8266 which converted the call to DMX to control the bands.  This is done by commenting out the API calls in `api_calls.py` - such as in `def new_random_effect():`:

```python
    def new_random_effect(db, song_id=None):

        ...

    api_request_2 = api_helpers.create_api_request_string(db, random_effect.type, colourscheme, random_effect.id, sticks_2=True)
    # api_helpers.perform_api_call(db, api_request_2, "sticks_2")

    # bands_current_song(db, "instant")

```

Doing this here and in `def new_random_colour()` enabled the system with a single virtual to run, as I now have it set up at home.  If you have the full system setup (and it is communicating with Mixxx or similar) then the other api calls will need to be modified, but the functions are sensibly named so it's easy to isolate which calls need to be commented out or removed.  I never got round to doing config flags for the presence of these, so consider that a project you can do if you need to!

System can be [seen running here](https://photos.app.goo.gl/MPWkFfHzNgioq3M98)

There's a fair bit of output to the console as the system runs.  This was for bug-hunting initially but I left it in place as the system needed to work out-of-the-box on my wedding day and having the reassurance of seeing this output on the morning was very relaxing!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

This is a legacy project that I've posted and made public because I was asked about it in an HN thread, and because I'm terminally ill and thought it might be useful to someone someday.

As a result, contributions are not open!  Feel free to fork the project and work on it, improve it or just use it.  But there isn't an active project as such because of my health.

### Top contributors:

<a href="https://github.com/djaychela/wedding_controller/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=djaychela/wedding_controller" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The project worked because of these two great projects - LedFX as a controller and WLED which runs the lights that LedFX controls.

* [LedFX](https://github.com/ledfx/ledfx)
* [Wled](https://kno.wled.ge/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

