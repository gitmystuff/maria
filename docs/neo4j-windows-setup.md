# Neo4j Community on Windows (zip install)

Using macOS or Linux? See [neo4j-mac-linux-setup.md](neo4j-mac-linux-setup.md).

These are the steps used for this project: Neo4j Community **2026.09.0**, installed from the zip archive on Windows. If you use a different version, adjust the folder names.

Links
- Download (Community, Windows zip): https://neo4j.com/deployment-center/
- System requirements: https://neo4j.com/docs/operations-manual/current/installation/requirements/
- Java (OracleJDK 21 shown here; Zulu JDK 21 also works, and Java 25 is supported): https://www.oracle.com/java/technologies/downloads/#jdk21-windows
- Windows installation manual: https://neo4j.com/docs/operations-manual/current/installation/windows/
- AuraDB (hosted, **not used** here): https://neo4j.com/product/auradb/

## 1. Install Java
Install JDK 21 and confirm it works:

```
java -version
```

## 2. Download and place Neo4j
1. Download the **Community** Windows zip for 2026.09.0 from the Deployment Center.
2. Right-click the zip and choose **Extract All**.
3. The extraction contains a folder such as `neo4j-community-2026.09.0-windows`. Open it until you find the inner folder `neo4j-community-2026.09.0`. That inner folder is the one you need.
4. Move it somewhere permanent. The root of `C:` is recommended, giving `C:\neo4j-community-2026.09.0`.

## 3. Set NEO4J_HOME
In a Command Prompt:

```
setx NEO4J_HOME "C:\neo4j-community-2026.09.0"
```

Close the Command Prompt and open a new one so `%NEO4J_HOME%` is picked up.

## 4. Start Neo4j
In **PowerShell**:

```
& "$env:NEO4J_HOME\bin\neo4j" console
```

In **Command Prompt**:

```
%NEO4J_HOME%\bin\neo4j console
```

`%NEO4J_HOME%` only works in Command Prompt. In PowerShell use `$env:NEO4J_HOME`. If `echo $env:NEO4J_HOME` prints nothing, open a new terminal, because `setx` only affects windows opened afterward. You can also use the full path, for example `C:\neo4j-community-2026.09.0\bin\neo4j console`.

Leave that window open while you work. **Ctrl+C** stops the database. When the log says it has started, open:

http://localhost:7474/browser/

## 5. First login and password
- Default user: `neo4j`
- Default password: `neo4j`

Neo4j asks you to choose a new password on first login. Put that password in your project's `.env` file as `NEO4J_PASSWORD` (see [env-and-groq.md](env-and-groq.md)).

## 6. Changing or recovering the password
- Password fields are hidden and Neo4j never displays a stored password. If Chrome saved it, open `chrome://password-manager/passwords` and search for `localhost`.
- To change a password you know, run this in the Neo4j Browser command bar:

  ```
  ALTER CURRENT USER SET PASSWORD FROM 'old_password' TO 'new_password'
  ```

- **If it is lost**, the Neo4j Operations Manual describes recovery by briefly turning authentication off. In outline, and please confirm the setting name against the manual for your version:
  1. Stop Neo4j (Ctrl+C).
  2. In `conf\neo4j.conf`, uncomment `dbms.security.auth_enabled=false` and save.
  3. Start Neo4j, open the browser and run `ALTER USER neo4j SET PASSWORD 'new_password'`.
  4. Stop Neo4j, **put the `#` back** on that line, and start again. Do not leave authentication off.
- Deleting the whole `data` folder also resets everything, but it erases every database in this installation.

## 7. Check it from the project
From the project folder:

```
uv run python scripts/check_setup.py
```

You should see `[ok] Neo4j connection`.

## Notes
- The notebook connects at `bolt://localhost:7687`. Change `NEO4J_URI` in `.env` only if you changed Neo4j's port.
- The notebook deletes every node that carries one of the labels Claim, Shop, Area, Adjuster, Customer or Interaction. Other graphs in the same database (for example a Bob and Alice demo) are left alone unless they use those same labels.
- Community Edition has a single user database. If you want the demo isolated, use a separate Neo4j installation folder or clear your own demo nodes first.
- If port 7474 or 7687 is already in use, another Neo4j instance is probably running. Stop it before starting a new one.
