#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       ShellTemplate.sh
#   Purpose:    Demonstrates the shell script template used for the DashAR system.
#

splash_message() {
    printf "\nDashAR - an AR-based HUD for Automobiles\n"
    printf "(c)2024-%s Trevor D. Brown\n" "$(date +%Y)"
    printf "Distributed under the MIT License.\n\n"

    printf "Describe the overarching goal of the script here...\n\n"
}

parse_arguments() {
    while [ "$#" -gt 0 ]; do
        case "$1" in
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
    DASHAR_BUILD_PATH="${DASHAR_PROJECT_ROOT}Build/"
    DASHAR_SOURCE_PATH="${DASHAR_PROJECT_ROOT}Source/"
    DASHAR_BUILD_TOOLS_PATH="${DASHAR_PROJECT_ROOT}Tools/Build/"
    DASHAR_BUILD_TOOLS_RESOURCE_PATH="${DASHAR_BUILD_TOOLS_PATH}Resources/"

    PYTHON_VENV_PATH="${DASHAR_PROJECT_ROOT}.venv/"
    PYTHON_VENV_EXECUTABLE="${PYTHON_VENV_PATH}bin/python3"
    PYTHON_REQUIREMENTS_FILE="${DASHAR_BUILD_TOOLS_RESOURCE_PATH}requirements.txt"
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

final_touches() {
    printf "Some friendly conclusion. Happy templating!\n\n"
}

main() {

    # Show the splash message.
    splash_message

    # Parse the script arguments.
    parse_arguments "$@" || exit 1

    # Locate the project root. If found, proceed. Otherwise, quit.
    find_dashar_project_root || exit 1
    define_paths_and_files

    # Wrap it up.
    final_touches
}

main "$@"

