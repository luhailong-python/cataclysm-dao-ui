"""Index frozen art-only deliverables. Reads and writes only inside this E project.

The existing 108-item kit manifest is an input and is never rewritten here.
No image pixels, F-reference files, renderer or screens are modified.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "art-delivery/records"
BASE = RECORDS / "asset-manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def image_info(path: Path) -> dict:
    with Image.open(path) as image:
        image.load()
        alpha = image.getchannel("A") if "A" in image.getbands() else None
        result = {
            "size": list(image.size), "width": image.width, "height": image.height,
            "mode": image.mode, "sha256": sha(path),
            "alphaExtrema": list(alpha.getextrema()) if alpha is not None else None,
            "alphaContentBox": list(alpha.getbbox()) if alpha is not None else None,
        }
    with Image.open(path) as image:
        image.verify()
    return result


def extra_asset(asset_id: str, category: str, record_suffix: str, meaning: str) -> dict:
    file = f"art-delivery/resources/{category}/{asset_id}.png"
    path = ROOT / file
    record_path = Path(str(path) + record_suffix)
    source = read(record_path)
    info = image_info(path)
    if source["sha256"] != info["sha256"]:
        raise ValueError(f"Generation/source hash mismatch: {asset_id}")
    if category == "backgrounds":
        if info["size"] != [1672, 941] or info["mode"] != "RGB":
            raise ValueError(f"Unexpected native background: {asset_id}")
    elif info["size"] != [1024, 1536] or info["mode"] != "RGBA":
        raise ValueError(f"Unexpected native character: {asset_id}")

    source_record = record_path.relative_to(ROOT).as_posix()
    if record_suffix == ".source.json":
        derived = source["derivedFrom"]
        original = ROOT / derived["file"]
        if sha(original) != info["sha256"]:
            raise ValueError(f"Byte-for-byte source mismatch: {asset_id}")
        generation_path = ROOT / derived["generationRecord"]
        generation = read(generation_path)
        derived_from = [dict(derived)]
        relationship = "direct-reuse-within-this-project"
    else:
        generation_path = record_path
        generation = source
        derived_from = []
        relationship = "new-generated-artwork"
    if generation["sha256"] != info["sha256"]:
        raise ValueError(f"Native generation hash mismatch: {asset_id}")

    return {
        "id": asset_id, "file": file, "category": category, **info,
        "nativePixelSize": info["size"],
        "state": "normal", "stateFamily": None,
        "borderLeftBottomRightTop": [0, 0, 0, 0], "resizeAxes": "none",
        "pivot": [0.5, 0.5], "pixelsPerUnit": 100,
        "spriteType": "Simple", "spriteImportMode": "Single", "meshType": "FullRect",
        "filterMode": "Bilinear", "wrapMode": "Clamp", "mipmaps": False,
        "sRGB": True, "alphaIsTransparency": info["mode"] == "RGBA",
        "compression": "Uncompressed recommended; final platform verification pending",
        "maxTextureSize": 2048,
        "dynamicTextBaked": False, "meaning": meaning,
        "operation": source["operation"], "relationship": relationship,
        "derivedFrom": derived_from,
        "sourceRecord": source_record, "sourceRecordSha256": sha(record_path),
        "generationRecord": generation_path.relative_to(ROOT).as_posix(),
        "generationRecordSha256": sha(generation_path),
        "generatedAt": generation["generatedAt"],
        "configTarget": generation.get("configSnapshot"),
        "submittedParameters": generation.get("submittedParameters"),
        "actualModel": generation.get("actualModel"),
        "actualQuality": generation.get("actualQuality"),
        "modelQualityEvidence": generation.get("unverifiedReason"),
        "references": generation.get("references", []),
        "nativeOutputPreserved": True,
        "unityValidation": "Import recommendations only; not imported into Unity in this phase",
        "layoutAdvice": (
            "Keep native RGB background. Preserve aspect ratio; choose cover crop or contain per page. "
            "A 1920x1080 design placement enlarges the native image by about 1.148; it does not add native detail. "
            "Overlay labels/markers separately; do not nine-slice."
            if category == "backgrounds" else
            "Preserve native RGBA including soft edges. Display whole silhouette at uniform scale, "
            "with lower edge positioned by layout anchor; no nine-slice, animation frames or skeletal data supplied."
        ),
    }


def main():
    base_sha = sha(BASE)
    base = read(BASE)
    assert len(base["assets"]) == 108
    assets = list(base["assets"])
    assets.extend([
        extra_asset("entry-keyart", "backgrounds", ".source.json", "入口/加载/菜单用无字生存主题插画"),
        extra_asset("expedition-playfield", "backgrounds", ".generation.json", "探索/战斗界面用无字场景插画；不代表可玩地图数据"),
        extra_asset("regional-map", "backgrounds", ".generation.json", "区域地图美术示例；地点/路径/坐标由独立 UI 与数据层标注"),
        extra_asset("hero-survivor", "characters", ".generation.json", "道家Q版生存者静态全身立绘；不包含动画或战斗角色控制数据"),
    ])
    assert len(assets) == 112
    assert len({asset["id"] for asset in assets}) == 112
    assert len({asset["file"] for asset in assets}) == 112
    for entry in assets:
        actual = image_info(ROOT / entry["file"])
        for key in ("sha256", "size", "mode", "alphaExtrema"):
            if actual[key] != entry[key]:
                raise ValueError(f"Current resource {key} mismatch: {entry['id']}")

    source_only = []
    for file in base["sourceOnlyFiles"]:
        if not file.endswith(".png"):
            continue
        path = ROOT / file
        record_path = Path(str(path) + ".generation.json")
        entry = {"file": file, **image_info(path), "role": "sourceOnly",
                 "countAsRuntimeSprite": False,
                 "generationRecord": record_path.relative_to(ROOT).as_posix(),
                 "generationRecordSha256": sha(record_path)}
        if read(record_path)["sha256"] != entry["sha256"]:
            raise ValueError(f"Source-only master hash mismatch: {file}")
        source_only.append(entry)
    assert len(source_only) == 2
    if sha(BASE) != base_sha:
        raise ValueError("Base manifest changed during indexing")

    counts = dict(Counter(asset["category"] for asset in assets))
    validation = {
        "formalIndependentSpriteCount": len(assets), "countsByCategory": counts,
        "sourceOnlyMasterImageCount": len(source_only), "sourceOnlyIncludedInSpriteCount": False,
        "all112PngsDecoded": True, "all112CurrentHashesMatchRecords": True,
        "newFourNativeDimensionsAndModesMatch": True,
        "baseManifest108PreservedByteForByte": True, "unityImportExecuted": False,
        "validationScope": "File/spec verification only; visual screen QA is recorded separately.",
    }
    manifest = {
        "schemaVersion": 1, "task": base["task"],
        "createdAt": datetime.now(timezone.utc).isoformat(), "phase": base["phase"],
        "designResolution": base["designResolution"],
        "functionalReference": base["functionalReference"],
        "functionalReferenceCommit": "eb86dffd20072d6fde54af568cf229f3cd4d751f",
        "artReferenceRepository": base["artReferenceRepository"],
        "artReferenceRemote": base["artReferenceRemote"],
        "resultRepository": base["resultRepository"],
        "associationRecord": "docs/image-reference-associations.md",
        "baseKitManifest": {"file": BASE.relative_to(ROOT).as_posix(), "sha256": base_sha,
                            "assetCount": 108, "existingEntriesCopiedWithoutModification": True},
        "formalIndependentSpriteCount": 112, "sourceOnlyMasterImageCount": 2,
        "sourceOnly": source_only, "font": base["font"],
        "otherFilesNotCountedAsSprites": "Font/license, JSON/CSV/Markdown records, source-only masters, previews and full-screen design composites.",
        "assets": assets, "validation": validation,
    }
    (RECORDS / "complete-resource-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RECORDS / "complete-resource-validation.json").write_text(
        json.dumps({"createdAt": manifest["createdAt"], "baseKitManifestSha256": base_sha,
                    **validation, "inputPixelHashes": {a["id"]: a["sha256"] for a in assets}},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (RECORDS / "unity-import-complete.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "file", "width", "height", "state", "stateFamily", "SpriteMode", "SpriteType",
                         "BorderLeft", "BorderBottom", "BorderRight", "BorderTop", "PivotX", "PivotY", "PPU",
                         "resizeAxes", "sha256", "category", "mode", "alphaIsTransparency", "MaxSize",
                         "Filter", "Wrap", "MipMaps", "sRGB", "sourceRecord", "unityValidation"])
        for entry in assets:
            max_size = 32
            while max_size < max(entry["size"]):
                max_size *= 2
            writer.writerow([entry["id"], entry["file"], entry["width"], entry["height"], entry["state"],
                             entry.get("stateFamily"), entry.get("spriteImportMode", "Single"), entry["spriteType"],
                             *entry["borderLeftBottomRightTop"], *entry["pivot"], entry["pixelsPerUnit"],
                             entry["resizeAxes"], entry["sha256"], entry["category"], entry["mode"],
                             entry.get("alphaIsTransparency", entry["mode"] == "RGBA"), max_size,
                             entry["filterMode"], entry["wrapMode"], entry["mipmaps"], entry["sRGB"],
                             entry.get("sourceRecord", "art-delivery/records/asset-manifest.json"),
                             entry["unityValidation"]])
    assert sha(BASE) == base_sha
    print(json.dumps(validation, ensure_ascii=False))


if __name__ == "__main__":
    main()
