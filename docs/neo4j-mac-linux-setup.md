# Neo4j Community on macOS and Linux (tar.gz install)

This is the macOS and Linux counterpart of [neo4j-windows-setup.md](neo4j-windows-setup.md). **It has not been tested on these systems for this project.** The steps follow the general Neo4j pattern, so check them against the Operations Manual for your version if anything differs.

Links
- Download (Community, tar.gz): https://neo4j.com/deployment-center/
- System requirements: https://neo4j.com/docs/operations-manual/current/installation/requirements/
- Linux installation manual: https://neo4j.com/docs/operations-manual/current/installation/linux/
- AuraDB (hosted, **not used** here): https://neo4j.com/product/auradb/

## 1. Install Java
Install JDK 21 (Java 25 is also supported by recent Neo4j versions) and confirm it works:

```
java -version
```

On macOS, a package manager such as Homebrew can install a JDK. On Linux, use your distribution's package manager or a JDK from https://adoptium.net/.

## 2. Download and place Neo4j
1. Download the **Community** tar.gz for your version from the Deployment Center.
2. Extract it somewhere permanent, for example your home folder:

   ```
   tar -xzf neo4j-community-*-unix.tar.gz -C ~
   ```

3. You now have a folder such as `~/neo4j-community-2026.09.0`. That folder is the one you need.

## 3. Set NEO4J_HOME
For the current terminal:

```
export NEO4J_HOME=~/neo4j-community-2026.09.0
```

To keep it, add that line to `~/.zshrc` (macOS default) or `~/.bashrc`, then open a new terminal.

## 4. Start Neo4j

```
$NEO4J_HOME/bin/neo4j console
```

Leave that terminal open while you work. **Ctrl+C** stops the database. When the log says it has started, open:

http://localhost:7474/browser/

## 5. First login and password
- Default user: `neo4j`
- Default password: `neo4j`

Neo4j asks you to choose a new password on first login. Put it in your project's `.env` file as `NEO4J_PASSWORD` (see [env-and-groq.md](env-and-groq.md)).

## 6. Changing or recovering the password
- To change a password you know, run this in the Neo4j Browser command bar:

  ```
  ALTER CURRENT USER SET PASSWORD FROM 'old_password' TO 'new_password'
  ```

- **If it is lost**, the recovery steps are the same as on Windows, with `$NEO4J_HOME/conf/neo4j.conf` as the file to edit. See section 6 of [neo4j-windows-setup.md](neo4j-windows-setup.md), and confirm the setting name against the manual for your version.

## 7. Check it from the project
From the project folder:

```
uv run python scripts/check_setup.py
```

You should see `[ok] Neo4j connection`.

## Notes
- The notebook connects at `bolt://localhost:7687`. Change `NEO4J_URI` in `.env` only if you changed Neo4j's port.
- The notebook deletes every node that carries one of the labels Claim, Shop, Area, Adjuster, Customer or Interaction. Use a database that does not use those labels for other data.
- If port 7474 or 7687 is already in use, another Neo4j instance is probably running. Stop it first.
