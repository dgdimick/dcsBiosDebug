# ARC-210 working tester

This branch preserves the working ARC-210 testing app used with the
[ARC-210 DCS Display project](https://github.com/dgdimick/ARC-210-DCS-Display).
It is separate from the optional-panel contribution proposed to the original
[dcsBiosDebug project by tldBear](https://github.com/tldBear/dcsBiosDebug).

## Download and run

1. Download this branch using **Code → Download ZIP** and extract it. Keep the
   `icons` folder beside `dcsBiosDebug.py`.
2. Install Python 3 with Tkinter support, then install the dependencies:

   ```cmd
   python -m pip install numpy pyserial Pillow
   ```

3. Open a terminal in the extracted folder and run:

   ```cmd
   python dcsBiosDebug.py
   ```

   Include `.py`: the extensionless `dcsBiosDebug` file is a Linux shell launcher.

4. Select your Teensy's serial port and click **Connect**. Close any other app
   using that port first.

The ARC-210 controls appear at the top automatically. They include MENU,
XMT/RCV, the three left soft keys, and separate **Set Freq**, **Set Secondary**,
and **Set Master** controls. Choose **2 - TR** and click **Set Master** for the
normal operating switch position, or **0 - OFF** to test radio power off.

For the normal instrument controls, load your installed DCS-BIOS aircraft JSON.
The ARC-210 shortcuts use fixed A-10C II addresses in the script; loading another
JSON does not remap them. They simulate radio data sent to the hardware and do
not operate a running DCS radio. Firmware may also require other power/status
exports supplied through the normal instrument controls. Avoid automatic updates
for the same fields while using the shortcut buttons.

This is the working development version, not a packaged release. The old bundled
Windows executable does not contain these ARC-210 additions; run the Python file.
Personal settings, test logs, and local backups are not included.
