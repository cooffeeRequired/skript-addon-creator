# Skript Addon Creator

Nástroj pro snadné vytváření Skript addonů pro Minecraft.

## Instalace

### Windows
1. Stáhněte `install.bat`
2. Spusťte `install.bat` jako administrátor
3. Počkejte na dokončení instalace

### Linux/macOS
1. Stáhněte `install.sh`
2. Otevřete terminál v adresáři se staženým souborem
3. Spusťte:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## Použití

1. Spusťte skript:
   ```bash
   python create_addon.py
   ```

2. Postupujte podle instrukcí:
   - Zadejte název addonu
   - Vyberte package name
   - Vyberte implementaci (Paper/Spigot)
   - Vyberte verzi Javy
   - Vyberte verzi Minecraftu
   - Vyberte verzi Skriptu
   - Nakonfigurujte Git (volitelné)

3. Po dokončení najdete vytvořený addon v novém adresáři

## Vytvoření release

1. Nastavte proměnné prostředí:
   ```bash
   export GITHUB_TOKEN="váš_token"
   export GITHUB_REPOSITORY="uživatel/repozitář"
   ```

2. Vytvořte soubor s popisem release (např. `2.8.2.md`)

3. Spusťte příkaz:
   ```bash
   ./gradlew release -Pversion="2.8.2-pre" -Pdescription="2.8.2.md" -Pprerelease=true
   ```

## Struktura projektu

```
src/
  ├── addon_creator.py  # Hlavní třída pro vytváření addonů
  ├── templates.py      # Šablony pro generování souborů
  └── main.py          # Vstupní bod programu
installers/
  ├── install.sh       # Instalační skript pro Linux/macOS
  └── install.bat      # Instalační skript pro Windows
```

## Požadavky

- Python 3.6+
- pip
- Git (volitelné)

## Závislosti

- requests
- inquirer
- colorama

## Licence

MIT 