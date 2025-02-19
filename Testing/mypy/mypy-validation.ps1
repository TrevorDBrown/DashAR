function Execute-Main {
    $STARTING_PATH=$PWD
    $MYPY_CONFIG_FILE="$STARTING_PATH\mypy.ini"
    cd ../../Source/
    $SOURCE_PATH=$PWD

    $DAS_PATH="$SOURCE_PATH\DAS\"

    mypy --config-file $MYPY_CONFIG_FILE $DAS_PATH

    cd $STARTING_PATH
}

Execute-Main
Write-Host "Done!"