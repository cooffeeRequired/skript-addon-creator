from pathlib import Path
import requests
import json
from typing import List, Dict
import sys
from colorama import init, Fore, Style
import inquirer
from inquirer import themes
import re
import subprocess

# Initialize colorama for colored output
init()

class AddonCreator:
    def __init__(self):
        self.addon_name = ""
        self.package_name = ""
        self.impl = ""
        self.mc_version = ""
        self.skript_version = ""
        self.java_version = ""
        self.use_git = False
        self.git_url = ""
        self.primary_branch = "main"
        self.init_new_repo = False
        
        # Available implementations
        self.available_impls = ["paper", "purpur", "spigot", "leaf"]
        
        # Available Java versions
        self.available_java_versions = ["8", "11", "17", "21"]
        
        # Available Git branches
        self.available_branches = ["main", "master", "dev", "development"]
        
        # Load available versions
        self.mc_versions = self._fetch_minecraft_versions()
        self.skript_versions = self._fetch_skript_versions()

        # Custom theme for inquirer
        self.theme = themes.GreenPassion()

    def _fetch_minecraft_versions(self) -> List[str]:
        """Load available Minecraft versions from Paper API."""
        try:
            response = requests.get("https://api.papermc.io/v2/projects/paper")
            data = response.json()
            return [version for version in data["versions"]]
        except:
            print(f"{Fore.RED}Error loading Minecraft versions. Using default versions.{Style.RESET_ALL}")
            return ["1.20.4", "1.20.2", "1.19.4", "1.18.2"]

    def _fetch_skript_versions(self) -> List[str]:
        """Load available Skript versions from GitHub API."""
        try:
            response = requests.get("https://api.github.com/repos/SkriptLang/Skript/releases")
            data = response.json()
            return [release["tag_name"].replace("v", "") for release in data]
        except:
            print(f"{Fore.RED}Error loading Skript versions. Using default versions.{Style.RESET_ALL}")
            return ["2.7.3", "2.7.2", "2.7.1"]

    def _print_header(self):
        """Print program header."""
        print(f"\n{Fore.CYAN}=== Skript Addon Creator ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Create a new Skript addon for Minecraft{Style.RESET_ALL}\n")

    def _get_input(self, prompt: str, options: List[str] = None) -> str:
        """Get user input with optional choices."""
        if options:
            questions = [
                inquirer.List('choice',
                    message=prompt,
                    choices=options,
                    carousel=True
                )
            ]
            answers = inquirer.prompt(questions, theme=self.theme)
            return answers['choice']
        else:
            questions = [
                inquirer.Text('input',
                    message=prompt
                )
            ]
            answers = inquirer.prompt(questions, theme=self.theme)
            return answers['input']

    def _validate_package_name(self, package: str) -> bool:
        """Validate package name."""
        parts = package.split(".")
        return all(part.isalnum() for part in parts)

    def _validate_addon_name(self, name: str) -> bool:
        """Validate addon name."""
        return name.isalnum() and name[0].isalpha()

    def _convert_to_git_name(self, name: str) -> str:
        """Convert addon name to Git repository format."""
        # Convert to lowercase and replace spaces and capital letters with hyphens
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
        name = name.lower()
        # Remove special characters and replace with hyphens
        name = re.sub(r'[^a-z0-9-]', '-', name)
        # Remove duplicate hyphens
        name = re.sub(r'-+', '-', name)
        # Remove hyphens from start and end
        name = name.strip('-')
        return name

    def _validate_git_url(self, url: str) -> bool:
        """Validate Git URL."""
        # Basic pattern for Git URL
        patterns = [
            r'^https?://(?:[\w-]+\.)+[\w-]+(?:/[\w-]+)*\.git$',  # HTTPS
            r'^git@(?:[\w-]+\.)+[\w-]+:[\w-]+/[\w-]+\.git$',     # SSH
            r'^https?://(?:[\w-]+\.)+[\w-]+(?:/[\w-]+)*$'         # HTTPS without .git
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    def _init_git(self, base_path: Path):
        """Initialize Git repository."""
        try:
            # Initialize Git
            subprocess.run(['git', 'init'], cwd=base_path, check=True)
            
            # Set primary branch
            subprocess.run(['git', 'branch', '-M', self.primary_branch], cwd=base_path, check=True)
            
            # Add remote origin
            if self.git_url:
                subprocess.run(['git', 'remote', 'add', 'origin', self.git_url], cwd=base_path, check=True)
            
            # Create .gitignore
            gitignore_content = """\
# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# IntelliJ IDEA
.idea/
*.iml
*.iws
*.ipr

# Eclipse
.classpath
.project
.settings/

# VS Code
.vscode/

# Compiled files
*.class
*.jar
*.war
*.ear

# Logs
*.log

# OS specific
.DS_Store
Thumbs.db
"""
            (base_path / ".gitignore").write_text(gitignore_content)
            
            # First commit
            subprocess.run(['git', 'add', '.'], cwd=base_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=base_path, check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error initializing Git repository: {str(e)}{Style.RESET_ALL}")
            return False

    def get_inputs(self):
        """Get all required inputs from user."""
        self._print_header()
        
        # Addon name
        while True:
            self.addon_name = self._get_input("Addon name (e.g. MySkriptAddon)")
            if self._validate_addon_name(self.addon_name):
                break
            print(f"{Fore.RED}Addon name must contain only letters and numbers and start with a letter.{Style.RESET_ALL}")

        # Package name
        while True:
            self.package_name = self._get_input("Base package (e.g. com.example.myaddon)")
            if self._validate_package_name(self.package_name):
                break
            print(f"{Fore.RED}Package name must be in format com.example.myaddon{Style.RESET_ALL}")

        # Implementation
        self.impl = self._get_input("Implementation", self.available_impls)

        # Java version
        self.java_version = self._get_input("Java version", self.available_java_versions)

        # Minecraft version
        self.mc_version = self._get_input("Minecraft version", self.mc_versions)

        # Skript version
        self.skript_version = self._get_input("Skript version", self.skript_versions)

        # Git configuration
        self.use_git = self._get_input("Do you want to initialize Git repository?", ["Yes", "No"]) == "Yes"
        
        if self.use_git:
            # Initialize new repository
            self.init_new_repo = self._get_input("Do you want to initialize a new repository on GitHub?", ["Yes", "No"]) == "Yes"
            
            # Primary branch
            self.primary_branch = self._get_input("Primary branch", self.available_branches)
            
            if self.init_new_repo:
                # Generate repository name
                repo_name = self._convert_to_git_name(self.addon_name)
                print(f"\n{Fore.CYAN}Repository name will be: {repo_name}{Style.RESET_ALL}")
                
                # Git URL
                while True:
                    self.git_url = self._get_input(f"GitHub username (for https://github.com/<username>/{repo_name}.git)")
                    if self.git_url:
                        self.git_url = f"https://github.com/{self.git_url}/{repo_name}.git"
                        break
                    print(f"{Fore.RED}You must enter a GitHub username.{Style.RESET_ALL}")
            else:
                # Git URL for existing repository
                while True:
                    self.git_url = self._get_input("Git URL (e.g. https://github.com/username/repo.git)")
                    if not self.git_url or self._validate_git_url(self.git_url):
                        break
                    print(f"{Fore.RED}Invalid Git URL. Use format https://github.com/username/repo.git or git@github.com:username/repo.git{Style.RESET_ALL}") 