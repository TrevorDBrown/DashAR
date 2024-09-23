function Execute-Main {
    $STARTING_PATH=$PWD
    $MYPY_CONFIG_FILE="$STARTING_PATH\mypy.ini"
    cd ../../Source/
    $SOURCE_PATH=$PWD

    $DAS_PATH="$SOURCE_PATH\DAS\"
    $DAS_SERVICE_FILE="$DAS_PATH\das_service.py"

    mypy --config-file $MYPY_CONFIG_FILE $DAS_SERVICE_FILE

    cd $STARTING_PATH
}

Execute-Main
Write-Host "Done!"