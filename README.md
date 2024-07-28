# App Privacy Policy Review

This repo contains scripts, methods, and dependencies required to replicate the research found in the paper below. That being, the analysis of the efficacy of App Privacy information of individual apps .

This research was largely made possible due to prior work and research detailed in this [repo](https://github.com/TrackerControl/PlatformControl), which contains many helpful links and tools that you may find useful. This repo only focuses on the Apple App Store. 

**DISCLAIMER: The authors of this repository do not and cannot guarantee the accuracy of any data provided or any results obtained from the use of this software. Use of this repository is at your own risk. The data and code of this project are shared strictly  _for research purposes only_.**


# Preparation

In order to gather data properly, a jailbroken iPhone is required.

**Note, there are issues at the moment with `Mac` when trying to inject scripts due to new security measures added on MacOs 14**

**Note, the code in this repo may require some adjusting as it was personalized to fit the specific requirements and criteria in our research and may not fit your unique circumstances**

Listed below are the dependences and their purposes.

1. [Frida](https://github.com/frida/frida) - Used to inject scripts into the Jailbroken Device. Install on both your computer and jailbroken device
2. [mitmproxy](https://github.com/mitmproxy/mitmproxy) - Used to monitor network traffic of apps
3. [SSL-Kill-Switch 3](https://github.com/NyaMisty/ssl-kill-switch3) - Install on Jailbroken Device, bypasses SSL Certificate Pinning to allow passing network traffic through `mitmproxy`
4. libimobiledevice - An important library to communicate to IOS devices using native protocols, required to properly analyze app data. For `Mac` and `Linux` users, follow [this](https://libimobiledevice.org/#downloads) page and scroll down slightly. It will give you download options based on the operating system you select. For `Windows` users, follow [this](https://github.com/L1ghtmann/libimobiledevice/releases/) page. Install and extract the latest version, and run the binaries inside.
5. [App Store Scraper](https://github.com/facundoolano/app-store-scraper) - Required to efficiently scrape the App Privacy information of apps at scale.


A text file is required to analyze IOS apps, with each line pointing to an app file (`[bundleId].ipa`  files):

-   `./data/ios_files.txt`

For example,

```
apps/education/com.duolingo.DuolingoMobile.ipa
```

You need to create such files manually before use and also provide app files to analyze.

# Data Analysis

Once all dependencies are installed, run `appinfoscrape.js` to gather app information, then run `privacylablescrape.js` to gather the privacy label information. Run `permissions.sh` and `CheckPermissions.py` to analyze app permissions. Run `FindFrameworks.py` to get frameworks used by apps. Run `processIpas.sh` to get run the static and dynamic analysis of all apps. Lastly, run the two Jupyter notebook files `1_detect_ios_trackers.ipynb` and `2_main_analysis.ipynb` in order. (The two versions of these notebooks are slimed down versions made to fit within the scope of this research, namely, keeping it exclusive to IOS analysis.)

In our analysis, we made use of [DuckDuckGo Tracker Radar](https://github.com/duckduckgo/tracker-radar?tab=readme-ov-file#duckduckgo-tracker-radar) to analyze the network traffic between the apps and tracks.

# Credits

-   [https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy)
-   [https://github.com/noobpk/frida-ios-hook](https://github.com/noobpk/frida-ios-hook)
-   [https://github.com/NyaMisty/ssl-kill-switch3](https://github.com/NyaMisty/ssl-kill-switch3) 
- [https://github.com/TrackerControl/platformcontrol-android-ios-analysis](https://github.com/TrackerControl/platformcontrol-android-ios-analysis)
- [https://github.com/TrackerControl/PlatformControl](https://github.com/TrackerControl/PlatformControl)
- [https://github.com/frida/frida](https://github.com/frida/frida)
- [https://github.com/duckduckgo/tracker-radar](https://github.com/duckduckgo/tracker-radar)

