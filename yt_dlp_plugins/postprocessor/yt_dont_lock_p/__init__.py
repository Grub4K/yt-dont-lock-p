from __future__ import annotations

import contextlib
import functools

import yt_dlp

from yt_dlp_plugins.postprocessor.yt_dont_lock_p._version import __version__

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import ParamSpec

    P = ParamSpec("P")


NAME = "yt-dont-lock-p"
LOCK_ATTR_NAME = f"__{NAME}_lock"


def lock_enter(self: yt_dlp.YoutubeDL, /):
    try:
        from wakepy import keep

    except ImportError:
        import sys
        from pathlib import Path

        # Try importing from zip file bundle
        search_path = str(Path(__file__).parent.parent.parent)
        sys.path.append(search_path)

        try:
            import jeepney  # noqa: F401 Import to add to sys.modules with modified sys.path
            from wakepy import keep

        except ImportError:
            self.report_warning(f"{NAME}: Could not find wakepy")
            return

        except Exception:
            self.report_error(f"{NAME}: Error importing wakepy")
            return

        finally:
            sys.path.remove(search_path)

    try:
        lock = keep.running(on_fail="error").__enter__()
    except Exception as error:
        self.report_warning(f"{NAME}: Could not acquire wakelock: {error}")
    else:
        self.write_debug(f"{NAME}: Acquired wakelock")
        setattr(self, LOCK_ATTR_NAME, lock)


def lock_exit(self: yt_dlp.YoutubeDL, /, *args):
    if lock := getattr(self, LOCK_ATTR_NAME, None):
        self.write_debug(f"{NAME}: Released wakelock")
        lock.__exit__(*args)


def print_version(self: yt_dlp.YoutubeDL, /):
    self.write_debug(f"{NAME} version: {__version__}")


def inject(
    cls: type,
    func: Callable[P],
    before: Callable[P] | None = None,
    after: Callable[P] | None = None,
):
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        if before:
            with contextlib.suppress(Exception):
                before(*args, **kwargs)
        result = func(*args, **kwargs)
        if after:
            with contextlib.suppress(Exception):
                after(*args, **kwargs)
        return result

    setattr(cls, func.__name__, functools.wraps(func)(wrapper))


inject(yt_dlp.YoutubeDL, yt_dlp.YoutubeDL.print_debug_header, after=print_version)
inject(yt_dlp.YoutubeDL, yt_dlp.YoutubeDL.__enter__, before=lock_enter)
inject(yt_dlp.YoutubeDL, yt_dlp.YoutubeDL.__exit__, before=lock_exit)
