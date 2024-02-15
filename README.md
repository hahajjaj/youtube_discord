# Music Bot for Discord

This project is a Discord bot developed to play music within voice channels. Using Discord.py and yt-dlp for audio extraction, the bot allows users to play music directly from YouTube links. With Firebase for environment configuration and command handling through discord.ext.commands, this bot provides a versatile solution for enhancing Discord server engagement.

## Features

* Music Playback: Plays music from YouTube URLs in a Discord voice channel.
* Queue System: Manages a queue of songs, playing them sequentially.
* Playback Control: Offers playback control through reactions for play/pause, skip, and loop functionality.
* Flexible Command Prefix: Utilizes "!" as the command prefix for easy access to bot commands.
* Join & Leave: Can join the user's voice channel or leave the current channel on command.
* Looping: Ability to loop the current song or the entire queue.
* Dynamic Help Command: Provides an embed with detailed command usage instructions.

## Commands

* !join: Joins the user's current voice channel.
* !leave: Leaves the current voice channel.
* !p <URL>: Plays the specified song from a YouTube URL. Adds to the queue if something is already playing.
* !skip: Skips the currently playing song.
* !stop: Stops the music playback and clears the queue.
* !loop: Toggles loop mode for the current song.
* !ping: Checks the bot's latency.
* !h: Displays help information with details on how to use the bot's commands.

## Reaction Controls

Users can control music playback by reacting to the bot's control message with:

* "⏯" for play/pause,
* "⏭" for skip,
* "🔁" for toggling loop mode.

## Setup
This bot requires an environment setup with Discord API keys and appropriate libraries installed. The .env file should contain your Discord bot token as API_KEY_DISCORD2.

## Note
The script has been updated to use "!" as the command prefix, simplifying interaction by removing the need to mention the bot's name. This change aims to enhance user experience by making commands more accessible and straightforward.

Remember, to keep your Discord token secure and never share it publicly. Enjoy adding a musical touch to your Discord servers with this versatile bot!
