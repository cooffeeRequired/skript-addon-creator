from pathlib import Path
import sys
from colorama import init, Fore, Style
from addon_creator import AddonCreator
from templates import Templates

# Initialize colorama for colored output
init()

def main():
    try:
        creator = AddonCreator()
        creator.get_inputs()
        
        # ==== PATHS ====
        group_path = Path(*creator.package_name.split("."))
        base = Path(creator.addon_name)
        src = base / "src" / "main"
        java = src / "java" / group_path
        elements = java / "elements"
        resources = src / "resources"

        for path in [elements, resources]:
            path.mkdir(parents=True, exist_ok=True)

        # ==== FILES ====
        templates = Templates()
        
        # Write files
        (resources / "plugin.yml").write_text(
            templates.get_plugin_yml(creator.addon_name, creator.package_name, creator.mc_version)
        )
        (base / "settings.gradle.kts").write_text(
            templates.get_settings_gradle(creator.addon_name)
        )
        (base / "build.gradle.kts").write_text(
            templates.get_build_gradle(
                creator.package_name,
                creator.java_version,
                creator.impl,
                creator.mc_version,
                creator.skript_version
            )
        )
        (java / f"{creator.addon_name}.java").write_text(
            templates.get_main_class(creator.addon_name, creator.package_name)
        )
        (java / "AddonLogger.java").write_text(
            templates.get_logger_class(creator.package_name)
        )
        (java / "ColorUtils.java").write_text(
            templates.get_color_utils(creator.package_name)
        )

        # Write example elements
        (elements / "EffExample.java").write_text(
            templates.get_example_effect(creator.addon_name, creator.package_name)
        )
        (elements / "CondExample.java").write_text(
            templates.get_example_condition(creator.addon_name, creator.package_name)
        )
        (elements / "ExprExample.java").write_text(
            templates.get_example_expression(creator.addon_name, creator.package_name)
        )

        # Write README.md
        (base / "README.md").write_text(
            templates.get_readme(creator.addon_name)
        )

        # Initialize Git
        if creator.use_git:
            if creator._init_git(base):
                print(f"\n{Fore.GREEN}[+] Git repository successfully initialized{Style.RESET_ALL}")
                print(f"- Primary branch: {creator.primary_branch}")
                if creator.git_url:
                    print(f"- Remote origin: {creator.git_url}")
                    if creator.init_new_repo:
                        print(f"\n{Fore.YELLOW}[!] To complete new repository initialization:{Style.RESET_ALL}")
                        print("1. Create a new repository on GitHub")
                        print("2. Run the following commands:")
                        print(f"   git remote add origin {creator.git_url}")
                        print(f"   git push -u origin {creator.primary_branch}")
            else:
                print(f"\n{Fore.YELLOW}[!] Git repository was not initialized{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}[+] Addon '{creator.addon_name}' was successfully created in: {base.absolute()}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}[!] Next steps:{Style.RESET_ALL}")
        print("1. Open the project in your IDE")
        print("2. Run 'gradle build' to build the addon")
        print("3. Find the built addon in the 'build/libs' directory")
        if creator.use_git:
            print(f"\n{Fore.CYAN}[*] Git commands:{Style.RESET_ALL}")
            print("1. Add changes:")
            print("   git add .")
            print("2. Commit changes:")
            print("   git commit -m \"Message\"")
            print("3. Push changes:")
            print("   git push -u origin " + creator.primary_branch)
        print(f"\n{Fore.CYAN}[*] Creating a release:{Style.RESET_ALL}")
        print("1. Set GITHUB_TOKEN and GITHUB_REPOSITORY environment variables")
        print("2. Create a release description file (e.g. 2.8.2.md)")
        print("3. Run the command:")
        print("   ./gradlew release -Pversion=\"2.8.2-pre\" -Pdescription=\"2.8.2.md\" -Pprerelease=true")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Operation was interrupted by user.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}[-] An error occurred: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main() 