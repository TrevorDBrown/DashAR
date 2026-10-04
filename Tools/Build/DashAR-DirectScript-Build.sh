#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       DashAR-DirectScript-Build.sh
#   Purpose:    This script sets up the DashAR System for use on the ICS device, using Direct Script mode.
#               Note: while it says "Build", it's really just shuffling the files in place. :)
#

splash_message() {
    printf "\nDashAR - an AR-based HUD for Automobiles\n"
    printf "(c)2024-%s Trevor D. Brown\n" "$(date +%Y)"
    printf "Distributed under the MIT License.\n\n"

    printf "\"Building\" DashAR in Direct Script mode...\n\n"
}

parse_arguments() {
    DASHAR_CLEAN_BUILD=0

    while [ "$#" -gt 0 ]; do
        case "$1" in
            --clean)
                DASHAR_CLEAN_BUILD=1
                ;;
            *)
                printf "Unknown argument: %s\n" "$1"
                return 1
                ;;
        esac

        shift
    done

    return 0
}

define_paths_and_files() {
    DASHAR_SOURCE_PATH="${DASHAR_PROJECT_ROOT}Source/"
    DASHAR_BUILD_PATH="${DASHAR_PROJECT_ROOT}Build/"
    DASHAR_BUILD_TOOLS_PATH="${DASHAR_PROJECT_ROOT}Tools/Build/"
    DASHAR_BUILD_TOOLS_RESOURCE_PATH="${DASHAR_BUILD_TOOLS_PATH}Resources/"
    DASHAR_BUILD_RESOURCES_PATH="${DASHAR_PROJECT_ROOT}Resources/"

    DASHAR_HUD_BUILD_PATH="${DASHAR_BUILD_PATH}HUD/"
    DASHAR_HUD_BUILD_RESOURCES_PATH="${DASHAR_BUILD_RESOURCES_PATH}HUD/"

    DASHAR_DAS_BUILD_PATH="${DASHAR_BUILD_PATH}DAS/"
    DASHAR_DAS_BUILD_RESOURCES_PATH="${DASHAR_BUILD_RESOURCES_PATH}DAS/"

    DASHAR_COMPANION_BUILD_PATH="${DASHAR_BUILD_PATH}Companion/"
    DASHAR_COMPANION_BUILD_RESOURCES_PATH="${DASHAR_BUILD_RESOURCES_PATH}Companion/"

    PYTHON_VENV_PATH="${DASHAR_PROJECT_ROOT}.venv/"
    PYTHON_VENV_EXECUTABLE="${PYTHON_VENV_PATH}bin/python3"
}

find_dashar_project_root() {
    DASHAR_ROOT_SEARCH_PATH="$PWD"

    printf "Locating the project root...\n"

    # Locate .dashar_root
    while [ ! -f "$DASHAR_ROOT_SEARCH_PATH/.dashar_root" ]; do
        if [ "$DASHAR_ROOT_SEARCH_PATH" = "/" ]; then
            printf "No .dashar_root found. Exiting.\n"
            unset DASHAR_ROOT_SEARCH_PATH
            return 1
        fi

        DASHAR_ROOT_SEARCH_PATH=$(dirname "$DASHAR_ROOT_SEARCH_PATH")
    done

    if ! cd "$DASHAR_ROOT_SEARCH_PATH"; then
        unset DASHAR_ROOT_SEARCH_PATH
        return 1
    fi

    DASHAR_PROJECT_ROOT="${PWD}/"

    printf "DashAR Project root found at %s.\n\n" "$DASHAR_PROJECT_ROOT"

    unset DASHAR_ROOT_SEARCH_PATH

    return 0
}

determine_host_platform() {
    printf "Determining host platform...\n"

    case "$(uname -s)" in
        Linux)
            DASHAR_PLATFORM="Linux"
            ;;
        Darwin)
            DASHAR_PLATFORM="macOS"
            ;;
        *)
            DASHAR_PLATFORM="Unknown"
            ;;
    esac

    printf "Current platform is %s.\n\n" "$DASHAR_PLATFORM"

    return 0
}

clean_build_directories() {
    # Skip if a clean build was not requested.
    if [ "$DASHAR_CLEAN_BUILD" -ne 1 ]; then
        return 0
    fi

    printf "Cleaning existing build directories...\n"

    # Remove and recreate the build directories.
    rm -rf "$DASHAR_DAS_BUILD_PATH" || return 1
    rm -rf "$DASHAR_HUD_BUILD_PATH" || return 1
    rm -rf "$DASHAR_COMPANION_BUILD_PATH" || return 1

    mkdir -p "$DASHAR_DAS_BUILD_PATH" || return 1
    mkdir -p "$DASHAR_HUD_BUILD_PATH" || return 1
    mkdir -p "$DASHAR_COMPANION_BUILD_PATH" || return 1

    printf "Build directories cleaned.\n\n"

    return 0
}

validate_and_deploy_das_scripts() {
    printf "Deploying Data Aggregator and Server scripts...\n"

    # Verify that the DAS source directory exists.
    if [ ! -d "${DASHAR_SOURCE_PATH}DAS/" ]; then
        printf "Error: %s does not exist. Exiting.\n" "${DASHAR_SOURCE_PATH}DAS/"
        return 1
    fi

    # Locate and deploy Python scripts while preserving their directory structure.
    find "${DASHAR_SOURCE_PATH}DAS/" \
        -type d -name "third_party" -prune -o \
        -type f -name "*.py" -print |
    while IFS= read -r DASHAR_DAS_SOURCE_FILE; do
        DASHAR_DAS_RELATIVE_FILE="${DASHAR_DAS_SOURCE_FILE#"${DASHAR_SOURCE_PATH}DAS/"}"
        DASHAR_DAS_DESTINATION_FILE="${DASHAR_DAS_BUILD_PATH}${DASHAR_DAS_RELATIVE_FILE}"
        DASHAR_DAS_DESTINATION_PATH=$(dirname "$DASHAR_DAS_DESTINATION_FILE")

        mkdir -p "$DASHAR_DAS_DESTINATION_PATH" || exit 1
        cp -v "$DASHAR_DAS_SOURCE_FILE" "$DASHAR_DAS_DESTINATION_FILE" || exit 1
    done

    # Remove the placeholder file from the DAS build directory.
    if ! rm -f "${DASHAR_DAS_BUILD_PATH}.gitkeep"; then
        printf "Failed to remove %s. Exiting.\n" "${DASHAR_DAS_BUILD_PATH}.gitkeep"
        return 1
    fi

    printf "Data Aggregator and Server scripts copied to %s.\n\n" "$DASHAR_DAS_BUILD_PATH"

    return 0
}

validate_and_deploy_das_resources() {
    printf "Deploying Data Aggregator and Server data resources...\n"
    DASHAR_DAS_BUILD_DATA_RESOURCES_PATH="${DASHAR_DAS_BUILD_RESOURCES_PATH}data/"

    if [ -d "$DASHAR_DAS_BUILD_DATA_RESOURCES_PATH" ]; then
        mkdir -p "${DASHAR_DAS_BUILD_PATH}data/"
        cp -Rv "${DASHAR_DAS_BUILD_DATA_RESOURCES_PATH}." "${DASHAR_DAS_BUILD_PATH}data/"
    else
        printf "Error: %s does not exist. Exiting.\n" "$DASHAR_DAS_BUILD_DATA_RESOURCES_PATH"
        return 1
    fi

    printf "Data files copied to %s.\n\n" "$DASHAR_DAS_BUILD_DATA_RESOURCES_PATH"

    unset DASHAR_DAS_BUILD_DATA_RESOURCES_PATH

    return 0
}

linux_setup_wifi_hotspot() {
    printf "Setting up persistent Wi-Fi Access Point...\n"
    printf "SSID: DashAR-Network\n"
    printf "Password: ConnectToDashAR\n"

    # Check if nmcli is installed.
    if ! command -v nmcli > /dev/null 2>&1; then
        printf "nmcli is not installed or could not be found in PATH. Exiting.\n"
        return 1
    fi

    # Create the Wi-Fi Access Point/Hotspot.
    if ! nmcli device wifi hotspot ssid "DashAR-Network" password "ConnectToDashAR"; then
        printf "Failed to set up WiFi Hotspot. Exiting.\n"
        return 1
    fi

    printf "WiFi Hotspot setup complete.\n\n"
    return 0
}

setup_das() {
    printf "Setting up Data Aggregator and Server...\n"

    # Deploy DAS scripts to Build/DAS/.
    validate_and_deploy_das_scripts || exit 1

    # Deploy configuration and base database template to Build/DAS/.
    validate_and_deploy_das_resources || exit 1

    # If platform is Linux, set up the Wi-Fi hotspot.
    if [ "$DASHAR_PLATFORM" = "Linux" ]; then
        linux_setup_wifi_hotspot || exit 1
    else
        printf "Warning: host platform is not Linux. Cannot set up WiFi Hotspot.\n\n"
    fi

    printf "Data Aggregator and Server is ready at %s.\n\n" "$DASHAR_DAS_BUILD_PATH"
    return 0
}

final_touches() {
    printf "The DashAR System has successfully built in Direct Script mode. Happy driving!\n\n"
}

main() {

    # Show the splash message.
    splash_message

    # Parse the script arguments.
    parse_arguments "$@" || exit 1

    # Determine the host platform.
    determine_host_platform || exit 1

    # Locate the project root. If found, proceed. Otherwise, quit.
    find_dashar_project_root || exit 1
    define_paths_and_files

    # Clean Build directories (if --clean is provided...)
    clean_build_directories || exit 1

    # DAS Setup
    setup_das || exit 1

    # Companion Setup
    # Currently, no action.

    # HUD App Setup
    # Currently, no action.

    # Wrap it up.
    final_touches
}

main "$@"

