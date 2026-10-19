#!/usr/bin/env python3
import cairosvg, html
W,H=1520,860
INK="#2B2B2B"; SUB="#555"; GROUND="#CBB389"; GROUND_D="#9C8458"; HOLE="#EFE7D6"
FONT="Arial, Helvetica, sans-serif"
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
p.append(f'<rect width="{W}" height="{H}" fill="#FBF8F2"/>')
def esc(s): return html.escape(s)
def txt(x,y,s,size=14,col=INK,anchor="middle",weight="normal",style="normal"):
    p.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{col}" font-weight="{weight}" font-style="{style}">{esc(s)}</text>')

txt(W/2,40,"Conservation is one peg — not the whole hole",24,"#1F5C2E","middle","bold")
txt(W/2,66,"Filling the hole of community wellbeing: from one overloaded peg to a set of pegs, each with an owner",14,SUB)

GY=470; HB=640; TOP=330
def ground(x0,x1,hx0,hx1):
    p.append(f'<rect x="{x0}" y="{GY}" width="{hx0-x0}" height="120" fill="{GROUND}" stroke="{GROUND_D}" stroke-width="2"/>')
    p.append(f'<rect x="{hx1}" y="{GY}" width="{x1-hx1}" height="120" fill="{GROUND}" stroke="{GROUND_D}" stroke-width="2"/>')
    p.append(f'<path d="M {hx0},{GY} L {hx0},{HB} Q {hx0},{HB+16} {hx0+16},{HB+16} L {hx1-16},{HB+16} Q {hx1},{HB+16} {hx1},{HB} L {hx1},{GY}" fill="{HOLE}" stroke="{GROUND_D}" stroke-width="2"/>')

def peg(cx,w,role_lines,owner_lines,color,top=TOP,into=HB-6):
    x=cx-w/2; r=16
    p.append(f'<path d="M {x},{top+r} Q {x},{top} {x+r},{top} L {x+w-r},{top} Q {x+w},{top} {x+w},{top+r} L {x+w},{into} Q {x+w},{into+16} {x+w-16},{into+16} L {x+16},{into+16} Q {x},{into+16} {x},{into} Z" fill="{color}" stroke="#00000030" stroke-width="2"/>')
    p.append(f'<rect x="{x+6}" y="{top+6}" width="{w-12}" height="9" rx="4" fill="#ffffff40"/>')
    ry=top+40-(len(role_lines)-1)*9
    for i,ln in enumerate(role_lines):
        txt(cx,ry+i*18,ln,14,"#ffffff","middle","bold")
    oy=GY-34-(len(owner_lines)-1)*7
    for i,ln in enumerate(owner_lines):
        txt(cx,oy+i*14,ln,10.5,"#ffffffdd","middle","normal","italic")

# ---------- LEFT ----------
LX0,LX1=40,560
txt((LX0+LX1)/2,120,"The old way: one peg for everything",16,INK,"middle","bold")
ground(LX0,LX1,120,480)
txt(300,HB+46,"THE HOLE:  community wellbeing",13,GROUND_D,"middle","bold")
txt(300,HB+64,"a good life on and from the land — livelihood, health, schooling, rights, culture, a healthy environment",10.5,SUB)
cx,top,w=300,250,150
p.append(f'<g transform="rotate(-7 {cx} {(top+HB)/2})">')
x=cx-w/2
p.append(f'<rect x="{x}" y="{top}" width="{w}" height="{HB-20-top}" fill="#8A8F6B" stroke="#00000035" stroke-width="2"/>')
for i,ln in enumerate(["CONSERVATION","made to carry","everything:","roads · jobs · services","rights · income …"]):
    txt(cx,top+42+i*20,ln,14 if i==0 else 11,"#ffffff","middle","bold" if i==0 else "normal")
p.append('</g>')
txt(168,HB-30,"gaps",12,"#A23B2E","middle","bold","italic")
txt(452,HB-30,"gaps",12,"#A23B2E","middle","bold","italic")
txt((LX0+LX1)/2,232,"over-promised  →  under-delivered  →  blamed for all of it",12,"#A23B2E","middle","bold","italic")
txt((LX0+LX1)/2,762,"Load every aspiration onto conservation and it fits nothing.",12.5,INK,"middle","normal","italic")
txt((LX0+LX1)/2,782,"It fails at what was never its job — and takes the blame when the rest doesn’t arrive.",12.5,INK,"middle","normal","italic")

p.append(f'<line x1="585" y1="95" x2="585" y2="800" stroke="#DDD6C6" stroke-width="2"/>')

# ---------- RIGHT ----------
RX0,RX1=610,1480
txt((RX0+RX1)/2,120,"The unbundled way: a peg each, an owner each",16,INK,"middle","bold")
ground(RX0,RX1,660,1440)
txt(1050,HB+46,"THE HOLE:  community wellbeing",13,GROUND_D,"middle","bold")
txt(1050,HB+64,"filled by the whole alliance — conservation is one contributor, not the vehicle for all of it",10.5,SUB)

pegs=[
 (["Conservation"],["landowners &","practitioners"],"#3D8B4E"),
 (["Infrastructure","& services"],["government"],"#2F6D8C"),
 (["Livelihoods"],["community,","business, partners"],"#C8842B"),
 (["Rights &","tenure"],["govt &","community"],"#6B5B95"),
 (["Knowledge"],["the conservation","effort"],"#2A9D8F"),
]
x0=682; w=104; gap=18
for i,(rl,ow,col) in enumerate(pegs):
    cx=x0+i*(w+gap)+w/2
    peg(cx,w,rl,ow,col)
# "one peg" callout on conservation
ccx=x0+w/2
p.append(f'<line x1="{ccx}" y1="305" x2="{ccx}" y2="328" stroke="#A23B2E" stroke-width="1.5"/>')
txt(ccx,296,"one peg — not the whole hole",11.5,"#A23B2E","middle","bold","italic")

# external peg (beyond the land)
tx=1385
for bx,bw,bh in [(tx-36,20,40),(tx-12,24,58),(tx+16,18,34)]:
    p.append(f'<rect x="{bx}" y="{188-bh}" width="{bw}" height="{bh}" rx="2" fill="#6E5A47" stroke="#00000025"/>')
txt(tx,116,"beyond the land",11.5,SUB,"middle","bold","italic")
peg(tx,104,["Economy, jobs","& urban","development"],["national govt","& business"],"#6E5A47")
p.append(f'<line x1="{tx}" y1="190" x2="{tx}" y2="328" stroke="#6E5A47" stroke-width="1.5" stroke-dasharray="4,4"/>')

# agreed gap between the land pegs and the external peg
land_right=x0+4*(w+gap)+w   # right edge of knowledge peg
gapx=(land_right+ (tx-w/2))/2
p.append(f'<line x1="{gapx}" y1="330" x2="{gapx}" y2="{HB}" stroke="#A23B2E" stroke-width="1.4" stroke-dasharray="5,4"/>')
txt(gapx,314,"the honest compromise",11,"#A23B2E","middle","bold","italic")
txt(gapx,300,"(nobody is ever 100% happy)",9.5,"#A23B2E","middle","normal","italic")

# coordination bracket over the land pegs (gaps between actors)
kcx=x0+4*(w+gap)+w/2
by=256; CO="#2F6D8C"
p.append(f'<path d="M 734,{by+10} L 734,{by} L {kcx},{by} L {kcx},{by+10}" fill="none" stroke="{CO}" stroke-width="1.6"/>')
for gx in [795,917,1039,1161]:
    p.append(f'<line x1="{gx}" y1="{by}" x2="{gx}" y2="{by+9}" stroke="{CO}" stroke-width="1.4" stroke-dasharray="3,3"/>')
txt((734+kcx)/2,by-8,"Requires coordination — the gaps between actors are where it breaks down",11.5,CO,"middle","bold","italic")

txt((RX0+RX1)/2,762,"Each peg has an owner accountable for it, transparently. Conservation is one of them.",12.5,INK,"middle","normal","italic")
txt((RX0+RX1)/2,782,"Fill the hole well — with the forest kept as part of how — and the global goods follow as the dividend.",12.5,INK,"middle","normal","italic")

p.append('</svg>')
svg="\n".join(p)
open("pegs_cartoon.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to="pegs_cartoon_hi.png",output_width=W*2,output_height=H*2,background_color="white")
print("wrote; land_right=",land_right,"gapx=",gapx)
