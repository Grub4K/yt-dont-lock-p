from __future__ import annotations

try:
    from wakepy import keep

except ImportError:
    import sys
    from pathlib import Path

    # Try importing from zip file bundle
    search_path = str(Path(__file__).parent.parent)
    sys.path.append(search_path)

    try:
        from wakepy import keep

    except ImportError:
        print("[yt-dont-lock-p] Could not find wakepy", file=sys.stderr)
        keep = None

    except Exception as error:
        raise error from None

    finally:
        sys.path.remove(search_path)


if keep:
    lock = keep.running()
    if lock.__enter__().success:
        import atexit

        atexit.register(lock.__exit__, None, None, None)

    else:
        print("[yt-dont-lock-p] Could not acquire wakelock", file=sys.stderr)
        lock.__exit__(None, None, None)
