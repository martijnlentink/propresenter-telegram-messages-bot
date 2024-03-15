#!/bin/sh
while true
do
	pgrep -f 'messagesbot.py' | xargs kill -9
	/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 '/Scripting/messagesbot.py'
done