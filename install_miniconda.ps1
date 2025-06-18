# Check and update PowerShell execution policy
Write-Host "Checking PowerShell execution policy..."
$currentPolicy = Get-ExecutionPolicy
if ($currentPolicy -eq "Restricted") {
    Write-Host "Execution policy is restricted. Updating to RemoteSigned..."
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
} else {
    Write-Host "Execution policy is already set to $currentPolicy. No changes needed."
}

# Download Miniconda installer
Write-Host "Downloading Miniconda installer..."
wget "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -outfile ".\miniconda.exe"

# Install Miniconda silently
Write-Host "Installing Miniconda..."
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait

# Delete the installer to clean up
Write-Host "Cleaning up installer..."
del .\miniconda.exe

# Add Miniconda to PATH for the current session
Write-Host "Adding Miniconda to PATH..."
$env:Path += ";C:\ProgramData\miniconda3;C:\ProgramData\miniconda3\Scripts;C:\ProgramData\miniconda3\Library\bin"

# Initialize Conda for PowerShell
Write-Host "Initializing Conda for PowerShell..."
C:\ProgramData\miniconda3\Scripts\conda.exe init powershell

# Set CUDA_HOME environment variable
Write-Host "Setting CUDA_HOME environment variable..."
$env:CUDA_HOME = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
$env:Path += ";$env:CUDA_HOME\bin"

# Restart PowerShell session
Write-Host "Please restart your PowerShell session to complete initialization."

# Set up Conda environment
Write-Host "Setting up Conda environment..."
conda env create --file environment.yml
conda update -n base -c defaults conda
git config --global user.email "u3645252@connect.hku.hk"
git config --global user.name "aza1re"
conda init 
Write-Host "Restart terminal and conda activate fisheye_gs!"