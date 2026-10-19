#!/usr/bin/env python3
# Forest-cover figure: shows the competing national estimates to display the LACK OF CONSENSUS.
import cairosvg, html
W,H=1200,720
GREEN="#1F5C2E"; GREENL="#3D8B4E"; MUTE="#9AA0A6"; NEU="#4A5B6B"; EXT="#8A6D00"
INK="#333333"; GRID="#E3E7EA"; AXIS="#666"; BLUE="#2F6D8C"; RED="#A23B2E"
FONT="Arial, Helvetica, sans-serif"
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
p.append(f'<rect width="{W}" height="{H}" fill="white"/>')
def esc(s): return html.escape(s)
XL,XR=95,1150; YB=430; YMAX=48
def xf(y): return XL+(y-1968)*(XR-XL)/(2028-1968)
def yf(v): return YB-v*(YB-100)/YMAX

p.append(f'<text x="{W/2}" y="34" text-anchor="middle" font-size="18" font-weight="bold" fill="{GREEN}">How much forest does Papua New Guinea have? No agreed answer</text>')
p.append(f'<text x="{W/2}" y="56" text-anchor="middle" font-size="12" fill="{INK}">Total forest area (million hectares) by source — the estimates disagree, on the level and on the trend</text>')

for v in (0,12,24,36,48):
    y=yf(v)
    p.append(f'<line x1="{XL}" y1="{y}" x2="{XR}" y2="{y}" stroke="{GRID}"/>')
    p.append(f'<text x="{XL-10}" y="{y+4}" text-anchor="end" font-size="11" fill="{AXIS}">{v}</text>')
p.append(f'<text x="{XL-44}" y="{yf(24)}" text-anchor="middle" font-size="11" fill="{AXIS}" transform="rotate(-90 {XL-44} {yf(24)})">Forest area (million ha)</text>')

yl=yf(46)
p.append(f'<line x1="{XL}" y1="{yl}" x2="{XR}" y2="{yl}" stroke="{MUTE}" stroke-width="1.3" stroke-dasharray="6,4"/>')
p.append(f'<text x="{XR-4}" y="{yl-6}" text-anchor="end" font-size="10.5" fill="{AXIS}">PNG land area ≈ 46 million ha</text>')

p.append(f'<line x1="{XL}" y1="{YB}" x2="{XR}" y2="{YB}" stroke="{AXIS}" stroke-width="1.5"/>')
for yr in range(1970,2026,10):
    x=xf(yr)
    p.append(f'<line x1="{x}" y1="{YB}" x2="{x}" y2="{YB+5}" stroke="{AXIS}"/>')
    p.append(f'<text x="{x}" y="{YB+19}" text-anchor="middle" font-size="11" fill="{AXIS}">{yr}</text>')

# Shearman measured line 1972->2002 (declining)
sh=[(1972,38),(2002,33)]
p.append('<polyline points="'+" ".join(f'{xf(a):.1f},{yf(b):.1f}' for a,b in sh)+f'" fill="none" stroke="{GREEN}" stroke-width="2.8"/>')
for a,b in sh:
    x,y=xf(a),yf(b)
    p.append(f'<circle cx="{x}" cy="{y}" r="5.4" fill="{GREEN}" stroke="white" stroke-width="1.4"/>')
    p.append(f'<text x="{x}" y="{y-12}" text-anchor="middle" font-size="12" font-weight="bold" fill="{GREEN}">{b} Mha</text>')
p.append(f'<text x="{xf(1985)}" y="{yf(37.4)}" text-anchor="middle" font-size="10.5" fill="{GREENL}">Shearman et al. 2009 (satellite): a measured decline</text>')

# PNGFA national estimate 2015 ~36.1 (higher, "stable")
px,py=xf(2015),yf(36.1)
p.append(f'<rect x="{px-6}" y="{py-6}" width="12" height="12" fill="{BLUE}" stroke="white" stroke-width="1.4" transform="rotate(45 {px} {py})"/>')
p.append(f'<text x="{px}" y="{py-13}" text-anchor="middle" font-size="12" font-weight="bold" fill="{BLUE}">~36 Mha</text>')
p.append(f'<text x="{px+14}" y="{py+4}" font-size="10.5" fill="{BLUE}">PNG Forest Authority 2019: ~78% of land, little change</text>')

# "two pictures" annotation between the two
p.append(f'<text x="{xf(2008)}" y="{yf(42)}" text-anchor="middle" font-size="12" font-style="italic" font-weight="bold" fill="{RED}">Two credible sources, two different pictures</text>')

# wave ribbon
def band(y,a,b,label,fill,stroke,tcol,dashed=False,faint=False,left=False):
    xa,xb=xf(a),xf(b); dash=' stroke-dasharray="7,5"' if dashed else ''; op=' opacity="0.45"' if faint else ''
    p.append(f'<rect x="{xa}" y="{y}" width="{xb-xa}" height="22" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}{op}/>')
    if left: p.append(f'<text x="{xa-8}" y="{y+15}" text-anchor="end" font-size="11" font-weight="bold" fill="{tcol}">{esc(label)}</text>')
    else: p.append(f'<text x="{xa+9}" y="{y+15}" font-size="11" font-weight="bold" fill="{tcol}">{esc(label)}</text>')
RB=474
p.append(f'<text x="{XL}" y="{RB-9}" font-size="11" font-weight="bold" fill="{AXIS}">THE WAVES (overlapping, not successive)</text>')
band(RB,   1968,2028,"Wave 1 — Circumstance (background, pre-1970 and continuing)","#F2F2F2",MUTE,"#7A7F85",faint=True)
band(RB+28,1970,1996,"Wave 2 — Imposition","#EEF2F5",NEU,NEU)
band(RB+56,1986,2010,"Wave 3 — Transaction (ICAD)","#F3EBD2",EXT,EXT)
band(RB+84,2009,2026,"Wave 4 — Consent","#DCEAD9",GREEN,GREEN)
band(RB+112,2026,2028,"Wave 5 — Recognition (proposed)","#EAF3E9",GREEN,GREEN,dashed=True,left=True)

fy=RB+150
p.append(f'<line x1="{XL}" y1="{fy-14}" x2="{XR}" y2="{fy-14}" stroke="{GRID}"/>')
notes=[
 "The estimates use different methods and definitions and are not a single series. Shearman et al. (2009, Biotropica) mapped a fall from 38 to 33 million ha, 1972–2002 (a net 15%",
 "cleared, 8.8% degraded); the PNG Forest Authority (2019) and Filer et al. (2009) dispute the magnitude, reporting ~36 million ha (~78% of land) and a more stable trend; Global",
 "Forest Watch records ~1.3 million ha of tree-cover loss over 2001–2017. What all sources agree on: the great majority of Papua New Guinea remains under forest, and loss is",
 "fastest where the forest is accessible. The disagreement is itself the point — on the most measurable fact of all, there is no consensus.",
]
for i,n in enumerate(notes):
    p.append(f'<text x="{XL}" y="{fy+i*15}" font-size="9.5" fill="{AXIS}">{esc(n)}</text>')

p.append('</svg>')
svg="\n".join(p)
open("/home/user/MCA_Symp/drafts/figures/Waves_figure_forest_v1.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to="/home/user/MCA_Symp/drafts/figures/Waves_figure_forest_v1.png",output_width=W*2,output_height=H*2,background_color="white")
print("wrote forest figure")
