#!/bin/bash

sudo apt-get update

#T2S and S2T
yes | sudo pip3 install gTTS
yes | sudo pip3 install playsound
yes | sudo pip3 install PyAudio
yes | sudo pip3 install SpeechRecognition
yes | sudo apt install flac

#BLE
sudo pip3 install bluepy
#bluez

#microphone
yes | sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo pip3 install pyaudio

#make mono
sudo echo load-module module-remap-sink sink_name=mono master=alsa_output.platform-bcm2835_audio.analog-stereo channels=2 channel_map=mono,mono > /etc/pulse/default.pa
sudo echo load-module module-remap-sink sink_name=mono master=alsa_output.platform-bcm2835_audio.digital-stereo channels=2 channel_map=mono,mono > /etc/pulse/default.pa
sudo pacmd load-module module-remap-sink sink_name=mono master=$(pacmd list-sinks | grep -m 1 -oP 'name:\s<\K.*(?=>)') channels=2 channel_map=mono,mono