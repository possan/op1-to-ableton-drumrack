# OP-1 Drum kit sample to Ableton Drum Rack converter

This is a small hack that converts the AIFF files for OP-1 into Ableton Drum Racks.


## Prerequisites

Install a couple of python dependencies `pip3 install -r requirements.txt`



## How to use

Download a drum kit .aiff file from the website, call it `drumkit.aif`

Run the conversion script to convert it into a `drumkit.adg`

```
python3 convert.py drumkit.aif
```

Put the `drumkit.aif` file into your `~/Music/Ableton/User Library/Samples/Imported` folder

Put the drum rack file `drumkit.adg` somewhere in your `~/Music/Ableton/User Library/Presets/Instruments/Drum Rack` folder




## Want lots of drum kits?

[OP1.fun](https://op1.fun) is a nice site with a lot of great drum kits

There's a couple of hacky scripts included, that will scrape the site and download all drum kits, using the op1.fun api.

<blockquote>
Please, as always, if you use any of the samples make sure to appropriately attribute the author.
</blockquote>

Get your API KEY from your [op1.fun profile page](https://op1.fun/profile) and put that and your email into [downloaduserpatches.py]
(downloaduserpatches.py)

Make a temporary folder

```
mkdir temp
```

Scrape the search page to get all usernames that has a drum kit _(there's no api for that :/)_

```
python3 scrapeallusers.py
```

Download all drum kit patches and audio files from each user

```
python3 downloaduserpatches.py
```

Convert them

```
python3 convert.py "temp/*aif"
```

Make an OP1.FUN Folder in Ableton

```
mkdir "~/Music/Ableton/User Library/Presets/Instruments/Drum Rack/OP1.FUN"
```

Copy the files into Ableton

```
cp temp/*adg ~/Music/Ableton/User\ Library/Presets/Instruments/Drum\ Rack/OP1.FUN
cp temp/*aif ~/Music/Ableton/User\ Library/Samples/Imported
```
