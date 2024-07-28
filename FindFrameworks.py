import frida
import sys
import csv
import subprocess

csv_dir = "./AppFrameworks.csv"

# List of known iOS frameworks to filter from all loaded modules
known_frameworks = [
    "AVFoundation",
    "AudioToolbox",
    "CFNetwork",
    "CoreGraphics",
    "CoreMedia",
    "CoreTelephony",
    "CoreVideo",
    "Foundation",
    "MediaPlayer",
    "MessageUI",
    "MobileCoreServices",
    "QuartzCore",
    "Security",
    "StoreKit",
    "SystemConfiguration",
    "UIKit",
    "AdSupport",
    "JavaScriptCore",
    "SafariServices",
    "WebKit",
    "CoreMotion",
    "CoreAudioKit",
    "CoreFoundation",
    "CoreAudio",
    "CoreData",
]


def on_message(message, data):
    if message["type"] == "send":
        print(message["payload"])
    else:
        print(message)


def main(target_process):
    if target_process.isdigit() == True:
        target_process = subprocess.run(
            "frida-ps -Ua | awk '/" + str(target_process) + "/{print $2}'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        target_process = target_process.stdout.strip()

    # Attach to the target iOS process
    session = frida.get_usb_device().attach(target_process)

    # JavaScript code to be executed in the target process
    script = session.create_script(
        """
        'use strict';
        rpc.exports = {
            enumerateFrameworks: function () {
                var frameworks = [];
                var modules = Process.enumerateModules();
                for (var i = 0; i < modules.length; i++) {
                    frameworks.push(modules[i].name);
                }
                return frameworks;
            }
        };
    """
    )

    script.on("message", on_message)
    script.load()

    # Get the list of loaded modules (frameworks) in the process
    frameworks = script.exports_sync.enumerate_frameworks()

    # Filter out the known iOS frameworks
    filtered_frameworks = [fw for fw in frameworks if fw in known_frameworks]

    with open(csv_dir, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["App Name", "Frameworks"])
        csvwriter.writerow([target_process, ", ".join(filtered_frameworks)])

    print(f"{target_process} Frameworks Added to CSV")

    session.detach()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <process_name_or_pid>" % __file__)
        sys.exit(1)

    main(sys.argv[1])
