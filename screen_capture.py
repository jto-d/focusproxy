import argparse
import os
import time
from datetime import datetime
from typing import Optional, Dict

import mss
from PIL import Image
from io import BytesIO

def parse_args():
    p = argparse.ArgumentParser(
        description="Capture screenshots (full screen, monitor, or region) using mss."
    )
    group = p.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true",
                       help="Capture each monitor separately on every shot.")
    group.add_argument("--monitor", type=int, default=None,
                       help="Monitor index to capture (1-based, as listed by mss).")

    p.add_argument("--region", type=int, nargs=4, metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
                   help="Capture a specific region in screen coordinates.")
    p.add_argument("--interval", type=float, default=None,
                   help="Seconds between captures. If omitted, capture once and exit.")
    p.add_argument("--count", type=int, default=1,
                   help="Number of captures to take (with interval). Use 0 for infinite until Ctrl+C.")
    p.add_argument("--outdir", type=str, default="screenshots",
                   help="Output directory.")
    p.add_argument("--format", choices=["png", "jpg", "jpeg"], default="png",
                   help="Image format. Use jpg/jpeg to control quality.")
    p.add_argument("--quality", type=int, default=90,
                   help="JPEG quality (1-95) when --format=jpg/jpeg.")
    p.add_argument("--prefix", type=str, default="shot",
                   help="Filename prefix.")
    p.add_argument("--list", action="store_true",
                   help="List detected monitors and exit.")
    return p.parse_args()


def ensure_outdir(path: str):
    os.makedirs(path, exist_ok=True)


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def build_region_dict(left: int, top: int, width: int, height: int) -> Dict[str, int]:
    return {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}


def save_png(raw_bytes: bytes, out_path: str):
    # mss gives BGRA; Pillow can open via BytesIO
    img = Image.open(BytesIO(raw_bytes))
    img.save(out_path, format="PNG")


def save_jpg(raw_bytes: bytes, out_path: str, quality: int):
    img = Image.open(BytesIO(raw_bytes)).convert("RGB")
    img.save(out_path, format="JPEG", quality=quality, optimize=True)


def capture_once(
    sct: mss.mss,
    outdir: str,
    fmt: str,
    quality: int,
    prefix: str,
    monitor_index: Optional[int] = None,
    region: Optional[Dict[str, int]] = None,
    capture_all: bool = False,
) -> None:
    ts = timestamp()

    if region:
        shot = sct.grab(region)
        raw = mss.tools.to_png(shot.rgb, shot.size)  # consistent bytes for Pillow open
        path = os.path.join(outdir, f"{prefix}_region_{ts}.{fmt}")
        if fmt == "png":
            save_png(raw, path)
        else:
            save_jpg(raw, path, quality)
        print(f"Saved {path}")
        return

    if capture_all:
        # monitors[1:] are per-monitor boxes; monitors[0] is the virtual bounding box
        for idx, mon in enumerate(sct.monitors[1:], start=1):
            shot = sct.grab(mon)
            raw = mss.tools.to_png(shot.rgb, shot.size)
            path = os.path.join(outdir, f"{prefix}_m{idx}_{ts}.{fmt}")
            if fmt == "png":
                save_png(raw, path)
            else:
                save_jpg(raw, path, quality)
            print(f"Saved {path}")
        return

    # single monitor or virtual full
    if monitor_index is None:
        # monitors[0] is the virtual full desktop across monitors
        mon = sct.monitors[0]
        label = "full"
    else:
        if monitor_index < 1 or monitor_index >= len(sct.monitors):
            raise ValueError(f"Monitor index {monitor_index} out of range. "
                             f"Valid: 1..{len(sct.monitors)-1}")
        mon = sct.monitors[monitor_index]
        label = f"m{monitor_index}"

    shot = sct.grab(mon)
    raw = mss.tools.to_png(shot.rgb, shot.size)
    path = os.path.join(outdir, f"{prefix}_{label}_{ts}.{fmt}")
    if fmt == "png":
        save_png(raw, path)
    else:
        save_jpg(raw, path, quality)
    print(f"Saved {path}")


def list_monitors(sct: mss.mss):
    print("Detected monitors (mss coordinates):")
    print("Index | left top width height")
    for i, mon in enumerate(sct.monitors):
        # mss.monitors[0] is the virtual bounding box
        label = "VIRTUAL-ALL" if i == 0 else f"{i}"
        print(f"{label:11} {mon['left']:4d} {mon['top']:4d} {mon['width']:5d} {mon['height']:5d}")


def main():
    args = parse_args()
    ensure_outdir(args.outdir)

    fmt = "jpg" if args.format in ("jpg", "jpeg") else "png"
    if fmt == "jpg" and not (1 <= args.quality <= 95):
        raise ValueError("--quality must be in [1, 95] for JPEG")

    with mss.mss() as sct:
        if args.list:
            list_monitors(sct)
            return

        # If interval is not provided, capture once and exit.
        if args.interval is None:
            capture_once(
                sct,
                outdir=args.outdir,
                fmt=fmt,
                quality=args.quality,
                prefix=args.prefix,
                monitor_index=args.monitor,
                region=(build_region_dict(*args.region) if args.region else None),
                capture_all=args.all,
            )
            return

        # Timed loop
        shots_taken = 0
        print("Starting timed capture. Press Ctrl+C to stop.")
        try:
            while True:
                capture_once(
                    sct,
                    outdir=args.outdir,
                    fmt=fmt,
                    quality=args.quality,
                    prefix=args.prefix,
                    monitor_index=args.monitor,
                    region=(build_region_dict(*args.region) if args.region else None),
                    capture_all=args.all,
                )
                shots_taken += 1
                if args.count > 0 and shots_taken >= args.count:
                    break
                time.sleep(max(0.0, args.interval))
        except KeyboardInterrupt:
            print("\nStopped by user.")

if __name__ == "__main__":
    main()