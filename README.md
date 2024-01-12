# yt-dont-lock-p

Plugin to apply a wake lock during [`yt-dlp`](<https://github.com/yt-dlp/yt-dlp>) execution using [`wakepy`](<https://github.com/fohrloop/wakepy>), thereby solving [yt-dlp/yt-dlp#8935](<https://github.com/yt-dlp/yt-dlp/issues/8935>) in a way that is non intrusive to the core project.

See [yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#plugins) for more details on plugins.
Note that this is neither a `postprocessor` nor an `extractor` plugin, but only uses the infrastructure to apply the wakelock code.

## Installation

Requires yt-dlp `2023.01.02` or higher.

You can download `yt-dont-lock-p.zip` from the [latest release](<https://github.com/Grub4K/yt-dont-lock-p/releases/latest>) and place the zip file in a [supported plugin directory](<https://github.com/yt-dlp/yt-dlp#installing-plugins>).

Alternatively, you can install this package with `pip` (if available):
```
python -m pip install -U https://github.com/Grub4K/yt-dont-lock-p/archive/main.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## FAQ

> Why in the world this name?

A well thought through combination of `yt-dlp` and "don't lock": **yt-_d_**_ont_-_**l**ock_-_**p**_

> Were there no less cringe options?

No. In fact, here are some even more cringe ones: `its-not-dead-jim`, `grubbing-coffee`, `attention-grubber`
