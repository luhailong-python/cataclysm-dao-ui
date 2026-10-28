"""Isolate all 24 generated survival objects by their actual alpha components.

The source was requested as a grid, but object silhouettes cross nominal cells.
This builder uses connected painted components and keeps soft edge alpha; it does
not cut the sheet into equal cells, repaint objects, or upscale their detail.
"""
from __future__ import annotations
from array import array
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
MASTER=ROOT/"art-delivery/resources/icons/survival-icons-master.png"
RECORD=MASTER.with_name(MASTER.name+".generation.json")
NAMES=("battery","flashlight","bandage","water","food","wrench",
       "wheel","scrap","bottle","rifle","ammo","magnifier",
       "map","compass","campfire","terminal","circuit","book",
       "backpack","radio","helmet","seeds","meat","pot")


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    with Image.open(MASTER) as opened:source=opened.convert("RGBA")
    width,height=source.size
    alpha=source.getchannel("A")
    pixels=bytearray(alpha.tobytes())
    labels=array("H",[0])*(width*height)
    components=[]
    # Connected pixels above 16 establish the actual object cores.
    for index,value in enumerate(pixels):
        if value<=16:continue
        cid=len(components)+1
        stack=[index];pixels[index]=0;labels[index]=cid
        area=0;left=right=index%width;top=bottom=index//width
        while stack:
            current=stack.pop();x=current%width;y=current//width;area+=1
            left=min(left,x);right=max(right,x);top=min(top,y);bottom=max(bottom,y)
            neighbors=[]
            if x:neighbors.append(current-1)
            if x+1<width:neighbors.append(current+1)
            if y:neighbors.append(current-width)
            if y+1<height:neighbors.append(current+width)
            for neighbor in neighbors:
                if pixels[neighbor]>16:
                    pixels[neighbor]=0;labels[neighbor]=cid;stack.append(neighbor)
        components.append({"id":cid,"area":area,"bbox":[left,top,right+1,bottom+1]})
    major=[c for c in components if c["area"]>6000]
    if len(major)!=24:raise ValueError(f"Expected 24 painted cores, got {len(major)}")
    # Sheet is regular in reading order, but the individual crops are deliberately not uniform.
    major.sort(key=lambda c:(((c["bbox"][1]+c["bbox"][3])/2)//250,c["bbox"][0]))
    assignment={c["id"]:index for index,c in enumerate(major)}
    def box_distance(a,b):
        dx=max(b[0]-a[2],a[0]-b[2],0);dy=max(b[1]-a[3],a[1]-b[3],0)
        return dx*dx+dy*dy
    for c in components:
        if c["id"] in assignment or c["area"]<4:continue
        index=min(range(24),key=lambda i:box_distance(c["bbox"],major[i]["bbox"]))
        if box_distance(c["bbox"],major[index]["bbox"])<=24*24:
            assignment[c["id"]]=index
    entries=[]
    masterhash=sha(MASTER)
    for index,(name,core) in enumerate(zip(NAMES,major)):
        assigned=[c for c in components if assignment.get(c["id"])==index]
        left=max(0,min(c["bbox"][0]for c in assigned)-5)
        top=max(0,min(c["bbox"][1]for c in assigned)-5)
        right=min(width,max(c["bbox"][2]for c in assigned)+5)
        bottom=min(height,max(c["bbox"][3]for c in assigned)+5)
        crop=source.crop((left,top,right,bottom))
        maskbytes=bytearray((right-left)*(bottom-top))
        for y in range(top,bottom):
            for x in range(left,right):
                if assignment.get(labels[y*width+x])==index:
                    maskbytes[(y-top)*(right-left)+x-left]=255
        mask=Image.frombytes("L",crop.size,bytes(maskbytes)).filter(ImageFilter.MaxFilter(9))
        edge_alpha=ImageChops.multiply(crop.getchannel("A"),mask)
        # Remove isolated near-zero noise; retain soft edge alpha >= 4 unchanged.
        edge_alpha=edge_alpha.point(lambda a:a if a>=4 else 0)
        crop.putalpha(edge_alpha)
        silhouette=crop.getbbox()
        crop=crop.crop(silhouette)
        native_bbox=[left+silhouette[0],top+silhouette[1],left+silhouette[2],top+silhouette[3]]
        native_size=crop.size
        factor=min(1.0,224/crop.width,224/crop.height)
        export_size=(max(1,round(crop.width*factor)),max(1,round(crop.height*factor)))
        if export_size!=crop.size:crop=crop.resize(export_size,Image.Resampling.LANCZOS)
        canvas=Image.new("RGBA",(256,256))
        position=((256-crop.width)//2,(256-crop.height)//2)
        canvas.alpha_composite(crop,position)
        target=MASTER.with_name("survival-"+name+".png")
        canvas.save(target)
        alpha_bbox=canvas.getchannel("A").getbbox()
        margins=[alpha_bbox[0],alpha_bbox[1],256-alpha_bbox[2],256-alpha_bbox[3]]
        if min(margins)<14:raise ValueError(f"Insufficient padding: {name} {margins}")
        record={
            "id":"survival-"+name,"file":target.relative_to(ROOT).as_posix(),"category":"icons",
            "size":[256,256],"width":256,"height":256,"mode":"RGBA","sha256":sha(target),
            "alphaExtrema":list(canvas.getchannel("A").getextrema()),"alphaContentBox":list(alpha_bbox),
            "transparentMarginsLeftTopRightBottom":margins,"state":"normal","stateFamily":None,
            "borderLeftBottomRightTop":[0,0,0,0],"resizeAxes":"none","pivot":[0.5,0.5],
            "pixelsPerUnit":100,"spriteType":"Simple","spriteImportMode":"Single","meshType":"FullRect",
            "filterMode":"Bilinear","wrapMode":"Clamp","mipmaps":False,"sRGB":True,"alphaIsTransparency":True,
            "dynamicTextBaked":False,"containsFixedArtSymbol":True,"meaning":name,
            "operation":"Isolate actual alpha-connected painted object and nearby fragments, preserve four-pixel soft-edge fringe, remove alpha<4 noise; tight crop, downsample only if needed, center with >=14px transparent padding on 256 canvas. No new image generation or repaint.",
            "cropBoxNativeXYXY":native_bbox,"nativeCropPixelSize":list(native_size),
            "placedPixelSize":list(export_size),"positionTopLeft":list(position),"scaleFactor":factor,
            "relationship":"adapted-use","newModelGeneration":False,
            "derivedFrom":[{"file":MASTER.relative_to(ROOT).as_posix(),"sha256":masterhash,
                            "generationRecord":RECORD.relative_to(ROOT).as_posix(),"sourcePixelSize":[width,height]}],
            "actualModel":None,"actualQuality":None,
            "modelQualityEvidence":"Refer to parent master generation record; actual model/quality unconfirmed by host. Cropping is not a model call.",
            "unityValidation":"Import recommendation only; pending next Unity stage",
        }
        entries.append(record)
    output={"schemaVersion":1,"createdAt":datetime.now(timezone.utc).isoformat(),"master":MASTER.relative_to(ROOT).as_posix(),
            "masterSha256":masterhash,"method":"nonuniform connected-component object extraction; not equal-grid cropping",
            "gridReadingOrder":[6,4],"assets":entries,"checks":{"icons":24,"equalCanvas":True,"noUpscaling":True,
            "minimumTransparentPadding":min(min(e["transparentMarginsLeftTopRightBottom"])for e in entries),
            "noSourceEdgeTouch":all(e["cropBoxNativeXYXY"][0]>0 and e["cropBoxNativeXYXY"][1]>0 and e["cropBoxNativeXYXY"][2]<width and e["cropBoxNativeXYXY"][3]<height for e in entries)}}
    path=ROOT/"art-delivery/records/survival-icon-slices.json"
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output["checks"]))


if __name__=="__main__":main()
