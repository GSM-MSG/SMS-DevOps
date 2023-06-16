#!/bin/bash

kill $(ps aux | grep '[p]ython3 android_bot.py' | awk '{print $2}')
