const store = require('app-store-scraper');
const fs = require('fs-extra');
const path = require('path');

async function scrapePrivacyInfo(appName) {
  try {
    const results = await store.search({
      term: appName,
      num: 1 // We only need the first result
    });

    if (results.length > 0) {
      const app = results[0];
      const privacyData = await store.privacy({ id: app.id });
      return privacyData;
    } else {
      throw new Error(`App not found: ${appName}`);
    }
  } catch (error) {
    console.error(`Error fetching privacy info for ${appName}:`, error);
    return null;
  }
}

async function processAppNames() {
  const appNames = fs.readFileSync('Names.txt', 'utf8').split('\n');
  const outputDir = path.join(__dirname, 'Privacy Label Information');
  await fs.ensureDir(outputDir);

  for (const appName of appNames) {
    if (appName.trim()) {
      console.log(`Processing: ${appName}`);
      const privacyInfo = await scrapePrivacyInfo(appName);
      if (privacyInfo) {
        const fileName = `${appName.trim()} Label.json`;
        const filePath = path.join(outputDir, fileName);
        await fs.writeJson(filePath, privacyInfo, { spaces: 2 });
      }
    }
  }
}

processAppNames();
