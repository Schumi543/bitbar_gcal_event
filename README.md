# Bitbar Gcal event

A BitBar plugin that show your upcoming meeting from Google Calendar.
And launch your video meeting with 1 click.

![screenshot](https://github.com/Schumi543/bitbar_gcal_event/master/doc/screenshot.gif?raw=true)

## Installation
### 1. setup bitbar
1. Download [BitBar](https://github.com/matryer/bitbar)
2. Move the BitBar application to your Applications folder
3. Open BitBar and BitBar will prompt you to set a plugins folder - you may set it to any folder you like
4. Click on BitBar in your MacOS menu bar and click Open Plugin Folder...

### 2. setup bitbar_gcal_event
1. `git clone https://github.com/Schumi543/bitbar_gcal_event`
2. Enable Google Calendar API and download `credentials.json`. (see. https://developers.google.com/calendar/quickstart/python#step_1_turn_on_the)
3. Place `credentials.json` on `/path/to/bitbar_gcal_event`.
4. `cp .env.sample .env` and set your `CALENDAR_ID` to .env.
5. write bitbar script(like `bitbar.1h.sh`) in your bitbar plugins folder.
