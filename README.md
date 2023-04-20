# Discord Bot : BathBot

My first Discord bot: Has similar functionality to my Twitch bot (a lot was repurposed)

Has the following features:

### Basic Commands
!8ball - posting a question as the second arg sends back one of 20 random responses

!flipacoin - flips a coin and returns heads or tails randomly

!commands - sends a list of hardcoded commands

!ping - sends the ping in milliseconds

!hello - debug test

### Reaction Roles

A little clunky but has the ability to add a role to a user based on a reaction they post in a specific room in the Discord.

Will remove the role when the reaction is removed.

Used to assign pronoun-based roles to users at their convenience.


### Webserver

Utilizes a webserver for 24 / 7 uptime, but doesn't work as well as it does on Twitch. Will eventually restart given a few hours of downtime.
