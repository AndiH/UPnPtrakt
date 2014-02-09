# UPnPtrakt

Monitors an UPnP device, logs changes into a database and checks in new episodes to [trakt.tv](http://trakt.tv).

UPnP devices are mounted into the file system (by means of [`djmount`](https://github.com/Boxee/djmount)), the content of the »Last Viewed« folder is checked against entries of a database. If new episodes are detected, they are added to the database and checked in to trakt.tv.

Made for OS X and Linux.
## TL;DR
Install needed stuff (see **Prerequisites**), fill in your trakt.tv credentials in `trakt-config.json`, watch something new and run

```shell
./upnptrakt.py
```

## Features
UPnPtrakt tracks your last viewed shows as indicated by your UPnP/DLNA devices. It parses the show, retrieves proper (meta) data from trakt.tv and fills up a database. New shows are checked in to trakt.tv.

`upnptrakt.py` has quite a few features accessable while calling, just check `./upnptrakt.py --help`.
## Prerequisites
There's some stuff which has to be on your system in order for UPnPtrakt to work.
### Program: djmount
As I was unable to find a Python package for monitoring UPnP devices, UPnPtrakt relies on [djmount](https://github.com/Boxee/djmount) to interface between the current host and all UPnP/DLNA devices in your network.

`djmount` is both available in Homebrew and Ubuntu's packages repository. To install, either run (OS X)

```shell
brew install djmount
````
or (Ubuntu)

```shell
sudo apt-get install djmount
```
If your Linux flavor is not Ubuntu, there's probably a package for djmount around for your distro as well. If you're running Windows, I don't know (neither about `djmount` nor about this stuff here running at all.)

### Python Packages
This Python program uses quite a few packages. All of them can be installed via [pip](http://www.pip-installer.org/):

```shell
pip install guessit psutil simplejson  
pip install git+https://github.com/z4r/python-trakt
```

## Setup
Use `createLocalDb.py` to create the necessary SQLite3 database. Use `--dropDB` to drop the databasse before recreating it.

Rename `trakt-config.example.json` to your likings, e.g. `trakt-config.json`, and insert your trakt.tv credentials . The `apikey` is really not needed any more. (Only, if you don't want to post to trakt.tv but merely get some show episode information and don't want to rely on UPnPtrakt's dev API key. But why would you?)

Manually test mounting UPnP devices by calling
```shell
mkdir test
djmount test
ll test
umount test; rm -rf test```
If you get an error you might need to load the FUSE kernel module first: `modprobe fuse`)
## Usage
Calling `upnptrakt.py -h` should be pretty much self-explanatory. The default values are tuned for my personal case, you might need to customize them in the call to the script. Especially the `--path-to-last-viewed` is probably different for your UPnP/DLNA server (or not, if you're running Serviio on a host named Andisk2…).

Let's get through the parameters, sorted by importance (and then through the flags):

* **--path-to-last-viewed *PATH***: The path to the *last viewed* folder of your UPnP/DLNA server. You probably need to find this out by running a manual `djmount` (see **Setup**). Don't care too much about trailing / ending slashes. This should be taken care of automatically.  
*Default*: `Serviio (Andisk2)/Video/Last Viewed`. 
* **--trakt-config-json *FILE***: Filename of the json config used to login to trakt.tv. See **Setup**.  
*Default*: `trakt-config.json`
* **--series-whitelist-json *FILE***: Sometimes the trakt.tv search is unable to finde the current show. Put it into this whitelist then.  
*Default*: `seriesWhitelist.json`
* **--database-file *FILE***: SQLite3 database filename to store all episode information in.  
*Default*: `episodes.db`
* **--mount-path *PATH***: Location, where `djmount` will mount the UPnP network surroundings in.  
*Default*: `.upnpDevices` (yes, it's hidden)

Flags provided (all off by default):

* **--dont-store**: Don't store information about new shows into the database. Becomes a *dry run* when used in combination with --dont-post.
* **--dont-post**: Don't post new episodes to trakt.tv. Only use the database. You might want to use this to initially fill up the database. Becomes a *dry run* when used together with --dont-store.
* **--restart-djmount**: In case of troubles with `djmount`, this flag gets rid of all `djmount` process, unmounts the mount path (as provided by `--mount-path`) and deletes the folder. *Attention:* ALL `djmount` processes are killed! If you have some other folders in your system mounted with the tool, you might get some funny behavior there.

After setting up all needed tools, creating and initial-filling your databse, you probably want to create a cronjob calling `upnptrakt.py` every 20 minutes or so.

## Limits & Todos
* At the moment the load to trakt.tv is quite high, as every episode's proper data is retrieved from there. Resulting in a slow script. This is going to be changed soon. Hopefully.
* No error handling whatsoever is included. No logging either.
* Take a look to [issues](https://github.com/AndiH/UPnPtrakt/issues) for what I plan to do next. Also, report them over there (or, much better, send me a pull request).