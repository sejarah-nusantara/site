# Translations

The repository contains a number of `.po` files that contain translations of phrases

These are in:

    project/locale
    apps/dasa/locale

You can change these files using an editor called `poedit`    

## (re)generating the `.po` files

If new words to be translated have been added to the code, the `.po` files need to be regenerated with the following commend:

    $  cd apps/dasa && ../../bin/django makemessages -l id

## compiling the files

    $  cd apps/dasa && ../../bin/django compilemessages
