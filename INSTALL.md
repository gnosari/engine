# Gnosari Installation Guide

## Quick Install (Recommended)

Install gnosari with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/gnosari/gnosari/main/install.sh | bash
```

Or download and run manually:

```bash
wget https://raw.githubusercontent.com/gnosari/gnosari/main/install.sh
chmod +x install.sh
./install.sh
```

## What the Installer Does

The installer automatically:

1. **Detects your operating system** (Linux, macOS, Windows/WSL)
2. **Checks for Python 3.12+** and installs it if missing
3. **Installs gnosari** using pipx (preferred) or pip (fallback)
4. **Configures your PATH** to make `gnosari` command available
5. **Verifies the installation** works correctly

## Supported Systems

### Linux
- **Ubuntu/Debian** (apt-get)
- **CentOS/RHEL** (yum)
- **Fedora** (dnf)
- **Arch Linux** (pacman)
- **openSUSE** (zypper)
- **Alpine Linux** (apk)

### macOS
- **Intel and Apple Silicon Macs**
- Automatically installs Homebrew if needed

### Windows
- **WSL (Windows Subsystem for Linux)**
- **Git Bash/MSYS2**
- **Cygwin**

> **Note**: For native Windows, please install Python manually from [python.org](https://python.org/downloads/) first, then run the installer.

## Installation Methods

The installer tries these methods in order:

1. **pipx** (recommended) - Installs gnosari in an isolated environment
2. **pip --user** (fallback) - Installs to user directory

## Requirements

- **Python 3.12+** (automatically installed if missing)
- **Internet connection** for downloading packages
- **sudo access** (only for system Python installation on Linux)

## Troubleshooting

### Command not found after installation

If `gnosari` command is not found after installation:

```bash
# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc for Zsh users

# Or restart your terminal
```

### Permission errors on Linux

If you get permission errors:

```bash
# Run with sudo only if needed for Python installation
sudo ./install.sh
```

### Python version too old

If your system Python is too old:

```bash
# The installer will automatically install Python 3.12
# On some systems, you may need to run:
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12 python3.12-pip python3.12-venv
```

### Manual installation

If the installer fails, you can install manually:

```bash
# Install pipx
pip install --user pipx
pipx ensurepath

# Install gnosari
pipx install gnosari

# Or with pip
pip install --user gnosari
```

## Verification

After installation, verify it works:

```bash
gnosari --version
gnosari --help
```

## Uninstallation

To remove gnosari:

```bash
# If installed with pipx
pipx uninstall gnosari

# If installed with pip
pip uninstall gnosari
```

## Development Installation

For development, use Poetry instead:

```bash
git clone https://github.com/gnosari/gnosari.git
cd gnosari
poetry install
poetry run gnosari --help
```

## Getting Started

After installation, create your first team:

```bash
# Download example team configuration
curl -O https://raw.githubusercontent.com/gnosari/gnosari/main/examples/simple_team.yaml

# Run your first team
gnosari --config simple_team.yaml --message "Hello, team!"
```

For more examples and documentation, visit: https://docs.gnosari.com