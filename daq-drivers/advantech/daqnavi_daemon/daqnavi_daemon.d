#!/bin/bash
### BEGIN INIT INFO
# Provides:          advantech
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: daqnavi_daemon
# Description:       DAQNavi4 Device Monitor Daemon
### END INIT INFO

BIN=/opt/advantech/daqnavi_daemon/daqnavi_daemon
USER=root
GROUP=root
PID_DIR=/var/run
PID_FILE=$PID_DIR/daqnavi_daemon.pid

RET_VAL=0

check_running() {
  if [[ -r $PID_FILE ]]; then
    read PID <$PID_FILE
    if [[ -d "/proc/$PID" ]]; then
      return 0
    else
      rm -f $PID_FILE
      return 1
    fi
  else
    return 2
  fi
}

do_status() {
  check_running
  case $? in
    0)
      echo "daqnavi_daemon running with PID $PID"
      ;;
    1)
      echo "daqnavi_daemon not running, remove PID file $PID_FILE"
      ;;
    2)
      echo "Could not find PID file $PID_FILE, daqnavi_daemon does not appear to be running"
      ;;
  esac
  return 0
}

do_start() {
  if [[ ! -d $PID_DIR ]]; then
    echo "creating PID dir"
    mkdir $PID_DIR || echo "failed creating PID directory $PID_DIR"; exit 1
    chown $USER:$GROUP $PID_DIR || echo "failed creating PID directory $PID_DIR"; exit 1
    chmod 0770 $PID_DIR
  fi
  if check_running; then
    echo "daqnavi_daemon already running with PID $PID"
    return 0
  fi
  echo "starting daqnavi_daemon"
  # sudo will set the group to the primary group of $USER
  $BIN > /dev/null 2>&1 &
  PID=$!
  echo $PID > $PID_FILE
  sleep 0.3
  if ! check_running; then
    echo "start failed"
    return 1
  fi
  echo "daqnavi_daemon running with PID $PID"
  return 0
}

do_stop() {
  if check_running; then
    echo "stopping daqnavi_daemon with PID $PID"
    kill $PID
    rm -f $PID_FILE
  else
    echo "Could not find PID file $PID_FILE"
  fi
}

do_restart() {
  do_stop
  do_start
}

case "$1" in
  start|stop|restart|status)
    do_$1
    ;;
  *)
    echo "Usage: daqnavi_daemon {start|stop|restart|status}"
    RET_VAL=1
    ;;
esac

exit $RET_VAL
