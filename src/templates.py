class Templates:
    @staticmethod
    def get_plugin_yml(addon_name: str, package_name: str, mc_version: str) -> str:
        return f"""name: {addon_name}
version: 1.0.0
main: {package_name}.{addon_name}
api-version: {mc_version}
depend: [Skript]"""

    @staticmethod
    def get_settings_gradle(addon_name: str) -> str:
        return f"""rootProject.name = "{addon_name}" """

    @staticmethod
    def get_build_gradle(package_name: str, java_version: str, impl: str, mc_version: str, skript_version: str) -> str:
        return f"""plugins {{
    id 'java'
    id 'com.github.johnrengelman.shadow' version '8.1.1'
}}

group = '{package_name}'
version = '1.0.0'

java {{
    toolchain {{
        languageVersion = JavaLanguageVersion.of({java_version})
    }}
}}

repositories {{
    mavenCentral()
    maven {{ url = 'https://hub.spigotmc.org/nexus/content/repositories/snapshots/' }}
    maven {{ url = 'https://repo.skriptlang.org/releases' }}
}}

dependencies {{
    compileOnly 'org.spigotmc:spigot-api:{mc_version}-R0.1-SNAPSHOT'
    compileOnly 'ch.njol:skript:{skript_version}'
}}

tasks.withType(JavaCompile) {{
    options.encoding = 'UTF-8'
}}

shadowJar {{
    archiveBaseName.set(project.name)
    archiveClassifier.set('')
    archiveVersion.set(project.version)
}}

build {{
    dependsOn shadowJar
}}

// Release task
task release(type: Exec) {{
    dependsOn shadowJar
    
    def version = project.findProperty('version') ?: '1.0.0'
    def description = project.findProperty('description') ?: 'Release ' + version
    def prerelease = project.findProperty('prerelease') ?: 'false'
    
    def token = System.getenv('GITHUB_TOKEN')
    def repo = System.getenv('GITHUB_REPOSITORY')
    
    if (!token || !repo) {{
        throw new GradleException('GITHUB_TOKEN and GITHUB_REPOSITORY environment variables must be set')
    }}
    
    def releaseData = [
        tag_name: version,
        name: version,
        body: new File(description).text,
        draft: false,
        prerelease: prerelease == 'true'
    ]
    
    def releaseJson = groovy.json.JsonOutput.toJson(releaseData)
    
    def createRelease = "curl -X POST -H 'Authorization: token $token' -H 'Content-Type: application/json' -d '$releaseJson' https://api.github.com/repos/$repo/releases"
    def releaseId = exec {{
        commandLine 'bash', '-c', "$createRelease | jq -r '.id'"
    }}.standardOutput.asText.trim()
    
    def jarFile = "build/libs/$project.name-$version.jar"
    def uploadUrl = "https://uploads.github.com/repos/$repo/releases/$releaseId/assets?name=$project.name-$version.jar"
    
    exec {{
        commandLine 'bash', '-c', "curl -X POST -H 'Authorization: token $token' -H 'Content-Type: application/java-archive' --data-binary @$jarFile $uploadUrl"
    }}
}}"""

    @staticmethod
    def get_main_class(addon_name: str, package_name: str) -> str:
        return f"""package {package_name};

import ch.njol.skript.Skript;
import ch.njol.skript.SkriptAddon;
import org.bukkit.plugin.java.JavaPlugin;

public class {addon_name} extends JavaPlugin {{
    private static {addon_name} instance;
    private SkriptAddon addon;

    @Override
    public void onEnable() {{
        instance = this;
        
        try {{
            addon = Skript.registerAddon(this);
            addon.loadClasses("{package_name}.elements");
            getLogger().info("Addon has been enabled!");
        }} catch (Exception e) {{
            getLogger().error("Error loading addon: " + e.getMessage());
            getServer().getPluginManager().disablePlugin(this);
        }}
    }}

    @Override
    public void onDisable() {{
        getLogger().info("Addon has been disabled!");
    }}

    public static {addon_name} getInstance() {{
        return instance;
    }}

    public SkriptAddon getAddonInstance() {{
        return addon;
    }}
}}"""

    @staticmethod
    def get_logger_class(package_name: str) -> str:
        return f"""package {package_name};

import org.bukkit.ChatColor;

public class AddonLogger {{
    public static void info(String message) {{
        log(LogLevel.INFO, message);
    }}

    public static void warning(String message) {{
        log(LogLevel.WARNING, message);
    }}

    public static void error(String message) {{
        log(LogLevel.ERROR, message);
    }}

    private static void log(LogLevel level, String message) {{
        String prefix = ChatColor.GRAY + "[" + level.getColor() + level.name() + ChatColor.GRAY + "] " + ChatColor.RESET;
        {package_name}.{package_name.split(".")[-1]}.getInstance().getLogger().info(prefix + message);
    }}

    private enum LogLevel {{
        INFO(ChatColor.GREEN),
        WARNING(ChatColor.YELLOW),
        ERROR(ChatColor.RED);

        private final ChatColor color;

        LogLevel(ChatColor color) {{
            this.color = color;
        }}

        public ChatColor getColor() {{
            return color;
        }}
    }}
}}"""

    @staticmethod
    def get_color_utils(package_name: str) -> str:
        return f"""package {package_name};

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.MiniMessage;

public class ColorUtils {{
    private static final MiniMessage miniMessage = MiniMessage.miniMessage();

    // Predefined colors
    public static final String PRIMARY = "<#3498db>";
    public static final String SECONDARY = "<#2ecc71>";
    public static final String ACCENT = "<#e74c3c>";
    public static final String WARNING = "<#f1c40f>";
    public static final String ERROR = "<#e74c3c>";
    public static final String SUCCESS = "<#2ecc71>";
    public static final String INFO = "<#95a5a6>";

    // Message templates
    public static final String SUCCESS_TEMPLATE = "<green>[+] {{message}}</green>";
    public static final String ERROR_TEMPLATE = "<red>[-] {{message}}</red>";
    public static final String WARNING_TEMPLATE = "<yellow>[!] {{message}}</yellow>";
    public static final String INFO_TEMPLATE = "<gray>[*] {{message}}</gray>";

    public static Component parse(String message) {{
        return miniMessage.deserialize(message);
    }}

    public static String format(String template, String message) {{
        return template.replace("{{message}}", message);
    }}
}}"""

    @staticmethod
    def get_example_effect(addon_name: str, package_name: str) -> str:
        return f"""package {package_name}.elements;

import ch.njol.skript.Skript;
import ch.njol.skript.doc.Description;
import ch.njol.skript.doc.Examples;
import ch.njol.skript.doc.Name;
import ch.njol.skript.doc.Since;
import ch.njol.skript.lang.Effect;
import ch.njol.skript.lang.Expression;
import ch.njol.skript.lang.SkriptParser;
import ch.njol.util.Kleenean;
import org.bukkit.entity.Player;
import org.bukkit.event.Event;
import org.jetbrains.annotations.NotNull;

@Name("Send Message")
@Description("Sends a message to a player")
@Examples({{
    "send \"Hello!\" to player",
    "send \"Welcome %player%!\" to all players"
}})
@Since("1.0.0")
public class EffExample extends Effect {{
    static {{
        Skript.registerEffect(EffExample.class,
            "send %string% to %players%"
        );
    }}

    private Expression<String> message;
    private Expression<Player> players;

    @Override
    protected void execute(@NotNull Event e) {{
        String msg = message.getSingle(e);
        if (msg == null) return;

        for (Player player : players.getArray(e)) {{
            player.sendMessage(msg);
        }}
    }}

    @Override
    public @NotNull String toString(Event e, boolean debug) {{
        return "send " + message.toString(e, debug) + " to " + players.toString(e, debug);
    }}

    @Override
    public boolean init(Expression<?>[] exprs, int matchedPattern, @NotNull Kleenean isDelayed, @NotNull SkriptParser.ParseResult parseResult) {{
        message = (Expression<String>) exprs[0];
        players = (Expression<Player>) exprs[1];
        return true;
    }}
}}"""

    @staticmethod
    def get_example_condition(addon_name: str, package_name: str) -> str:
        return f"""package {package_name}.elements;

import ch.njol.skript.Skript;
import ch.njol.skript.doc.Description;
import ch.njol.skript.doc.Examples;
import ch.njol.skript.doc.Name;
import ch.njol.skript.doc.Since;
import ch.njol.skript.lang.Condition;
import ch.njol.skript.lang.Expression;
import ch.njol.skript.lang.SkriptParser;
import ch.njol.util.Kleenean;
import org.bukkit.entity.Player;
import org.bukkit.event.Event;
import org.jetbrains.annotations.NotNull;

@Name("Has Permission")
@Description("Checks if a player has a specific permission")
@Examples({{
    "if player has permission \"myaddon.use\":",
    "    send \"You have permission!\" to player"
}})
@Since("1.0.0")
public class CondExample extends Condition {{
    static {{
        Skript.registerCondition(CondExample.class,
            "%players% (has|have) permission %string%",
            "%players% (doesn't|does not|do not|don't) have permission %string%"
        );
    }}

    private Expression<Player> players;
    private Expression<String> permission;
    private boolean isNegated;

    @Override
    public boolean check(@NotNull Event e) {{
        String perm = permission.getSingle(e);
        if (perm == null) return false;

        boolean hasPermission = true;
        for (Player player : players.getArray(e)) {{
            if (!player.hasPermission(perm)) {{
                hasPermission = false;
                break;
            }}
        }}

        return isNegated != hasPermission;
    }}

    @Override
    public @NotNull String toString(Event e, boolean debug) {{
        return players.toString(e, debug) + (isNegated ? " doesn't have" : " has") + " permission " + permission.toString(e, debug);
    }}

    @Override
    public boolean init(Expression<?>[] exprs, int matchedPattern, @NotNull Kleenean isDelayed, @NotNull SkriptParser.ParseResult parseResult) {{
        players = (Expression<Player>) exprs[0];
        permission = (Expression<String>) exprs[1];
        isNegated = matchedPattern == 1;
        return true;
    }}
}}"""

    @staticmethod
    def get_example_expression(addon_name: str, package_name: str) -> str:
        return f"""package {package_name}.elements;

import ch.njol.skript.Skript;
import ch.njol.skript.doc.Description;
import ch.njol.skript.doc.Examples;
import ch.njol.skript.doc.Name;
import ch.njol.skript.doc.Since;
import ch.njol.skript.expressions.base.SimplePropertyExpression;
import ch.njol.skript.lang.Expression;
import ch.njol.skript.lang.SkriptParser;
import ch.njol.util.Kleenean;
import org.bukkit.entity.Player;
import org.bukkit.event.Event;
import org.jetbrains.annotations.NotNull;

@Name("Player Name")
@Description("Returns the name of a player")
@Examples({{
    "set {{addon_name}} to player's name",
    "send \"Your name is %player's name%\" to player"
}})
@Since("1.0.0")
public class ExprExample extends SimplePropertyExpression<Player, String> {{
    static {{
        register(ExprExample.class, String.class, "name", "players");
    }}

    @Override
    public String convert(Player player) {{
        return player.getName();
    }}

    @Override
    public @NotNull Class<? extends String> getReturnType() {{
        return String.class;
    }}

    @Override
    protected @NotNull String getPropertyName() {{
        return "name";
    }}
}}"""

    @staticmethod
    def get_readme(addon_name: str) -> str:
        return f"""# {addon_name}

A Skript addon for Minecraft.

## Building

To build the addon, run:

```bash
./gradlew build
```

The built addon will be in the `build/libs` directory.

## Creating a Release

1. Set the following environment variables:
   - `GITHUB_TOKEN`: Your GitHub personal access token
   - `GITHUB_REPOSITORY`: The repository name (e.g. "username/repo")

2. Create a release description file (e.g. `2.8.2.md`)

3. Run the release command:
   ```bash
   ./gradlew release -Pversion="2.8.2-pre" -Pdescription="2.8.2.md" -Pprerelease=true
   ```

## License

This project is licensed under the MIT License.""" 