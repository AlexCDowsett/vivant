# Vivant: Smart Raspberry Pi Doorbell System

Vivant is a smart home doorbell and access control system designed for the Raspberry Pi. It combines facial recognition, fingerprint authentication, and cloud connectivity to provide secure, convenient entry and remote communication. The system is intended for use with dedicated hardware and is not compatible with Windows.

## Features

- **Facial Recognition**: Unlock the door using a camera and face recognition algorithms.
- **Fingerprint Authentication**: Secure access with a fingerprint sensor.
- **Remote Video Calling**: Initiate video calls with visitors using Jitsi Meet in Chromium.
- **Cloud Database Integration**: Logs events and synchronizes state with a MySQL database via a PHP API hosted on AWS.
- **iOS App Integration**: Designed to communicate with a companion iOS app (not included in this repo) for remote control, notifications, and video calls.
- **Text-to-Speech (TTS) and Speech-to-Text (S2T)**: Supports TTS for visitor messages and S2T for audio processing.

## Architecture

- **Raspberry Pi**: Runs the main application and interfaces with hardware (camera, fingerprint sensor).
- **Python GUI**: The main interface (`Python/gui.py`) is built with Tkinter and manages user interaction, authentication, and hardware control.
- **Database Layer**: MySQL database schema and PHP API (`DB/sql.php`) for cloud communication and remote control.
- **Video Calls**: Uses Chromium to launch Jitsi Meet video calls for remote communication with visitors.

## Hardware Requirements

- Raspberry Pi (tested on Pi 3/4)
- Pi Camera module
- Fingerprint sensor (compatible with `pyfingerprint`)
- (Optional) Microphone and speaker for TTS/S2T

## Software Requirements

- Raspberry Pi OS (Linux)
- Python 3
- Required Python packages (see `Python/requirements.txt`)
- Chromium browser (for video calls)
- MySQL server (cloud-hosted, e.g., AWS RDS)
- PHP-enabled web server (for `sql.php` API)

## Setup & Usage

1. **Install dependencies**
   - Use the provided shell scripts in `Python/scripts/` to install OpenCV, face recognition, and other dependencies.
   - Install Chromium and required Python packages.

2. **Configure hardware**
   - Connect the camera and fingerprint sensor to the Raspberry Pi.

3. **Database setup**
   - Use `DB/init_db.sql` to create the MySQL schema.
   - Deploy `DB/sql.php` to your PHP-enabled web server (e.g., AWS EC2).
   - Update credentials as needed.

4. **Run the application**
   - Launch the main GUI: `python3 Python/gui.py`
   - Follow on-screen instructions to enroll fingerprints and faces.

5. **Remote control**
   - The system communicates with the iOS app and cloud via the PHP API. (iOS app not included.)

## Limitations

- **Platform**: Only runs on Raspberry Pi/Linux. Not compatible with Windows.
- **Hardware**: Requires specific hardware (camera, fingerprint sensor) to function.
- **Security**: Ensure your PHP API and database are secured before deploying in production.

## Project Structure

- `Python/` — Main application code (GUI, facial/fingerprint recognition, video, etc.)
- `DB/` — Database schema, PHP API, and documentation
- `s2tBites/` — Audio processing scripts and data
- `README.md` — This file

## Credits

Developed by Alex, Sam, Mihir for EEE3035 - Group H

---

For more details, see code comments and individual module documentation.