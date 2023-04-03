# RemoteDAQ
RemoteDAQ is a device configured to manage and control a Data Acquisition (DAQ) device.

# How to Install
1. Add user to `/etc/sudoers` (replace USER with actual username)
   ```
   USER ALL=(ALL) NOPASSWD:ALL
   ```
2. Change script permission:
    ```
    chmod +x setup.sh
    ```
3. Run command:
    ```
    sudo ./setup.sh
    ```
4. Fill the prompt accordingly.
5. Wait until finished.
