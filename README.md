# GTA 6 on PS5 with keyboard and mouse (Remote Play via Veyra + reWASD)

**English** · [Русский](README.ru.md)

Play GTA 6 on a PS5 from your PC with a keyboard and mouse. The PS5 streams to the PC through **Veyra** (PS5 Remote Play with picture enhancement). **reWASD** turns the keyboard and mouse into a virtual DualShock 4, and Veyra sends that gamepad to the PS5.

The game itself does not support keyboard and mouse on PS5, so to the console this looks like an ordinary gamepad. Mouse aiming is emulated through the right stick: it works well, but it is not the same as native PC mouse aim.

## What is in this folder

| File | What it is |
|---|---|
| `configs/GTA6 KB+M (slot 1).rewasd` | Game config: keyboard and mouse → DualShock 4. On foot, vehicle (V) and aircraft (G) modes. |
| `configs/GTA6 PC mode (slot 2).rewasd` | PC mode: keyboard and mouse work normally, the gamepad stays connected but idle. |
| `cheatsheet/controls-ru.html` | Controls cheat sheet (Russian). Open it in any browser. |
| `tools/find-input-device.py` | Diagnostic script: shows which USB device your mouse or keyboard input actually comes from. |

## What you need

- PS5 with Remote Play enabled (Settings → System → Remote Play).
- Windows 10/11 PC on the same network as the PS5.
- [Veyra](https://github.com/Likely7/Veyra-NRVideo) connected to your PS5 (PS5 streaming mode).
- [reWASD](https://www.rewasd.com/). It is paid software with a free trial. Download it only from the official site.
- A keyboard and a mouse. A **wired** mouse is the safest choice (see "Problems" below).

## Setup

### 1. Group your keyboard and mouse in reWASD

1. Open reWASD. At the bottom it lists your devices.
2. Click the "Group with other devices" button (bottom right) and put **your keyboard and your mouse** into one group. Save the group.
3. If reWASD shows a device as "Please initialize the device", click it and choose what it is (keyboard or "Mouse with programmable buttons").

Not sure which device is which? Run `tools/find-input-device.py` (see "Problems").

### 2. Import the two configs

1. In the left menu, pick or create any game profile (for example "GTA 6 PS5").
2. Open the config drop-down next to the profile name → **Import** → choose `GTA6 KB+M (slot 1).rewasd`.
3. Import `GTA6 PC mode (slot 2).rewasd` the same way.

### 3. Apply them to slots

1. Select your keyboard+mouse group at the bottom.
2. Open `GTA6 PC mode`, choose **Slot 2** in the arrow next to "Apply", press Apply.
3. Open `GTA6 KB+M`, choose **Slot 1**, press Apply.
4. reWASD will offer to connect the virtual gamepad to a physical USB hub and **reboot the PC**. Choose **"No, apply without changes"**. Veyra does not need it (only Sony's official Remote Play app does).

### 4. Slot hotkeys (switching between game and PC)

reWASD → Settings → **Slots** → "Switch slots with hotkeys for": your group.

- Slot 1: **RCtrl** (back to game)
- Slot 2: **RShift** (PC mode)

Press Apply.

### 5. Veyra

1. Connect Veyra to the PS5 as usual.
2. If a DualSense or another gamepad is connected to the PC, disconnect it. Veyra uses the first gamepad it finds.
3. Keep the Veyra window active while playing. Press **F11** for fullscreen: the cursor hides by itself.

## Controls

Full table: `cheatsheet/controls-ru.html`. The essentials:

| Key | Action |
|---|---|
| WASD | Move |
| Mouse | Camera / aim |
| LMB / RMB | Shoot / aim (R2 / L2) |
| Left Shift (hold) | Sprint (auto-tap ✕) |
| Space | Jump |
| F | Enter / exit vehicle |
| R | Reload |
| Q | Cover |
| E | Pick up (L1) |
| Tab | Weapon wheel |
| Left Ctrl | Crouch |
| M | Map |
| Esc | Pause |
| **V** | Vehicle mode on/off: W gas, S brake, Space handbrake |
| **G** | Aircraft mode on/off: W up/throttle, S down, A/D yaw, arrows pitch and roll, Space landing gear |
| **Right Shift** | PC mode (gamepad off, keyboard and mouse normal) |
| **Right Ctrl** | Back to the game |
| **Ctrl + Alt + Del** | Emergency: turns reWASD remapping off completely |

Actions follow the GTA 5 console layout. If GTA 6 uses a different button for something, the gamepad button in the cheat sheet is always correct, and you can remap the key in reWASD.

## Problems

**Nothing reacts in the game.**
Make the Veyra window active. Check that the reWASD power button is lit (config applied). Check that no other gamepad is connected to the PC.

**Keyboard works on the PC, but the game ignores it after switching modes.**
Some other reWASD config, or another program, has created an extra virtual gamepad (for example an Xbox 360), and Veyra switched to it. Turn off reWASD configs on all other devices, disconnect other gamepads, then apply slot 1 again. Only one virtual DualShock 4 should remain in Device Manager.

**The Windows cursor still moves and the mouse does not turn the camera.**
reWASD does not see your mouse as a mouse. This often happens with wireless gaming mice whose receiver also presents itself as a keyboard. Connect the mouse **by cable**, initialize it in reWASD as "Mouse with programmable buttons", and add it to the group.

**How do I find which device is my mouse or keyboard?**
Install Python 3, then run in a terminal:

```
python find-input-device.py 20            (move the mouse for 20 seconds)
python find-input-device.py 15 keyboard   (type for 15 seconds)
```

It prints the device ID (VID/PID). Match it with the device tooltips in reWASD.

**reWASD shows "Group of too complex composite devices".**
Keep the group to one keyboard device and one mouse device.

## Risks and notes

- Veyra is an unofficial Remote Play client. Using unofficial clients is a grey area in Sony's terms of service. A virtual gamepad is indistinguishable from a real one for the PS5, but no guarantees.
- Mouse aim combined with aim assist can be seen as an unfair advantage in GTA Online. Story mode is the safest place to use it.
- reWASD requires a license after the trial ends.
