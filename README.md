# NomNom # 

University of Southampton - Cloud Application Development - Coursework 2

## Members ##
 * Hannah Dadd
 * Imran Bepari
 * Jamie Scott
 * Michael Paulsen-Forster
 * Steffan Padel
 * Toby Fielding

## Development Setup Instructions ##
1. Install GAE SDK, Python 2 and Pip.
2. Open `Makefile` and set `gcloud-sdk` to the path to where your SDK is installed.
3. Run `make depends` to download the project dependencies.
4. Run `make run` to run the application locally.

## GAE Setup Instructions ##

### Linux (and macOS) ###
1. Download the latest GAE 64-bit version from https://cloud.google.com/sdk/docs/
2. Move the archive to `/opt`
```
$ sudo mv path/to/archive.tar.gz /opt
```
3. Decompress and delete the archive
```
$ cd /opt
$ sudo tar -zxvf archive.tar.gz
$ sudo rm archive.tar.gz
$ sudo chown -R <user>:<group> /opt/google-cloud-sdk
```
4. Add required binaries to your system path
```
$ sudo ln -s /opt/google-cloud-sdk/bin/gcloud /usr/local/bin
$ sudo ln -s /opt/google-cloud-sdk/bin/gsutil /usr/local/bin
```
5. Initialize the SDK
```
$ gcloud init
```
