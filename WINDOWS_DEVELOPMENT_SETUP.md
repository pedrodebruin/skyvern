# Windows 11 Development Environment Setup Guide

This guide provides multiple options for setting up a Windows 11 development environment to test and improve Skyvern's Windows support.

## Option 1: Windows 11 Virtual Machine (Recommended)

### Using VMware Fusion (macOS)
1. Download VMware Fusion from https://www.vmware.com/products/fusion.html
2. Download Windows 11 ISO from Microsoft: https://www.microsoft.com/en-us/software-download/windows11
3. Create a new VM in VMware Fusion:
   - Choose "Install from disc or image"
   - Select the Windows 11 ISO
   - Choose "Windows 11" as the operating system
   - Allocate at least 4GB RAM and 50GB storage
   - Enable 3D acceleration for better performance

### Using VirtualBox (Cross-platform)
1. Download VirtualBox from https://www.virtualbox.org/
2. Download Windows 11 ISO from Microsoft
3. Create a new VM:
   - Type: Microsoft Windows
   - Version: Windows 11 (64-bit)
   - Allocate at least 4GB RAM and 50GB storage
   - Enable 3D acceleration

### Using Parallels Desktop (macOS)
1. Download Parallels Desktop from https://www.parallels.com/
2. Follow the installation wizard to create a Windows 11 VM
3. Parallels will automatically download and install Windows 11

## Option 2: Windows 11 on Cloud Services

### Microsoft Azure
1. Create an Azure account (free tier available)
2. Deploy a Windows 11 VM:
   ```bash
   # Using Azure CLI
   az vm create \
     --resource-group myResourceGroup \
     --name windows11-dev \
     --image MicrosoftWindowsDesktop:windows-11:win11-22h2-pro:latest \
     --size Standard_D2s_v3 \
     --admin-username azureuser
   ```

### AWS EC2
1. Create an AWS account
2. Launch a Windows Server 2022 instance (Windows 11 not available on EC2)
3. Use Windows Server as a substitute for testing

### Google Cloud Platform
1. Create a GCP account
2. Deploy a Windows Server VM instance

## Option 3: Windows 11 on Physical Hardware

If you have access to a Windows 11 machine:
1. Install Python 3.11+ from https://www.python.org/downloads/
2. Install Git from https://git-scm.com/download/win
3. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
4. Clone the Skyvern repository

## Required Software for Windows 11 Development

### Essential Tools
- **Python 3.11+**: https://www.python.org/downloads/
- **Git**: https://git-scm.com/download/win
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/
- **Visual Studio Code**: https://code.visualstudio.com/
- **PowerShell**: Usually pre-installed on Windows 11

### Optional Tools
- **Windows Terminal**: Available in Microsoft Store
- **Chocolatey**: Package manager for Windows
- **WSL2**: Windows Subsystem for Linux (for Linux-like development)

## Installation Commands

### Using Chocolatey (if installed)
```powershell
# Install Chocolatey first if not installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required software
choco install python git docker-desktop vscode
```

### Manual Installation
1. **Python**: Download and install from python.org
2. **Git**: Download and install from git-scm.com
3. **Docker Desktop**: Download and install from docker.com
4. **VS Code**: Download and install from code.visualstudio.com

## Environment Setup

### 1. Clone the Repository
```powershell
git clone https://github.com/skyvern-ai/skyvern.git
cd skyvern
```

### 2. Install Python Dependencies
```powershell
# Install pip if not available
python -m ensurepip --upgrade

# Install Skyvern in development mode
pip install -e .
```

### 3. Verify Installation
```powershell
# Check if skyvern command is available
skyvern --help

# Check Python version
python --version

# Check Docker
docker --version
```

## Testing Skyvern on Windows 11

### 1. Basic Quickstart Test
```powershell
# Run the quickstart command
skyvern quickstart
```

### 2. Manual Setup Test
```powershell
# Initialize Skyvern
skyvern init

# Run server
skyvern run server
```

### 3. Browser Configuration Test
```powershell
# Test browser setup
skyvern init browser
```

## Common Windows-Specific Issues

### 1. Path Issues
- Windows uses backslashes (`\`) instead of forward slashes (`/`)
- Environment variables use different syntax
- File paths may have spaces and special characters

### 2. Docker Issues
- Docker Desktop must be running
- WSL2 backend may be required
- Port conflicts with existing services

### 3. Browser Issues
- Chrome executable path differences
- User data directory paths
- Remote debugging port conflicts

### 4. Permission Issues
- PowerShell execution policy
- Administrator privileges required for some operations
- File system permissions

## Troubleshooting

### PowerShell Execution Policy
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy to allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker Issues
```powershell
# Check Docker status
docker info

# Restart Docker Desktop if needed
# Check WSL2 integration
wsl --list --verbose
```

### Python Path Issues
```powershell
# Check Python installation
where python
python --version

# Add Python to PATH if needed
# Check pip installation
pip --version
```

## Development Workflow

### 1. Make Changes
- Edit code in VS Code or your preferred editor
- Test changes locally

### 2. Test on Windows
- Run the modified commands
- Document any issues found
- Fix Windows-specific problems

### 3. Commit Changes
```powershell
git add .
git commit -m "Improve Windows 11 support"
git push
```

## Next Steps

After setting up the Windows 11 environment:

1. **Test Current Functionality**: Run `skyvern quickstart` and document any issues
2. **Identify Windows-Specific Problems**: Look for path issues, command differences, etc.
3. **Implement Fixes**: Modify the code to handle Windows-specific cases
4. **Test Fixes**: Verify that the changes work on Windows 11
5. **Document Changes**: Update documentation and add Windows-specific instructions

## Resources

- [Windows 11 Development Documentation](https://docs.microsoft.com/en-us/windows/)
- [Python on Windows](https://docs.python.org/3/using/windows.html)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/) 