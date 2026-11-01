# ARC-210 working tester

**Last updated: November 1, 2026 at 12:23 AM MDT (America/Denver)**

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
and **Set Master** controls. Click **Power On / Send All** to send RT status, MAN mode, MASTER = TR, and the selected frequency together. Then use the individual controls, or choose **0 - OFF** and click **Set Master** to test radio power off.

For the normal instrument controls, load your installed DCS-BIOS aircraft JSON.
The ARC-210 shortcuts use fixed A-10C II addresses in the script; loading another
JSON does not remap them. They simulate radio data sent to the hardware and do
not operate a running DCS radio. Firmware may also require other power/status
exports supplied through the normal instrument controls. Avoid automatic updates
for the same fields while using the shortcut buttons.

This is the working development version, not a packaged release. The old bundled
Windows executable does not contain these ARC-210 additions; run the Python file.
Personal settings, test logs, and local backups are not included.

## Version 1.5.3 and verified bench behavior

I confirmed that the bridge delivered MASTER = TR, radio/display power on, and frequency 133.123 to my physical panel running v0.1.3 Diagnostic. The display worked. This does not verify every menu or live DCS operation.

- **Power On / Send All** sends the basic powered-radio state; selecting a COM port or loading JSON alone does not power the simulated radio.
- String packets are word-aligned and preserve adjacent selector bits, including the shared word at 0x1322 beside `ARC210_SELECTED_RT`.
- A USB disconnect stops the connection without stopping the receive loop. Reconnect after flashing.
- The receiver displays readable USB diagnostics when supported by the loaded firmware.

Click **Find Serial Ports**, then select the detected port in the adjacent dropdown and click **Connect**. The dropdown may still show “–” until you choose a port. Close other apps using that port.

Use **Choose DCSBios JSON file** to load `DCS-BIOS/doc/json/A-10C.json` from your DCS-BIOS release. Our bench test used v0.11.8. The categories populate only after loading this file; the JSON is not bundled. You can also pass its path when launching:

```cmd
python dcsBiosDebug.py "C:\path\to\A-10C.json"
```

The app has no computer-specific JSON path. Its saved settings still work. It sends simulated exports to the Teensy; it does not simulate all DCS radio logic or provide full physical-control integration.

Run `python test_string_packets.py` to check word alignment and preservation of neighboring bytes in string packets without opening the GUI or a COM port.
