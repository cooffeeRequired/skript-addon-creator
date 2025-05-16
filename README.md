# Skript Addon Creator

A tool for easy creation of Skript addons for Minecraft.

## Installation

### Windows
1. Download `create_addon.bat`
2. Run `create_addon.bat` as administrator
3. Wait for the installation to complete

### Linux/macOS
1. Download `create_addon.sh`
2. Open a terminal in the directory with the downloaded file
3. Run:
   ```bash
   chmod +x create_addon.sh
   ./create_addon.sh
   ```

## Usage

1. Run the script:
   ```bash
   python src/main.py
   ```
   or on Windows:
   ```cmd
   create_addon.bat
   ```
   or on Linux/macOS:
   ```bash
   ./create_addon.sh
   ```

2. Follow the instructions:
   - Enter the addon name
   - Enter the package name
   - Select implementation (Paper/Spigot)
   - Select Java version
   - Select Minecraft version
   - Select Skript version
   - Configure Git (optional)

3. After completion, you will find the created addon in a new directory.

## Usage Example

```bash
$ python src/main.py
=== Skript Addon Creator ===
Create a new Skript addon for Minecraft
[?] Addon name (e.g. MySkriptAddon): MyAddon
[?] Base package (e.g. com.example.myaddon): com.example.myaddon
[?] Implementation: paper
[?] Java version: 17
[?] Minecraft version: 1.20.4
[?] Skript version: 2.7.3
[?] Do you want to initialize Git repository?: No
[+] Addon 'MyAddon' was successfully created in: /path/to/MyAddon
```

## Creating a Release

1. Set environment variables:
   ```bash
   export GITHUB_TOKEN="your_token"
   export GITHUB_REPOSITORY="username/repository"
   ```

2. Create a release description file (e.g. `2.8.2.md`)

3. Run the command:
   ```bash
   ./gradlew release -Pversion="2.8.2-pre" -Pdescription="2.8.2.md" -Pprerelease=true
   ```

## Project Structure

```text
src/
  ├── addon_creator.py  # Main class for addon creation
  ├── templates.py      # Templates for file generation
  └── main.py           # Program entry point
create_addon.sh         # Installer for Linux/macOS
create_addon.bat        # Installer for Windows
```

## Requirements

- Python 3.6+
- pip
- Git (optional)

## Dependencies

- requests
- inquirer
- colorama

## License

MIT 