#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       DashAR-Development-Setup.sh
#   Purpose:    Sets up development tools for DashAR.
#


splash_message() {
    printf "\nDashAR - an AR-based HUD for Automobiles\n"
    printf "(c)2024-%s Trevor D. Brown\n" "$(date +%Y)"
    printf "Distributed under the MIT License.\n\n"

    printf "Setting up development tools...\n\n"
}

parse_arguments() {
    DASHAR_CLEAN_SETUP=0

    while [ "$#" -gt 0 ]; do
        case "$1" in
            --clean)
                DASHAR_CLEAN_SETUP=1
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

clean_python_virtual_environment() {
    if [ "$DASHAR_CLEAN_SETUP" -ne 1 ]; then
        return 0
    fi

    printf "Cleaning Python virtual environment...\n"

    if [ -d "$PYTHON_VENV_PATH" ]; then
        if ! rm -rf "$PYTHON_VENV_PATH"; then
            printf "Failed to remove Python virtual environment at %s. Exiting.\n" "$PYTHON_VENV_PATH"
            return 1
        fi

        printf "Python virtual environment removed from %s.\n\n" "$PYTHON_VENV_PATH"
    else
        printf "No existing Python virtual environment found to clean.\n\n"
    fi

    return 0
}

setup_python_virtual_environment() {
    printf "Setting up Python virtual environment...\n"

    # Verify that Python 3 is installed.
    if ! command -v python3 > /dev/null 2>&1; then
        printf "Python 3 is not installed or could not be found in PATH. Exiting.\n"
        return 1
    fi

    # Create the virtual environment.
    if ! python3 -m venv "$PYTHON_VENV_PATH"; then
        printf "Failed to create Python virtual environment at %s. Exiting.\n" "$PYTHON_VENV_PATH"
        return 1
    fi

    printf "Python virtual environment created at %s.\n\n" "$PYTHON_VENV_PATH"

    return 0
}

install_python_requirements() {
    printf "Installing Python requirements to virtual environment...\n"

    # Verify that the requirements file exists.
    if [ ! -f "$PYTHON_REQUIREMENTS_FILE" ]; then
        printf "Python requirements file not found at %s. Exiting.\n" "$PYTHON_REQUIREMENTS_FILE"
        return 1
    fi

    # Verify that the virtual environment exists.
    if [ ! -x "$PYTHON_VENV_EXECUTABLE" ]; then
        printf "Python virtual environment not found at %s. Exiting.\n" "$PYTHON_VENV_PATH"
        return 1
    fi

    # Install the Python requirements into the virtual environment.
    if ! "$PYTHON_VENV_EXECUTABLE" -m pip install \
        -r "$PYTHON_REQUIREMENTS_FILE"; then
        printf "Failed to install Python requirements. Exiting.\n"
        return 1
    fi

    printf "Python requirements installed from %s.\n\n" "$PYTHON_REQUIREMENTS_FILE"

    return 0
}

final_touches() {
    printf "The DashAR System development tools are now ready for use. Happy coding!\n\n"
}

main() {

    # Show the splash message.
    splash_message

    # Parse the script arguments.
    parse_arguments "$@" || exit 1

    # Locate the project root. If found, proceed. Otherwise, quit.
    find_dashar_project_root || exit 1
    define_paths_and_files

    # Setup Python environment.
    clean_python_virtual_environment || exit 1
    setup_python_virtual_environment || exit 1
    install_python_requirements || exit 1

    # Wrap it up.
    final_touches
}

main "$@"
