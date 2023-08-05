PKRADIO
=======

An easy to use Pakstani radio player.


Details
-------

There is a built-in list of popular radio stations in different languages and more will be added.


Package Usage
-------------

from pkradio import pkradio as pkr

\# Get version

pkr.get_version()

\# Load list of stations

_st = pkr.load_stations()

\# Get the support player

_pl = pkr.get_player()

\# Stream a station

pkd.play_radio_url(_pl, _st['vos'])
