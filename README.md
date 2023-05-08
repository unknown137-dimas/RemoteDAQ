# RemoteDAQ
RemoteDAQ is a device configured to manage and control a Data Acquisition (DAQ) device.

# How to Install
1. Add user to `/etc/sudoers` (replace USER with actual username)
    ```
    USER ALL=(ALL) NOPASSWD:ALL
    ```
2. Check wireless interface name for setup process with command below, It should start with `wlp` or anything similar, please check your OS documentation.
    ```
    ip link show
    ```
4. Change `setup.sh` script permission:
    ```
    chmod +x setup.sh
    ```
5. Run `setup.sh` command:
    ```
    sudo ./setup.sh
    ```
6. Fill the prompt accordingly.
7. Wait until finished.
