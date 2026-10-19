#!/usr/bin/env python3
# Builds Waves v15 from v14: (1) reorder the Section 4 intro project list to lead with
# the Oro Butterfly Project; (2) embed the forest-cover figure (Figure 3) with a bridge
# passage at the end of Section 5; renumber later figures; footer -> v15.
import zipfile, re

SRC="/home/user/MCA_Symp/drafts/Waves_of_Conservation_in_PNG_v14.docx"
OUT="/home/user/MCA_Symp/drafts/Waves_of_Conservation_in_PNG_v15.docx"
FOREST_PNG="/home/user/MCA_Symp/drafts/figures/Waves_figure_forest_v1.png"

z=zipfile.ZipFile(SRC)
doc=z.read('word/document.xml').decode('utf-8')
rels=z.read('word/_rels/document.xml.rels').decode('utf-8')
footer=z.read('word/footer1.xml').decode('utf-8').replace('(v14)','(v15)')

m=re.search(r'(<w:body>)(.*)(<w:sectPr>.*</w:sectPr></w:body></w:document>)', doc, re.S)
head=doc[:m.start(2)]; tail=doc[m.start(3):]; body=m.group(2)
paras=re.findall(r'<w:p\b.*?</w:p>', body, re.S)

RPR='<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri"/>'
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def run(t,b=False,i=False,sz=22,color=None):
    r='<w:r><w:rPr>'+RPR
    if b: r+='<w:b/><w:bCs/>'
    if i: r+='<w:i/><w:iCs/>'
    if color: r+=f'<w:color w:val="{color}"/>'
    return r+f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
BODY_PPR='<w:pPr><w:spacing w:after="140" w:line="276"/><w:jc w:val="both"/></w:pPr>'
def para(runs): return '<w:p>'+BODY_PPR+''.join(runs)+'</w:p>'
def figpara(rid,cx,cy,pid):
    return (f'<w:p><w:pPr><w:spacing w:after="40" w:before="160"/><w:jc w:val="center"/></w:pPr>'
      f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
      f'<wp:effectExtent t="0" r="0" b="0" l="0"/><wp:docPr id="{pid}" name="" descr="" title=""/>'
      f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
      f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="" descr=""/>'
      f'<pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/></pic:cNvPicPr></pic:nvPicPr>'
      f'<pic:blipFill><a:blip r:embed="{rid}" cstate="none"/><a:srcRect/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
      f'<pic:spPr bwMode="auto"><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
      f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
def capt(figno,text):
    return ('<w:p><w:pPr><w:spacing w:after="200"/><w:jc w:val="center"/></w:pPr>'
      +run(f"Figure {figno}. ",b=True,sz=18,color="444444")+run(text,i=True,sz=18,color="444444")+'</w:p>')

# ---- (1) reorder intro list ----
old_list="that bargain: Lak, Bismarck–Ramu, Crater Mountain, the Oro Butterfly Project, Kamiali, Kikori Basin and the Hunstein Range among them."
new_list="that bargain: the Oro Butterfly Project, Lak, Bismarck–Ramu, Crater Mountain, Kamiali, Kikori Basin and the Hunstein Range among them."
paras=[pp.replace(old_list,new_list) for pp in paras]

# ---- (2) renumber later figure captions (pegs 3->4, fifth wave 4->5) ----
# caption number sits in a separate run from the title, so target by paragraph
for i,pp in enumerate(paras):
    if 'Conservation is one peg' in pp and 'Figure 3. ' in pp:
        paras[i]=pp.replace('Figure 3. ','Figure 4. ')
    elif 'A potential fifth wave' in pp and 'Figure 4. ' in pp:
        paras[i]=pp.replace('Figure 4. ','Figure 5. ')

# ---- (3) forest figure + bridge passage, before Section 6 ----
CX=5669280; CY=round(CX*1440/2400)
forest=figpara("rId14",CX,CY,103)+capt("3","How much forest does Papua New Guinea have? Competing national estimates, set against the waves. Shearman et al. (2009) mapped a decline from 38 to 33 million ha, 1972–2002; the PNG Forest Authority puts it at ~36 million ha and broadly stable. The sources disagree on both level and trend — on the most measurable fact of all, there is no consensus.")
bridge=para([run("Notice what that disagreement means. The most measurable fact about the country’s environment — how much forest it has, and whether that is shrinking — has no agreed answer; two credible sources give two different pictures. If even the easiest, most countable question cannot yet be settled, it is a plain warning about the harder ones this paper now turns to: what conservation is, what 30x30 should mean here, and who decides. Data matters, and better data would help. But it matters less than what is actually on the ground, the forests that still stand and the people who hold them, and it is to that ground, and to who is responsible for what upon it, that we now turn.")])

idx=next(i for i,pp in enumerate(paras) if 'The ground the future stands on' in pp)
paras = paras[:idx] + [forest, bridge] + paras[idx:]

newdoc=head+''.join(paras)+tail

rels=rels.replace('</Relationships>','<Relationship Id="rId14" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/forest_v1.png"/></Relationships>')

zout=zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED)
for item in z.infolist():
    data=z.read(item.filename)
    if item.filename=='word/document.xml': data=newdoc.encode('utf-8')
    elif item.filename=='word/_rels/document.xml.rels': data=rels.encode('utf-8')
    elif item.filename=='word/footer1.xml': data=footer.encode('utf-8')
    zout.writestr(item,data)
zout.write(FOREST_PNG,'word/media/forest_v1.png')
zout.close()
print("WROTE",OUT)
