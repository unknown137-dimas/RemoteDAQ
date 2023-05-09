# RemoteDAQ
RemoteDAQ is a device configured to manage and control a Data Acquisition (DAQ) device.

# How to Install
1. Add user to `/etc/sudoers` (replace USER with actual username)
    ```
    USER ALL=(ALL) NOPASSWD:ALL
    ```
2. [OPTIONAL] Check wireless interface name for setup process with command below, It should start with `wlp` or anything similar, please check your OS documentation.
    ```
    ip link show
    ```
3. Change `setup.sh` script permission:
    ```
    chmod +x setup.sh
    ```
4. Run `setup.sh` command:
    ```
    sudo ./setup.sh
    ```
    If you want to configure it with wireless instead of wired, run this command instead after checking your wireless interface name using the command in step 2 above:
    ```
    sudo ./setup.sh -w
    ```
5. Fill the prompt accordingly.
6. Wait until finished.
