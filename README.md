# Phoebus Testing

A repo to demonstrate the capabilities of [CSS phoebus](https://github.com/ControlSystemStudio/phoebus) and [PVI](https://github.com/epics-containers/pvi).

To run the ioc install and source the python venv and then run

```
    run-ioc
```

This will regenerate pvi files in `bobfiles/pvi`.

To include the classes defined in `classes_testing` run phobus with `our_phoebus.sh`. This will will require a `phoebus.sh` in the path (i.e `module load phobus` on a DLS machine). You will also need to modify `settings.ini` to include an absolute path to the file.
