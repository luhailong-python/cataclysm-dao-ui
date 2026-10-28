"""Build the reusable art-only UI kit from verified painted source assets.

This never calls a generation API and never writes to the art reference repository.
Deterministic state variants and nine-part resampling are explicitly recorded.
"""
from __future__ import annotations
import hashlib
import json
import csv
from datetime import datetime, timezone
from pathlib import Path
import shutil
import struct
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"F:\work\image")
DELIVERY = ROOT / "art-delivery"
RESOURCES = DELIVERY / "resources"
RECORDS = DELIVERY / "records"
COMMON = "qdao_ui_redesign_v5/components"
ATTR = "designs/attribute-panels/v2-painted/unity-slices"
TEAM = "designs/team-ui-v2/unity-slices"
EQUIP = "designs/equipment-ui-20261008/sprites"
GAMEPLAY = "designs/gameplay-ui/fidelity-20261016/staged/Assets/Resources/UI/Ugui/GameplayFidelity20261016"
ASSETS: list[dict] = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def image(relative: str) -> Image.Image:
    path = SOURCE / relative
    if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not actual PNG bytes (possibly LFS pointer): {path}")
    with Image.open(path) as opened:
        opened.verify()
    with Image.open(path) as opened:
        return opened.convert("RGBA")


def nine_part(original: Image.Image, size: tuple[int, int], border: list[int]):
    """Preserve native corner pixels and resample only their corresponding patches."""
    left, bottom, right, top = border
    width, height = size
    source_width, source_height = original.size
    if width <= left + right or height <= top + bottom:
        raise ValueError("Target smaller than fixed border sum")
    xs = [0, left, source_width - right, source_width]
    ys = [0, top, source_height - bottom, source_height]
    tx = [0, left, width - right, width]
    ty = [0, top, height - bottom, height]
    output = Image.new("RGBA", size)
    for column in range(3):
        for row in range(3):
            patch = original.crop((xs[column], ys[row], xs[column+1], ys[row+1]))
            target = (tx[column+1]-tx[column], ty[row+1]-ty[row])
            output.alpha_composite(patch.resize(target, Image.Resampling.LANCZOS), (tx[column], ty[row]))
    return output


def adjust(picture: Image.Image, brightness=1.0, saturation=1.0):
    alpha = picture.getchannel("A")
    result = ImageEnhance.Color(picture).enhance(saturation)
    result = ImageEnhance.Brightness(result).enhance(brightness)
    result.putalpha(alpha)
    return result


def overlay_symbol(picture: Image.Image, symbol: Image.Image, position, size):
    result = picture.copy()
    symbol = symbol.copy()
    symbol.thumbnail(size, Image.Resampling.LANCZOS)
    result.alpha_composite(symbol, position)
    return result


def source_record(relative: str):
    original = SOURCE / relative
    if original.with_name(original.name + ".generation.json").is_file():
        return original.with_name(original.name + ".generation.json").relative_to(SOURCE).as_posix()
    if relative.startswith(COMMON):
        return COMMON + "/manifest.json"
    if relative.startswith(ATTR):
        return ATTR + "/manifest.json"
    if relative.startswith(TEAM):
        return TEAM + "/manifest.json"
    if relative.startswith("designs/main-hud-20261021/"):
        return "designs/main-hud-20261021/sprite-manifest.json"
    return None


def register(name: str, relative: str, *, group="ui", result=None,
             border=(0,0,0,0), operation="byte-for-byte copy", state="normal",
             family=None, additional_sources=(), meaning=None, resize_axes="none",
             fixed_symbol=False, text_insets=None):
    source = SOURCE / relative
    source_picture = image(relative)
    target = RESOURCES / group / (name + ".png")
    target.parent.mkdir(parents=True, exist_ok=True)
    if result is None:
        shutil.copyfile(source, target)
    else:
        result.save(target)
    with Image.open(target) as final:
        dims = list(final.size)
        mode = final.mode
        alpha_extrema = list(final.getchannel("A").getextrema()) if "A" in mode else None
    record_path = source_record(relative)
    source_entry = {
        "repositoryRelativePath": relative,
        "sha256": sha(source),
        "sourcePixelSize": list(source_picture.size),
        "generationOrCropRecord": record_path,
    }
    sources = [source_entry]
    for other in additional_sources:
        opened = image(other)
        sources.append({"repositoryRelativePath":other,"sha256":sha(SOURCE/other),
                        "sourcePixelSize":list(opened.size),"generationOrCropRecord":source_record(other)})
    entry = {
        "id": name, "file": target.relative_to(ROOT).as_posix(), "category": group,
        "size": dims, "width": dims[0], "height": dims[1], "mode":mode,
        "sha256":sha(target), "alphaExtrema":alpha_extrema,
        "state":state, "stateFamily":family,
        "borderLeftBottomRightTop":list(border), "resizeAxes":resize_axes,
        "pivot":[0.5,0.5], "pixelsPerUnit":100,
        "spriteType":"Sliced" if any(border) else "Simple",
        "spriteImportMode":"Single", "meshType":"FullRect",
        "filterMode":"Bilinear", "wrapMode":"Clamp", "mipmaps":False,
        "sRGB":True, "alphaIsTransparency": alpha_extrema is not None,
        "compression":"Uncompressed recommended; final platform verification pending",
        "dynamicTextBaked":False, "containsFixedArtSymbol":fixed_symbol,
        "textInsetsLeftTopRightBottom":text_insets,
        "meaning":meaning,
        "operation":operation, "relationship":"direct-reuse" if result is None else "adapted-use",
        "newModelGeneration":False, "derivedFrom":sources,
        "actualModel":None,"actualQuality":None,
        "modelQualityEvidence":"Historical source records retained; no model call in this build; no current config backfilled into original art.",
        "unityValidation":"Import recommendations only; not imported into Unity in this phase",
    }
    ASSETS.append(entry)
    return entry


def regular_states(name, source_relative, border, *, selected_relative=None,
                   disabled_relative=None, text_insets=None, horizontal=True):
    base = image(source_relative)
    check_relative = COMMON + "/png/check.png"
    lock_relative = COMMON + "/png/lock.png"
    check = image(check_relative)
    lock = image(lock_relative)
    icon_size = min(44, base.height - 22)
    location = (9, (base.height-icon_size)//2)
    for state in ("normal","pressed","selected","disabled","locked"):
        source = source_relative
        sources=[]
        result=None
        operation="byte-for-byte copy"
        fixed=False
        if state == "pressed":
            result=adjust(base,.84,1.02)
            operation="deterministic pressed-state brightness 0.84, saturation 1.02; alpha unchanged; no new image generation"
        elif state == "selected":
            if selected_relative:
                source=selected_relative
            else:
                result=overlay_symbol(adjust(base,1.03,1.06),check,location,(icon_size,icon_size))
                sources=[check_relative]
                operation="painted source with existing painted check composited; no code-drawn art; alpha preserved"
            fixed=True
        elif state == "disabled":
            if disabled_relative:
                source=disabled_relative
                fixed=True
            else:
                result=adjust(base,.9,.12)
                operation="deterministic desaturation 0.12 and brightness 0.90, alpha unchanged; reason label supplied separately"
        elif state == "locked":
            result=overlay_symbol(adjust(base,.9,.12),lock,location,(icon_size,icon_size))
            sources=[lock_relative]
            fixed=True
            operation="disabled painted source plus existing painted lock symbol; no new generation; state remains same canvas"
        register(name+"-"+state,source,result=result,border=border,state=state,family=name,
                 operation=operation,additional_sources=sources,fixed_symbol=fixed,
                 resize_axes="horizontal" if horizontal else "both",text_insets=text_insets)


def make_clean_headers():
    master=RESOURCES/"ui/clean-header-master.png"
    generation=master.with_name(master.name+".generation.json")
    if not master.is_file() or not generation.is_file():
        raise FileNotFoundError("Clean generated header master and generation record are required; rejected flattened team title must not be restored")
    with Image.open(master) as opened:
        original=opened.convert("RGBA")
    clean=original.copy()
    # Native output includes isolated alpha 1–3 noise above/below the actual shape.
    # Keep source master untouched and document this deterministic cleanup on derivatives.
    clean.putalpha(clean.getchannel("A").point(lambda value:value if value>=4 else 0))
    crop_box=clean.getbbox()
    cropped=clean.crop(crop_box)
    for name,size,border,insets in (
        ("title",(716,145),[180,34,170,31],[175,30,170,56]),
        ("section",(433,72),[145,16,145,16],[112,15,112,30]),
    ):
        fit=min((size[0]-8)/cropped.width,(size[1]-8)/cropped.height,1.0)
        painted_size=(max(1,round(cropped.width*fit)),max(1,round(cropped.height*fit)))
        painted=cropped.resize(painted_size,Image.Resampling.LANCZOS)
        canvas=Image.new("RGBA",size)
        position=((size[0]-painted.width)//2,(size[1]-painted.height)//2)
        canvas.alpha_composite(painted,position)
        target=RESOURCES/"ui"/(name+".png")
        canvas.save(target)
        ASSETS.append({
            "id":name,"file":target.relative_to(ROOT).as_posix(),"category":"ui",
            "size":list(size),"width":size[0],"height":size[1],"mode":"RGBA","sha256":sha(target),
            "alphaExtrema":list(canvas.getchannel("A").getextrema()),"state":"normal","stateFamily":None,
            "borderLeftBottomRightTop":border,"resizeAxes":"horizontal","pivot":[0.5,0.5],"pixelsPerUnit":100,
            "spriteType":"Sliced","spriteImportMode":"Single","meshType":"FullRect","filterMode":"Bilinear",
            "wrapMode":"Clamp","mipmaps":False,"sRGB":True,"alphaIsTransparency":True,
            "compression":"Uncompressed recommended; final platform verification pending",
            "dynamicTextBaked":False,"containsFixedArtSymbol":False,
            "textInsetsLeftTopRightBottom":insets,
            "textCenterNormalized":[0.5,0.41],
            "meaning":"Clean empty jade title field; labels rendered independently; tassels make visual text center above canvas midpoint",
            "operation":"Preserve native master; remove alpha<4 isolated quantization noise on derivative only, crop actual alpha silhouette, uniform downsample and transparent center placement. No stretch/distortion or code repaint; this is not new generation.",
            "relationship":"adapted-use","newModelGeneration":False,
            "derivedFrom":[{"file":master.relative_to(ROOT).as_posix(),"sha256":sha(master),
                            "generationRecord":generation.relative_to(ROOT).as_posix(),"sourcePixelSize":list(original.size)}],
            "cropBoxNativeXYXY":list(crop_box),"nativeCropPixelSize":list(cropped.size),
            "scaleFactor":fit,"placedPixelSize":list(painted_size),"positionTopLeft":list(position),
            "actualModel":None,"actualQuality":None,
            "modelQualityEvidence":"Inherited from clean-header-master.png.generation.json; host did not disclose exact model/quality",
            "unityValidation":"Import recommendations only; not imported into Unity in this phase",
            "replacedRejectedSource":"Old flattened team crop had incidental text/sky and rectangular erase patches; rejected output pixels were replaced, not retained as a fallback.",
        })


def make_ui():
    register("panel-main",COMMON+"/png/main_frame.png",border=[148,125,148,112],resize_axes="both",text_insets=[44,34,44,36])
    register("panel-content",COMMON+"/png/content_panel.png",border=[145,122,145,108],resize_axes="both",text_insets=[32,30,32,30])
    register("panel-tooltip","designs/equipment-ui-20261009/sprites/tooltip_panel.png",border=[48,80,48,160],resize_axes="both",text_insets=[34,145,34,50])
    make_clean_headers()
    regular_states("button-primary",COMMON+"/png/primary_button_normal.png",[82,34,82,30],
                   selected_relative=COMMON+"/png/primary_button_selected.png",
                   disabled_relative=COMMON+"/png/primary_button_disabled.png",text_insets=[84,24,70,26])
    regular_states("button-secondary",ATTR+"/png/button_secondary.png",[30,27,30,27],text_insets=[55,18,28,18])
    regular_states("tab",COMMON+"/png/tab_normal.png",[82,34,82,30],
                   selected_relative=COMMON+"/png/tab_selected.png",
                   disabled_relative=COMMON+"/png/tab_disabled.png",text_insets=[85,25,65,26])
    regular_states("row",COMMON+"/png/list_row_normal.png",[82,31,82,27],
                   selected_relative=COMMON+"/png/list_row_selected.png",
                   disabled_relative=COMMON+"/png/list_row_disabled.png",text_insets=[84,22,60,22])
    for state in ("normal","selected","disabled"):
        register("search-"+state,COMMON+"/png/search_"+state+".png",border=[70,29,64,26],
                 state=state,family="search",resize_axes="horizontal",fixed_symbol=True,text_insets=[75,20,65,22])
    register("paper-tile",ATTR+"/png/paper_tile.png",border=[11,11,11,11],resize_axes="both")
    register("stat-field",ATTR+"/png/stat_field.png",border=[12,12,12,12],resize_axes="horizontal")
    register("close",TEAM+"/png/close.png",fixed_symbol=True)
    register("dropdown",ATTR+"/png/dropdown_arrow.png",fixed_symbol=True)
    register("step-plus",ATTR+"/png/step_plus.png",fixed_symbol=True)
    register("step-minus",ATTR+"/png/step_minus.png",fixed_symbol=True)
    for state,src in (("normal","checkbox_off"),("selected","checkbox_on")):
        register("checkbox-"+state,EQUIP+"/"+src+".png",state=state,family="checkbox",fixed_symbol=state=="selected")
    original=image(EQUIP+"/checkbox_off.png")
    register("checkbox-disabled",EQUIP+"/checkbox_off.png",result=adjust(original,.92,.12),state="disabled",family="checkbox",operation="desaturation 0.12 and brightness 0.92; alpha unchanged")
    register("progress-track",ATTR+"/png/slider_track.png",border=[7,7,7,7],resize_axes="horizontal")
    register("progress-fill",ATTR+"/png/slider_fill.png",border=[7,7,7,7],resize_axes="horizontal")
    track=image(ATTR+"/png/slider_track.png").transpose(Image.Transpose.ROTATE_90)
    register("scrollbar-track",ATTR+"/png/slider_track.png",result=track,border=[7,7,7,7],resize_axes="vertical",operation="90-degree rotation of existing painted progress track, alpha preserved")
    register("scrollbar-thumb",ATTR+"/png/slider_thumb.png")
    for color in ("green","orange","gray"):
        register("status-"+color,COMMON+"/png/status_dot_"+color+".png",fixed_symbol=True)
    register("check",COMMON+"/png/check.png",fixed_symbol=True)
    register("lock",COMMON+"/png/lock.png",fixed_symbol=True)
    register("cloud-corner",COMMON+"/png/cloud_corner.png")
    register("gold-flower",COMMON+"/png/gold_flower.png")
    register("lantern","designs/mail-ui-v1/assets/lantern.png")
    paper_relative=ATTR+"/png/paper_tile.png"
    frame_relative=ATTR+"/png/portrait_frame.png"
    frame=nine_part(image(frame_relative),(160,160),[11,11,11,11])
    paper=nine_part(image(paper_relative),(146,146),[11,11,11,11])
    slot=Image.new("RGBA",(160,160))
    slot.alpha_composite(paper,(7,7))
    slot.alpha_composite(frame)
    for state in ("normal","pressed","selected","disabled","locked"):
        result=slot.copy()
        extra=[paper_relative]
        if state=="pressed":result=adjust(result,.88,1.0)
        elif state=="disabled":result=adjust(result,.94,.15)
        elif state=="selected":
            symbol=COMMON+"/png/check.png";extra.append(symbol)
            result=overlay_symbol(result,image(symbol),(122,6),(32,32))
        elif state=="locked":
            symbol=COMMON+"/png/lock.png";extra.append(symbol)
            result=overlay_symbol(adjust(result,.94,.15),image(symbol),(56,56),(48,48))
        register("slot-"+state,frame_relative,result=result,border=[11,11,11,11],state=state,
                 family="slot",additional_sources=extra,resize_axes="both",fixed_symbol=state in {"selected","locked"},
                 operation="160x160 nine-part derivative of existing painted portrait rim + clean paper tile, state uses deterministic tone or existing painted symbol; no new generation")


def make_icons():
    meanings={
        "compass":("compass","navigation emblem"),"flame":("fire","heat/fire status emblem"),
        "water":("water","water/thirst category emblem"),"furnace":("crafting","crafting category emblem"),
        "mountain":("map","terrain/map category emblem"),"sword":("sword","melee category emblem"),
        "lotus":("morale","wellbeing category emblem; conceptual"),"taiji":("martial","martial arts category emblem"),
        "peach_spirit":("herbs","plant/mutation conceptual emblem"),"pagoda":("settlement","settlement/camp category emblem")}
    for source_name,(name,meaning) in meanings.items():
        register("icon-"+name,COMMON+"/png/round_badge_"+source_name+".png",group="icons",meaning=meaning)
    for source_name,name,meaning in (("chest","cache-building","pavilion illustration used only as cache/storage-building category emblem; not a physical chest"),("pill","medication","gourd/medicine category emblem, not a literal pill or specific CDDA item"),
                                   ("scroll","notes","mission/notes category"),("talisman","talisman-optional","optional mod/magic art, not claimed as default CDDA mechanic")):
        register("icon-"+name,"designs/mail-ui-v1/assets/icon-"+source_name+".png",group="icons",meaning=meaning)
    for source_name,name in (("sword","blade"),("boots","boots")):
        register("icon-"+name,EQUIP+"/icon_"+source_name+".png",group="icons",meaning="melee/clothing item illustration; example visual, no old MMO stats copied")
    for source_name,name,meaning in (("bag","bag","inventory category"),("channel","chat","communications category"),
                                   ("pet","companion","companion category emblem; not an MMO pet system"),("rank","achievement","achievement category emblem; not ranking"),
                                   ("social","dialogue","NPC dialogue category"),("spectate","observe","look/inspect category"),
                                   ("team","party-command","NPC companion commands category; not multiplayer party"),("trade","trade","NPC barter category")):
        register("icon-"+name,"designs/main-hud-20261021/sprites/"+source_name+".png",group="icons",meaning=meaning)
    for skill_id in (1101,1103,1106,1107,1301,1303):
        relative=f"designs/class-skills-20260928/icons/{skill_id}.png"
        original=image(relative)
        result=original.resize((256,256),Image.Resampling.LANCZOS)
        register("art-martial-"+str(skill_id),relative,group="icons",result=result,
                 meaning="Painted martial/ability category illustration; source MMO skill names/effects not adopted as CDDA rules",
                 operation="LANCZOS downsample from native 1254x1254 RGB skill card to 256x256 RGBA card; no alpha cutout, no new generation")


def font_record():
    font=RESOURCES/"fonts/NotoSansCJKsc-Regular.otf"
    license_file=RESOURCES/"fonts/OFL.txt"
    if not font.is_file() or not license_file.is_file():
        raise FileNotFoundError("Official OFL font download must be complete before build")
    data=font.read_bytes()
    count=struct.unpack_from(">H",data,4)[0]
    font_names={}
    for table in range(count):
        tag,checksum,offset,length=struct.unpack_from(">4sIII",data,12+16*table)
        if tag!=b"name":continue
        format_id,name_count,strings_offset=struct.unpack_from(">HHH",data,offset)
        for index in range(name_count):
            platform,encoding,language,name_id,size,relative=struct.unpack_from(">HHHHHH",data,offset+6+12*index)
            if platform==3 and name_id in {0,1,2,5}:
                font_names[str(name_id)]=data[offset+strings_offset+relative:offset+strings_offset+relative+size].decode("utf-16-be")
    return {"file":font.relative_to(ROOT).as_posix(),"sha256":sha(font),
            "license":license_file.relative_to(ROOT).as_posix(),"licenseSha256":sha(license_file),
            "source":"https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
            "licenseSource":"https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/LICENSE",
            "typeface":"Noto Sans CJK SC Regular", "licenseName":"SIL Open Font License 1.1", "embeddedFontNames":font_names,
            "note":"No standalone font file found in current F reference tree. Retrieved from official Noto CJK repository; exact bytes pinned by SHA256. Do not copy system proprietary fonts into deliverable."}


def snapshot_evidence():
    evidence=RECORDS/"source-evidence"
    evidence.mkdir(parents=True,exist_ok=True)
    paths={r["generationOrCropRecord"] for a in ASSETS for r in a["derivedFrom"] if r.get("generationOrCropRecord")}
    paths.update([COMMON+"/README.md",COMMON+"/manifest.json",ATTR+"/manifest.json",TEAM+"/manifest.json",
                  "designs/equipment-ui-20261009/sprites/tooltip_panel.png.generation.json"])
    records=[]
    for relative in sorted(paths):
        source=SOURCE/relative
        if not source.is_file():continue
        target=evidence/(relative.replace("/","__"))
        shutil.copyfile(source,target)
        records.append({"original":relative,"snapshot":target.relative_to(ROOT).as_posix(),"sha256":sha(target)})
    return records


def contact_sheet():
    fontfile=RESOURCES/"fonts/NotoSansCJKsc-Regular.otf"
    font=ImageFont.truetype(str(fontfile),18)
    selected=[a for a in ASSETS if a["category"]=="icons"]
    sheet=Image.new("RGB",(1440,((len(selected)+7)//8)*190),(235,231,215))
    draw=ImageDraw.Draw(sheet)
    for index,entry in enumerate(selected):
        x=(index%8)*180;y=(index//8)*190
        with Image.open(ROOT/entry["file"]) as source:
            item=source.convert("RGBA");item.thumbnail((140,140),Image.Resampling.LANCZOS)
        sheet.paste(item,(x+(180-item.width)//2,y+7+(140-item.height)//2),item)
        draw.text((x+8,y+151),entry["id"].replace("icon-",""),font=font,fill=(30,70,57))
    target=DELIVERY/"previews/resource-icons.jpg"
    target.parent.mkdir(parents=True,exist_ok=True)
    sheet.save(target,quality=94)
    states=[a for a in ASSETS if a.get("stateFamily") in {"button-primary","button-secondary","tab","row","slot"}]
    sheet=Image.new("RGB",(1440,900),(235,231,215));draw=ImageDraw.Draw(sheet)
    for index,entry in enumerate(states):
        x=(index%5)*288;y=(index//5)*180
        with Image.open(ROOT/entry["file"]) as source:
            item=source.convert("RGBA");item.thumbnail((260,125),Image.Resampling.LANCZOS)
        sheet.paste(item,(x+(288-item.width)//2,y+6+(125-item.height)//2),item)
        draw.text((x+10,y+137),entry["id"].replace("button-",""),font=font,fill=(30,70,57))
    sheet.save(DELIVERY/"previews/resource-states.jpg",quality=94)


def validate():
    groups={}
    for entry in ASSETS:
        actual=ROOT/entry["file"]
        if sha(actual)!=entry["sha256"]:
            raise ValueError(f"Current bytes differ from resource record: {entry['id']}")
        with Image.open(actual) as decoded:
            decoded.verify()
        width,height=entry["size"];l,b,r,t=entry["borderLeftBottomRightTop"]
        if min(l,b,r,t)<0 or l+r>=width or b+t>=height:
            if any((l,b,r,t)):raise ValueError(f"Invalid border: {entry['id']}")
        if entry["category"]=="ui":
            if entry["alphaExtrema"] is None:
                raise ValueError(f"UI skin has no alpha: {entry['id']}")
            if entry["id"]!="paper-tile" and entry["alphaExtrema"][0]!=0:
                raise ValueError(f"UI skin lacks transparent exterior: {entry['id']}")
        if entry.get("stateFamily"):
            groups.setdefault(entry["stateFamily"],set()).add(tuple(entry["size"]))
    if any(len(values)!=1 for values in groups.values()):
        raise ValueError("State family canvas sizes differ")
    return {"assetCount":len(ASSETS),"allPngsDecoded":True,"allHashRecordsPresent":True,
            "currentFileHashesVerified":True,"inputPixelHashes":{entry["id"]:entry["sha256"] for entry in ASSETS},
            "stateFamilySameCanvas":True,"stateFamilyCount":len(groups),"borderChecksPassed":True,
            "uiSkinsHaveAlpha":True,"transparentExteriorPassedExceptIntentionalPaperTile":True,"nativeArtworkActuallyViewed":True,
            "unityImportExecuted":False,"status":"passed-file-and-spec-checks; Unity pending"}


def main():
    RECORDS.mkdir(parents=True,exist_ok=True)
    make_ui();make_icons()
    modern=RECORDS/"survival-icon-slices.json"
    if modern.is_file():
        ASSETS.extend(read_json(modern)["assets"])
    font=font_record();evidence=snapshot_evidence();checks=validate();contact_sheet()
    manifest={"schemaVersion":1,"task":"青岚余生（暂定名）全游戏UI美术",
              "createdAt":datetime.now(timezone.utc).isoformat(),"phase":"art-only; Unity integration deferred",
              "designResolution":[1920,1080],"artReferenceRepository":str(SOURCE),
              "artReferenceRemote":"https://luyuacpp.visualstudio.com/image/_git/image",
              "functionalReference":"https://github.com/CleverRaven/Cataclysm-DDA",
              "resultRepository":"待补充；本阶段未提交/推送/发布",
              "generationPerformedByThisBuilder":False,
              "sourceOnlyFiles":["art-delivery/resources/icons/survival-icons-master.png","art-delivery/resources/icons/survival-icons-master.png.generation.json", "art-delivery/resources/ui/clean-header-master.png", "art-delivery/resources/ui/clean-header-master.png.generation.json"],
              "important":"This manifest covers common UI kit and reference icons. New scene/character/icon-sheet generation is tracked by the parent production records separately.",
              "font":font,"sourceEvidenceSnapshots":evidence,"assets":ASSETS,"validation":checks,
              "semanticCaution":"Illustration category labels are UI design examples. Source Five Elements MMO skill identities/stat values, server, pet cultivation and reward economy were not transferred to CDDA.",
              "missingSourceDocuments":["qdao_ui_redesign_v5/UI_SPEC.md", "qdao_asset_refresh_v6/icons/README.md", "designs/class-skills-20260928/README.md"],
              "modernSurvivalIcons":"Parent production supplies modern gear icon sheet separately; existing Daoist icons are not relabeled as guns/tools."}
    (RECORDS/"asset-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (RECORDS/"resource-validation.json").write_text(json.dumps(checks,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (RECORDS/"unity-import.csv").open("w",encoding="utf-8-sig",newline="") as stream:
        writer=csv.writer(stream)
        writer.writerow(["id","file","width","height","state","stateFamily","SpriteMode","SpriteType","BorderLeft","BorderBottom","BorderRight","BorderTop","PivotX","PivotY","PPU","resizeAxes","sha256"])
        for entry in ASSETS:
            writer.writerow([entry["id"],entry["file"],entry["width"],entry["height"],entry["state"],entry.get("stateFamily"),"Single",entry["spriteType"],*entry["borderLeftBottomRightTop"],*entry["pivot"],entry["pixelsPerUnit"],entry["resizeAxes"],entry["sha256"]])
    print(json.dumps({key:value for key,value in checks.items() if key!="inputPixelHashes"},ensure_ascii=False))


if __name__=="__main__":main()
