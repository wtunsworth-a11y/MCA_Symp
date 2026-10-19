#!/usr/bin/env python3
# Builds Waves v14 from v13: (1) move Oro Butterfly to first ICAD case + renumber;
# (2) insert Table 1 (waves -> tools -> outcomes) at the end of Section 5.
import zipfile, re

SRC="/home/user/MCA_Symp/drafts/Waves_of_Conservation_in_PNG_v13.docx"
OUT="/home/user/MCA_Symp/drafts/Waves_of_Conservation_in_PNG_v14.docx"

z=zipfile.ZipFile(SRC)
doc=z.read('word/document.xml').decode('utf-8')
footer=z.read('word/footer1.xml').decode('utf-8').replace('(v13)','(v14)')

m=re.search(r'(<w:body>)(.*)(<w:sectPr>.*</w:sectPr></w:body></w:document>)', doc, re.S)
head=doc[:m.start(2)]; tail=doc[m.start(3):]; body=m.group(2)
paras=re.findall(r'<w:p\b.*?</w:p>', body, re.S)
assert len(paras)==137, len(paras)

# ---- (1) reorder Section 4 cases ----
lak=paras[33:36]; br=paras[36:39]; crater=paras[39:41]; oro=paras[41:44]; kamiali=paras[44:49]
def renum(block, old, new):
    block=list(block); block[0]=block[0].replace(old,new,1); return block
oro=renum(oro,"4.4  The Oro Butterfly","4.1  The Oro Butterfly")
lak=renum(lak,"4.1  Lak","4.2  Lak")
br=renum(br,"4.2  Bismarck","4.3  Bismarck")
crater=renum(crater,"4.3  Crater","4.4  Crater")
# kamiali stays 4.5
reordered = oro + lak + br + crater + kamiali
paras = paras[:33] + reordered + paras[49:]

# ---- (2) Table 1 ----
RPR='<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri"/>'
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def run(t,b=False,i=False,sz=18,color=None):
    r='<w:r><w:rPr>'+RPR
    if b: r+='<w:b/><w:bCs/>'
    if i: r+='<w:i/><w:iCs/>'
    if color: r+=f'<w:color w:val="{color}"/>'
    return r+f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
def tc(w,runs,shade=None):
    shd=f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ''
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}</w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:after="20" w:line="240"/></w:pPr>{runs}</w:p></w:tc>')
def rowx(cells): return '<w:tr>'+''.join(cells)+'</w:tr>'
W=[1500,2500,2800,2560]; HEAD="1F5C2E33" if False else "DCEAD9"
def cell(ci,text,b=False,it=False,shade=None): return tc(W[ci],run(text,b=b,i=it,color=("1F5C2E" if b and shade else None)),shade)

rows=[]
rows.append(rowx([tc(W[0],run("Wave",b=True),"DCEAD9"),tc(W[1],run("Theory / starting point",b=True),"DCEAD9"),
                  tc(W[2],run("Main tools & instruments",b=True),"DCEAD9"),tc(W[3],run("Outcomes",b=True),"DCEAD9")]))
data=[
 ("1 — Circumstance","Protection as a by-product of how people lived",
  "None deliberate: customary practice (sacred groves, taboos, fallows), low population, subsistence economy, territorial limits",
  "Extensive intact forest persisted — most of what still stands — but as a by-product, not an achieved outcome"),
 ("2 — Imposition (1970s–90s)","The state sets land aside and manages it",
  "National parks and reserves; Wildlife Management Areas (Fauna (Protection and Control) Act); 1975 Constitution, Fourth Goal",
  "~2.8% designated by the mid-1990s, mostly too small; ~89% with no or minimal management (1999); “paper parks” — but the WMA established the community-tenure principle"),
 ("3 — Transaction (ICAD, 1986–2010s)","Development exchanged for conservation",
  "ICAD/ICDP projects; development inducements; Conservation Needs Assessment site selection; UNDP–GEF funding",
  "Few durable protected areas; cargo expectations; could not out-compete logging. Legacy: the Bismarck Ramu Group, a documented body of lessons, and partial local gains"),
 ("4 — Consent (2009–present)","Consent is the foundation, built first",
  "Conservation Areas Act 1978 gazettal (YUS, Managalas); conservation deeds; FPIC; 2014 PA Policy; Protected Areas Act 2024; payment for ecosystem services",
  "First gazetted Conservation Areas (YUS 2009; Managalas 2017, 214,696 ha). Coverage ~4%, under ~1% effectively managed; consent secured but the shared vision not yet delivered"),
]
for wv,th,tl,oc in data:
    rows.append(rowx([tc(W[0],run(wv,b=True)),tc(W[1],run(th)),tc(W[2],run(tl)),tc(W[3],run(oc))]))
# proposed fifth row (italic)
rows.append(rowx([
  tc(W[0],run("5 — Recognition? (proposed)",b=True,i=True)),
  tc(W[1],run("Recognising what the first wave still holds",i=True)),
  tc(W[2],run("To be defined by the symposium — candidate tools: OECMs, participatory mapping, recognised community-conserved areas, and private-sector and sub-national instruments",i=True)),
  tc(W[3],run("To be defined by the symposium",i=True))]))

tbl=('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>'
     +''.join(f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="BBBBBB"/>' for e in ['top','left','bottom','right','insideH','insideV'])
     +'</w:tblBorders><w:tblLook w:val="04A0"/></w:tblPr>'
     +'<w:tblGrid>'+''.join(f'<w:gridCol w:w="{w}"/>' for w in W)+'</w:tblGrid>'
     +''.join(rows)+'</w:tbl>')
cap=('<w:p><w:pPr><w:spacing w:before="200" w:after="60"/><w:jc w:val="center"/></w:pPr>'
     +run("Table 1. ",b=True,color="444444")
     +run("The waves of conservation in Papua New Guinea: tools and outcomes. The fifth row is left open deliberately — its tools and expected outcomes are for the symposium to agree.",i=True,color="444444")
     +'</w:p>')
after_tbl_spacer='<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'

# insert [cap, tbl, spacer] before the Section 6 heading
idx=next(i for i,pp in enumerate(paras) if 'The ground the future stands on' in pp)
paras = paras[:idx] + [cap, tbl, after_tbl_spacer] + paras[idx:]

newdoc=head+''.join(paras)+tail

zout=zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED)
for item in z.infolist():
    data=z.read(item.filename)
    if item.filename=='word/document.xml': data=newdoc.encode('utf-8')
    elif item.filename=='word/footer1.xml': data=footer.encode('utf-8')
    zout.writestr(item,data)
zout.close()
print("WROTE",OUT)
