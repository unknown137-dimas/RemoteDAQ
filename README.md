# RemoteDAQ
RemoteDAQ is a device configured to manage and control a Data Acquisition (DAQ) device.

# How to Install
1. Add user to `/etc/sudoers` (replace USER with actual username) using root account.
    ```
    USER ALL=(ALL) NOPASSWD:ALL
    ```
2. [OPTIONAL] Check wireless interface name for setup process with command below, It should start with `wlp` or anything similar, please check your OS documentation.
    ```
    ip link show
    ```
3. Clone this repository.
    ```
    git clone https://github.com/unknown137-dimas/RemoteDAQ.git
    ```
4. `cd` to inside the repository.
5. Change `setup.sh` script permission:
    ```
    chmod +x setup.sh
    ```
6. Run `setup.sh` command:
    ```
    sudo ./setup.sh
    ```
    If you want to configure it with wireless instead of wired, run this command instead after checking your wireless interface name using the command in step 2 above:
    ```
    sudo ./setup.sh -w
    ```
7. Fill the prompt accordingly.
8. Wait until finished.
9. Continue the installation from the dashboard by installing the server-side system [here](https://github.com/unknown137-dimas/RemoteDAQ-Server).
