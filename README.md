# Auto Clicker

A simple auto clicker for Windows. Set a speed, hit a hotkey, it clicks.

## Usage

- **F5** - Start clicking
- **F6** - Stop clicking
- Change the speed in **Settings > Click Speed (CPS)** (1-100, default is 5)

It clicks wherever your mouse currently is.

## Download

Grab the latest `.exe` from [Releases](../../releases).

## GPG Verification

Official releases are signed with GPG.

**Public key:** [weirdpom-public.asc](weirdpom-public.asc)

**Fingerprint:**
```text
700E 90D2 66AA EC76 B2F6
6AFE 42D5 01B2 E673 EAF7
```

To verify a release:

```bash
gpg --import weirdpom-public.asc
gpg --fingerprint 311205461+weirdpom@users.noreply.github.com
gpg --verify AutoClicker.exe.asc AutoClicker.exe
```

A successful verification should report `Good signature`.

## Run from source

```bash
pip install -r requirements.txt
python main.py
```

## Build the exe

```bash
pyinstaller AutoClicker.spec
```

## License

This project is licensed under the [0BSD License](LICENSE).
