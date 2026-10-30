# Installera under /hockey/

Kopiera **hockey/** och **.github/** till roten av ditt befintliga GitHub-repository. Webbplatsen är då tillgänglig på `https://www.mydomain.dev/hockey/` **om** din befintliga GitHub–Namecheap-deploy bevarar samma katalogstruktur i webbrot. Behåll `hockey/index.html`, `hockey/css/`, `hockey/js/` och `hockey/data/` tillsammans.

GitHub Actions-workflow måste ligga i `.github/workflows/update-matches.yml` i repositoryts rot. Den uppdaterar endast `hockey/data/matches.json` och använder `hockey/scripts/update_matches.py`. Kör Actions > Kontrollera matchschema > Run workflow för att testa.

Schemat är kl 00, 08, 16 Europe/Stockholm; GitHub kan starta med fördröjning. Automatkollen omfattar tills vidare bara herr-VM 2027 och behöver lyckas mot IIHF:s aktuella sidformat.

---

# Tre Kronor Matchcenter – automatisk kontroll

## Installation

1. Packa upp filerna i **roten på din GitHub-repo** (eller anpassa din deployment-sökväg). Säkerställ att även den dolda `.github`-mappen följer med.
2. Lägg upp på `main`. Kontrollera att GitHub → **Actions** är aktiverat, att workflow har rätt att skriva till repot (`Settings → Actions → General → Workflow permissions → Read and write permissions`) och att `main` inte blockerar botens push.
3. Testkör **Actions → Kontrollera matchschema → Run workflow**. Om den lyckas och hittar ändringar committas `data/matches.json`, vilket triggar din befintliga Namecheap-deploy.
4. Schemat `0 0,8,16 * * *` och `timezone: Europe/Stockholm` ger planerade kontroller kl. **00:00, 08:00, 16:00 svensk tid**, även vid sommartid. GitHub Actions kan bli fördröjt, särskilt vid hel timme; garanterad exakt klockslag finns inte.
5. Sajten läser JSON vid sidladdning och kontrollerar för ny version var femte minut när den är öppen. Nedräkningen uppdateras varje sekund.

## Viktig begränsning

Den **fungerande automatiska källkontrollen omfattar i denna version endast de sju kända svenska gruppspelsmatcherna i herr-VM 2027** från officiella `https://stats.iihf.com/Hydra/985/index.html`. Det går inte att säkert påstå att Swehockey, JVM, damerna eller TV-rättigheterna hämtas automatiskt utan separata testade integrationer. Övriga 18 matcher är migrerade från din tidigare sammanställning och är **inte nyverifierade**. I JSON-filen finns `sourceStatus` per match.

Scriptet avbryter utan att skriva över filen om IIHF ändrat HTML-format, saknar någon av de 7 förväntade matcherna eller ändrar motståndare. Se då felloggen i Actions.

För att uppdatera även **nya matcher**, **resultat**, **dam**, **JVM**, **TV** behövs fler säkra adapters med stabila officiella datakällor, datavalidering och källspårning. Denna version automatiserar alltså *kontroll och verifierade tidsändringar* av VM-gruppspelet, inte fullständigt all hockeydata.

### 'Senaste källkontroll'

Den sparade tidpunkten uppdateras endast vid den första lyckade kontrollen eller när källuppgifterna har ändrats, för att undvika commits och omdeploys var åttonde timme. Den motsvarar därmed **senaste registrerade verifiering**, inte nödvändigtvis senaste körningen av GitHub Actions. För körhistorik: Actions-fliken.

## Kalender

- **Lägg alla kommande i kalendern**: en enda `.ics` med alla framtida matcher, oavsett filter.
- **Lägg synliga kommande i kalendern**: en enda `.ics` för de kommande matcher som matchar aktuella filter.
- Enskilda matcher kan fortfarande exporteras från respektive matchkort.

En `.ics`-import är en **ögonblicksbild**, inte en kalenderprenumeration. Om tider ändras på webbplatsen uppdateras inte redan importerade kalenderposter automatiskt. För prenumeration behövs en publicerad `.ics`-feed med stabila UID och korrekt kalender-URL.

## Lokal test

Kör `python -m http.server 8000` från projektroten och öppna `http://localhost:8000`. Dubbelklicka inte på `index.html` eftersom `fetch()` av JSON kan blockeras för `file://`.

## Filstruktur

- `index.html` – innehåll
- `css/style.css` – design
- `js/app.js` – interaktivitet, filter, klocka, kalender
- `data/matches.json` – matchdata
- `scripts/update_matches.py` – säker datakontroll
- `.github/workflows/update-matches.yml` – schema (svensk tid)
