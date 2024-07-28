const store = require('app-store-scraper');
const fs = require('fs-extra');
const path = require('path');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

async function fetchAppInfo(bundleId) {
    try {
        const appInfo = await store.app({ appId: bundleId, ratings: true });
        return {
            app: bundleId,
            id: appInfo.id,
            title: appInfo.title,
            rating: Math.round(appInfo.score * 10) / 10, // Round to one decimal
            num_reviews: appInfo.reviews,
            genre: appInfo.primaryGenre,
            family_genre: appInfo.contentRating,
            updated: appInfo.updated.split('T')[0], // Format: YYYY-MM-DD
            released: appInfo.released.split('T')[0] // Format: YYYY-MM-DD
        };
    } catch (error) {
        console.error(`Error fetching app info for ${bundleId}:`, error);
        return null;
    }
}

async function processBundleIds() {
    const bundleIds = fs.readFileSync('BundleIDs.txt', 'utf8').split('\n');
    const outputDir = path.join(__dirname, 'App Information');
    await fs.ensureDir(outputDir);

    const csvWriter = createCsvWriter({
        path: path.join(outputDir, 'App Info.csv'),
        header: [
            { id: 'app', title: 'App' },
            { id: 'id', title: 'ID' },
            { id: 'title', title: 'Title' },
            { id: 'rating', title: 'Rating' },
            { id: 'num_reviews', title: 'Num Reviews' },
            { id: 'genre', title: 'Genre' },
            { id: 'family_genre', title: 'Family Genre' },
            { id: 'updated', title: 'Updated' },
            { id: 'released', title: 'Released' },
            // Additional columns (empty)
            { id: 'offersiap', title: 'Offers IAP' },
            { id: 'frameworks', title: 'Frameworks' },
            { id: 'permissions', title: 'Permissions' },
            { id: 'trackersettings', title: 'Tracker Settings' },
            { id: 'Google Firebase', title: 'Google Firebase' },
            { id: 'AdID', title: 'AdID' },
            { id: 'CalendarRead', title: 'Calendar Read' },
            { id: 'CalendarWrite', title: 'Calendar Write' },
            { id: 'ContactsRead', title: 'Contacts Read' },
            { id: 'ContactsWrite', title: 'Contacts Write' },
            { id: 'Bluetooth', title: 'Bluetooth' },
            { id: 'Calendar', title: 'Calendar' },
            { id: 'Camera', title: 'Camera' },
            { id: 'Contacts', title: 'Contacts' },
            { id: 'Location', title: 'Location' },
            { id: 'Microphone', title: 'Microphone' },
            { id: 'Motion', title: 'Motion' },
            { id: 'Analytics', title: 'Analytics' }
        ]
    });

    const records = [];
    for (const bundleId of bundleIds) {
        if (bundleId.trim()) {
            console.log(`Processing: ${bundleId}`);
            const appInfo = await fetchAppInfo(bundleId);
            if (appInfo) {
                records.push(appInfo);
            }
        }
    }

    await csvWriter.writeRecords(records);
    console.log('CSV file created successfully.');
}

processBundleIds();
