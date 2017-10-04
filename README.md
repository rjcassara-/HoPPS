# HoPPS
Host Process Polling System

This project is meant to act as a basic monitoring tool for a home network. The client.py runs on computers within the network, reporting to a server that runs server.py.

The hopps.conf configuration file is set on each client to define where the server is, what port it is listening on, and how often the client script should execute (defaults to every 5 minutes)
