# autoTaskiller
is used to detect commands which are using CPU for too much long

# Requirements
It's simple, just Python 3

# Usage 
autoTaskiller needs to bude run in a interval in which you want to check the usage \
For example: \
  I want to kill every command which runs more than 30 mins. and usess more than 90% of CPU \
   You set up cron to run autoTaskiller every 30 mins. and its done\
\
Cron code:\
``
*/30 * * * * python3 /path/to/code/taskKiller
``
 
