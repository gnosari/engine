#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="windows"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    print_info "Detected OS: $OS"
}

# Detect Linux distribution and package manager
detect_linux_distro() {
    if [[ "$OS" != "linux" ]]; then
        return
    fi

    if command -v apt-get >/dev/null 2>&1; then
        DISTRO="debian"
        PKG_MANAGER="apt-get"
        PKG_UPDATE="apt-get update"
        PKG_INSTALL="apt-get install -y"
        PYTHON_PKG="python3 python3-pip python3-venv"
    elif command -v yum >/dev/null 2>&1; then
        DISTRO="rhel"
        PKG_MANAGER="yum"
        PKG_UPDATE="yum update -y"
        PKG_INSTALL="yum install -y"
        PYTHON_PKG="python3 python3-pip python3-venv"
    elif command -v dnf >/dev/null 2>&1; then
        DISTRO="fedora"
        PKG_MANAGER="dnf"
        PKG_UPDATE="dnf update -y"
        PKG_INSTALL="dnf install -y"
        PYTHON_PKG="python3 python3-pip python3-venv"
    elif command -v pacman >/dev/null 2>&1; then
        DISTRO="arch"
        PKG_MANAGER="pacman"
        PKG_UPDATE="pacman -Sy"
        PKG_INSTALL="pacman -S --noconfirm"
        PYTHON_PKG="python python-pip"
    elif command -v zypper >/dev/null 2>&1; then
        DISTRO="opensuse"
        PKG_MANAGER="zypper"
        PKG_UPDATE="zypper refresh"
        PKG_INSTALL="zypper install -y"
        PYTHON_PKG="python3 python3-pip python3-venv"
    elif command -v apk >/dev/null 2>&1; then
        DISTRO="alpine"
        PKG_MANAGER="apk"
        PKG_UPDATE="apk update"
        PKG_INSTALL="apk add"
        PYTHON_PKG="python3 py3-pip py3-venv"
    else
        print_error "Unsupported Linux distribution. Could not detect package manager."
        exit 1
    fi
    
    print_info "Detected Linux distro: $DISTRO ($PKG_MANAGER)"
}

# Check if Python is installed and get version
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        return 1
    fi

    # Get Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    # Check if Python 3.12+
    if [[ $PYTHON_MAJOR -eq 3 ]] && [[ $PYTHON_MINOR -ge 12 ]]; then
        print_success "Found Python $PYTHON_VERSION"
        return 0
    elif [[ $PYTHON_MAJOR -gt 3 ]]; then
        print_success "Found Python $PYTHON_VERSION"
        return 0
    else
        print_warning "Found Python $PYTHON_VERSION, but gnosari requires Python 3.12+"
        return 1
    fi
}

# Install Python based on OS
install_python() {
    print_info "Installing Python..."

    case $OS in
        "linux")
            print_info "Updating package manager..."
            sudo $PKG_UPDATE
            print_info "Installing Python and pip..."
            sudo $PKG_INSTALL $PYTHON_PKG
            ;;
        "macos")
            if ! command -v brew >/dev/null 2>&1; then
                print_info "Installing Homebrew first..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                
                # Add Homebrew to PATH for current session
                if [[ -f "/opt/homebrew/bin/brew" ]]; then
                    # Apple Silicon Mac
                    export PATH="/opt/homebrew/bin:$PATH"
                    eval "$(/opt/homebrew/bin/brew shellenv)"
                else
                    # Intel Mac
                    export PATH="/usr/local/bin:$PATH"
                    eval "$(/usr/local/bin/brew shellenv)"
                fi
            fi
            print_info "Installing Python via Homebrew..."
            brew install python@3.12
            ;;
        "windows")
            print_error "Automatic Python installation on Windows is not supported."
            print_info "Please install Python manually from https://python.org/downloads/"
            print_info "Make sure to check 'Add Python to PATH' during installation."
            exit 1
            ;;
    esac

    # Verify Python installation
    if ! check_python; then
        print_error "Python installation failed or version is still too old"
        exit 1
    fi
}

# Check if pip is available
check_pip() {
    if command -v pip3 >/dev/null 2>&1; then
        PIP_CMD="pip3"
        return 0
    elif command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip"
        return 0
    else
        return 1
    fi
}

# Install pipx
install_pipx() {
    if command -v pipx >/dev/null 2>&1; then
        print_success "pipx is already installed"
        return 0
    fi

    print_info "Installing pipx..."
    if ! check_pip; then
        print_error "pip is not available. Cannot install pipx."
        return 1
    fi

    $PIP_CMD install --user pipx
    
    # Add pipx to PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    # Ensure pipx is available
    if command -v pipx >/dev/null 2>&1; then
        pipx ensurepath
        print_success "pipx installed successfully"
        return 0
    else
        print_warning "pipx installation may have succeeded but is not in PATH"
        return 1
    fi
}

# Install gnosari using pipx or pip
install_gnosari() {
    print_info "Installing gnosari..."

    # Try pipx first (preferred method)
    if install_pipx; then
        print_info "Installing gnosari with pipx..."
        pipx install gnosari
        if command -v gnosari >/dev/null 2>&1; then
            print_success "gnosari installed successfully with pipx"
            return 0
        fi
    fi

    # Fallback to pip
    print_info "Falling back to pip installation..."
    if check_pip; then
        $PIP_CMD install --user gnosari
        
        # Add user bin to PATH if not already there
        USER_BIN="$HOME/.local/bin"
        if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
            export PATH="$USER_BIN:$PATH"
        fi
        
        if command -v gnosari >/dev/null 2>&1; then
            print_success "gnosari installed successfully with pip"
            return 0
        else
            print_error "gnosari installation failed"
            return 1
        fi
    else
        print_error "Neither pipx nor pip are available"
        return 1
    fi
}

# Configure PATH permanently
configure_path() {
    print_info "Configuring PATH..."

    local shell_rc=""
    local user_bin="$HOME/.local/bin"
    
    # Detect shell and set appropriate config file
    if [[ -n "$ZSH_VERSION" ]] || [[ "$SHELL" == *"zsh"* ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]] || [[ "$SHELL" == *"bash"* ]]; then
        shell_rc="$HOME/.bashrc"
        # On macOS, also check .bash_profile
        if [[ "$OS" == "macos" ]] && [[ -f "$HOME/.bash_profile" ]]; then
            shell_rc="$HOME/.bash_profile"
        fi
    else
        shell_rc="$HOME/.profile"
    fi

    # Add PATH export if not already present
    if [[ -f "$shell_rc" ]] && ! grep -q "\.local/bin" "$shell_rc"; then
        echo "" >> "$shell_rc"
        echo "# Added by gnosari installer" >> "$shell_rc"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$shell_rc"
        print_success "Added $user_bin to PATH in $shell_rc"
    fi

    # For pipx installations, also ensure pipx path
    if command -v pipx >/dev/null 2>&1; then
        local pipx_bin
        pipx_bin=$(pipx environment --value PIPX_BIN_DIR 2>/dev/null || echo "$HOME/.local/bin")
        if [[ -f "$shell_rc" ]] && ! grep -q "pipx ensurepath" "$shell_rc"; then
            echo "# Ensure pipx is in PATH" >> "$shell_rc"
            echo "export PATH=\"$pipx_bin:\$PATH\"" >> "$shell_rc"
        fi
    fi
}

# Verify installation
verify_installation() {
    print_info "Verifying installation..."
    
    if command -v gnosari >/dev/null 2>&1; then
        local version
        version=$(gnosari --version 2>/dev/null || echo "unknown")
        print_success "gnosari is installed and working! Version: $version"
        print_info "Try running: gnosari --help"
        return 0
    else
        print_error "gnosari command not found in PATH"
        print_info "You may need to restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
        return 1
    fi
}

# Main installation function
main() {
    echo "=========================================="
    echo "         Gnosari AI Teams Installer"
    echo "=========================================="
    echo ""

    # Check if running as root
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root is not recommended"
        print_info "The installer will install gnosari for the current user"
    fi

    # Detect OS and distro
    detect_os
    detect_linux_distro

    # Check Python
    if ! check_python; then
        print_warning "Python 3.8+ not found"
        install_python
    fi

    # Install gnosari
    if ! install_gnosari; then
        print_error "Failed to install gnosari"
        exit 1
    fi

    # Configure PATH
    configure_path

    # Verify installation
    verify_installation

    echo ""
    print_success "Installation complete!"
    echo ""
    print_info "To get started:"
    print_info "  1. Restart your terminal or run: source ~/.bashrc"
    print_info "  2. Run: gnosari --help"
    print_info "  3. Check out examples at: https://github.com/gnosari/gnosari"
    echo ""
}

# Run main function
main "$@"