if (-not $env:VIRTUAL_ENV) {
    Write-Output "This script is executed from a Python virtual environment."
}

if (Test-Path "transpiled_pc_examples") {
    Write-Output "transpiled_pc_examples already exists"
    exit 1
} else {
    New-Item -ItemType Directory -Path "transpiled_pc_examples" | Out-Null
}

Get-ChildItem -Recurse -Filter "*.pc" -Path "pc_examples" | ForEach-Object {
    $relative_path = $_.FullName.Substring((Get-Location).Path.Length + 13)
    $output_dir = Join-Path "transpiled_pc_examples" (Split-Path $relative_path -Parent)
    New-Item -ItemType Directory -Path $output_dir -Force | Out-Null
    $output_file = ($_.BaseName + ".py")
    Write-Output "Transpiling $($_.FullName) to $output_file"
    python -m ..pcc --output-rendered-source 0 -o (Join-Path $output_dir $output_file) $_.FullName
}

Write-Output "Done"
exit 0
