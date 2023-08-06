# Nautobot deep copy

enables you to copy a device along with all of its components. The asset tag
and position information (rack and virtual chassis) will remain empty by default, the
name will need to be changed (as soon as you migrate the tenant or site, you
will be allowed to change the name back as long as there are no collisions). All information in the deep copy form will be used to replace the equivalent fields in the target device.

## Integration

To integrate the plugin, you will have to provide add it to your `PLUGINS`
configuration to your `configuration.py`:

```
PLUGINS = [
  "nautobot_deepcopy",
  # my other plugins
]
```

The [Nautobot plugins guide](https://nautobot.readthedocs.io/en/stable/plugins/development/#initial-setup)
should help you get started!

Please note that this plugin uses internal Nautobot components, which is
explicitly discouraged by the documentation. We promise to keep the plugin up
to date, but the latest version might break on unsupported Nautobot versions.
Your mileage may vary.

<hr/>

Have fun!
