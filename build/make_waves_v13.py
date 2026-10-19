#!/usr/bin/env python3
# Builds Waves v13 from the committed v12 .docx by applying deltas to the XML.
# Kept in the repo so it survives container recycles.
import zipfile, re, io, shutil, html

SRC="/home/user/MCA_Symp/drafts/Waves_of_Conservation_in_PNG_v12.docx"
OUT="/home/user/MCA_Symp/drafts/Waves_of_Conservation_in_PNG_v13.docx"
PEGS_PNG="/home/user/MCA_Symp/drafts/figures/Waves_figure_pegs_v1.png"
GAZ_PNG="/home/user/MCA_Symp/drafts/figures/Waves_figure_PAgazettal_v1.png"

z=zipfile.ZipFile(SRC)
doc=z.read('word/document.xml').decode('utf-8')
rels=z.read('word/_rels/document.xml.rels').decode('utf-8')
footer=z.read('word/footer1.xml').decode('utf-8')

# ---- split body into paragraphs ----
m=re.search(r'(<w:body>)(.*)(<w:sectPr>.*</w:sectPr></w:body></w:document>)', doc, re.S)
head=doc[:m.start(2)]
tail=doc[m.start(3):]
body=m.group(2)
paras=re.findall(r'<w:p\b.*?</w:p>', body, re.S)
assert len(paras)==126, len(paras)

# ---- XML builders ----
RPR='<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri"/>'
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def run(t,b=False,i=False,sz=22,color=None):
    r='<w:r><w:rPr>'+RPR
    if b: r+='<w:b/><w:bCs/>'
    if i: r+='<w:i/><w:iCs/>'
    if color: r+=f'<w:color w:val="{color}"/>'
    r+=f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
    return r
BODY_PPR='<w:pPr><w:spacing w:after="140" w:line="276"/><w:jc w:val="both"/></w:pPr>'
REF_PPR='<w:pPr><w:spacing w:after="100" w:line="264"/><w:ind w:left="576" w:hanging="576"/></w:pPr>'
def para(runs): return '<w:p>'+BODY_PPR+''.join(runs)+'</w:p>'
def refpara(runs): return '<w:p>'+REF_PPR+''.join(runs)+'</w:p>'
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

def rt(para_xml, old, new):
    assert old in para_xml, "NOT FOUND: "+old[:60]
    return para_xml.replace(old,new)

# ===================================================================
# DELTAS
# ===================================================================
newp=list(paras)

# ---- (fix, pre-existing in v12) scope-box border child order: schema wants top,left,bottom,right ----
def fix_border(pxml):
    m=re.search(r'<w:pBdr>(.*?)</w:pBdr>', pxml, re.S)
    if not m: return pxml
    inner=m.group(1); tags={}
    for t in ['top','left','bottom','right','between','bar']:
        mm=re.search(r'(<w:'+t+r'\b[^>]*/>)', inner)
        if mm: tags[t]=mm.group(1)
    ordered=''.join(tags[t] for t in ['top','left','bottom','right','between','bar'] if t in tags)
    return pxml.replace(m.group(0), '<w:pBdr>'+ordered+'</w:pBdr>')
newp[16]=fix_border(newp[16])

# ---- (fix) footer version ----
footer=footer.replace('(v12)','(v13)')

# ---- (fix) Anderson citation [95] ----
newp[95]=rt(newp[95],
  'Challenging ‘integrated conservation and development’ in Papua New Guinea: the Bismarck Ramu Group',
  'Challenging ‘integrated conservation and development’ in Papua New Guinea: the Bismarck Ramu Group')
newp[95]=rt(newp[95],
  '. [Full publication details to be confirmed against the source at finalisation.]',
  '. Pacific Economic Bulletin 20(1): 56–70. Canberra: Asia Pacific Press.')

# ---- (cite Mace) intro global-shift [13] ----
newp[13]=rt(newp[13],
  'towards a rights-based paradigm that puts local people first (Phillips 2003)',
  'towards a rights-based paradigm that puts local people first (Phillips 2003; Mace 2014)')

# ---- (Managalas does-both) [52] ----
newp[52]=rt(newp[52],
  'Its defining feature is precisely the one the ICAD era lacked: the agreement of the landowners came first, and the legal area followed from it.',
  'Its defining feature is precisely the one the ICAD era lacked: the agreement of the landowners came first, and the legal area followed from it. It is offered here as both the largest expression of consent-led conservation and, as the next paragraphs make plain, the clearest illustration of its central risk.')

# ---- (Wave Four = hypothesis) [55] ----
newp[55]=rt(newp[55],
  'They are best read not as proof that the consent model works, but as the most promising evidence so far that it might.',
  'They are best read not as proof that the consent model works, but as the most promising evidence so far that it might: a hypothesis this symposium is convened to test, not a finding to be reported.')

# ---- (renumber fifth-wave figure caption 2 -> 4) [83] ----
newp[83]=rt(newp[83],'Figure 2. ','Figure 4. ')

# ---- (NBSAP enhancement) [64] guiding policies ----
newp[64]=rt(newp[64],
  'the National Biodiversity Strategy and Action Plan (NBSAP)',
  'the National Biodiversity Strategy and Action Plan 2019–2024, which records the country’s own target of placing five per cent of its land under protected areas, a target it has not met, and which is now being revised for 2025–2030 to align with the Kunming–Montreal framework (its national targets not yet published at the time of writing)')

# ---- (drop superlative + add O'Neill) fifth-wave [81] ----
newp[81]=rt(newp[81],
  ' Measured by outcome rather than intention, conservation by circumstance has been by far the most effective of all.',
  ' Measured by outcome rather than intention, it is the forests that no one set out to protect that have lasted best.')
oneill=(" This is not a marginal accounting trick. Recent global work finds that once national datasets and potential OECMs are counted, conservation-area coverage is far higher than the official figures record, close to 27 per cent of the world’s land rather than the reported 18.5 per cent (O’Neill et al. 2026), though nothing like that in Papua New Guinea, which sits near four per cent even when Managalas is counted. Much of that uncounted land is community-, Indigenous- or privately-governed, and the same study finds it can match or outperform state protected areas, and matters most of all for tropical forests. But it carries the warning this paper has made throughout: adding area achieves little on its own, because the land most easily counted is the land least under threat, and genuine representativeness barely improves. Recognition is therefore real and substantial, but only if it reaches the forests that matter rather than the residual reserve, and, as that study stresses, only where the people who govern the land ask for it.")
newp[81]=rt(newp[81],
  ' and the conserved territories of indigenous peoples and local communities (IUCN 2023).',
  ' and the conserved territories of indigenous peoples and local communities (IUCN 2023).'+oneill)

# ---- (§6) replace square-peg funding para [67] with the pegs framing + figure ----
pegs_section=[
 para([run("One consequence deserves to be stated plainly, because it inverts the usual order of business, and because it is where this paper parts company with how conservation has been attempted before. Begin by naming the hole, for every wave so far has failed partly by not doing so. Each assumed it knew the problem, and each solved the problem it assumed: the second wave drew the protected area, the third delivered the development incentive, the fourth secured the consent. Each still fell short, because the real need was never stated. The hole these efforts are meant to fill is not conservation. It is the enduring wellbeing of the customary community: a good life lived on and from their own land, a dependable livelihood, health, schooling, secure rights, social order, the continuation of culture, and a healthy environment to hold it all together. Conservation is one part of that, no more.")]),
 para([run("Name the hole this way and the old failure comes into focus as a failure of expectation. The square peg was conservation made to carry the whole of it: a thing defined, and funded, as an outside donor would understand it, pressed onto communities whose own understanding of it, and whose capacity to deliver it in those terms, were different. A promise the size of the whole hole can only be broken, and it is broken in the way that matters most, not on a ledger but in the eyes of the community, where a shortfall against an oversized promise is felt as betrayal even when something real was delivered. Consent runs on that perception, not on an audit. The first virtue of what follows is therefore not more delivery but honest expectation: each part promising only what it can keep, and the gaps named at the outset rather than discovered at the end.")]),
 para([run("The way through is to stop asking conservation to be the only peg, and to set it among others, each with a named owner. Conservation, defined narrowly enough to be deliverable, is one peg, held by the landowners and the practitioners who support them, and increasingly by the private sector and by provincial and local-level government where their own lands and laws allow. Infrastructure and basic services are another, and they belong to government, through the national and provincial development budgets, not to conservation. A living from the land is a third, shared among the community, the private sector and development partners. The security of customary rights and boundaries is a fourth. Knowledge of what the land is, and what it could become, is the one part the conservation effort genuinely owns and must supply. Between these pegs there will still be gaps, aspirations no one can meet, chief among them the forms of growth that require clearing the very forest the arrangement exists to keep; naming those gaps plainly, as the agreed limit of what is on offer, holds better than a promise that one peg covers everything.")]),
 para([run("Some of the most important pegs are not on the land at all. Conservation of a customary landscape does not succeed in isolation from the country around it; it depends on a thriving economy beyond the boundary. Investment in manufacturing and services, the creation of formal jobs, genuine urban development rather than the spread of settlements, home ownership, careers a young person can build: these are nation-building outcomes, the business of the national government, the private sector and development partners, not of any conservation project. Their contribution is quieter but no less vital, for they offer an alternative. Rural smallholder life is honourable and full of meaning, but it is not the only life, and it is not for everyone. An economy that can draw those who wish to leave into formal employment eases the pressure a growing population would otherwise place on the forest, and leaves those who remain on the land doing so by choice rather than necessity. A thriving economy outside the conservation boundaries is not a distraction from conservation; it is one of the conditions of its success.")]),
 para([run("Unbundling the task this way does not make the problem vanish; it changes its shape, and leaves two kinds of gap. The first lie between the pegs, where they must meet: conservation in place but the road not built, rights recognised but no livelihood to follow. These are not inevitable. They are a coordination problem, and they are where the whole arrangement breaks down if no one holds it together; who coordinates the alliance, and how, is one of the real questions this symposium exists to answer. The second kind sits at the edges: aspirations no peg can meet, because nobody is ever wholly satisfied. These are irreducible, and the mature course is to name and accept them, not to pretend they are closed. One thing more follows, and it is what makes the arrangement durable: a shortfall is now attributable. When a peg fails it can be seen which owner fell short, or where the coordination broke, and that can be put right, rather than the whole structure, and the community’s consent with it, collapsing onto conservation. Failure becomes diagnosable instead of fatal. Only once the shape of the hole and the division of the pegs are agreed does the money question arise, and then in its proper place: the funding is sought, or designed, to fit a conservation that can actually be delivered, never the other way about.")]),
]
# pegs figure (rId12) + caption
PEGS_CX=5669280; PEGS_CY=round(PEGS_CX*1720/3040)
pegs_fig=[figpara("rId12",PEGS_CX,PEGS_CY,101),
          capt("3","Conservation is one peg, not the whole hole. The old way loads every aspiration onto conservation, which fits nothing and is blamed for the rest; the unbundled way fills the hole of community wellbeing with several pegs, each with an accountable owner, with the coordination between them and the honest residual gaps both named.")]
newp[67]=''.join(p for p in pegs_section)+''.join(pegs_fig)

# ---- (§7) definition rewrite + descriptors [71] ----
defn_run=run("conservation in Papua New Guinea is an enduring, community-managed landscape — forest, grassland, mangrove or reef — kept healthy by the people who hold it, through management recognisably their own, in which those communities can thrive.",b=True,i=True)
newp[71]=rt(newp[71],
  'As a starting point for that discussion, and no more than a starting point, the paper offers this: ',
  'As a starting point for that discussion, and no more than a starting point, offered for the symposium to amend or reject, the paper suggests this: ')
# swap the old italic definition run for the new one by replacing its text
newp[71]=rt(newp[71],
  'conservation in Papua New Guinea is the deliberate and lasting care of a customary landscape by the people who own it, in a way that keeps its forests, waters and wildlife healthy while also providing a livelihood from them, sustaining nature, community and social order together for generations to come, with government, non-government organisations and funders in support rather than in charge.',
  'conservation in Papua New Guinea is an enduring, community-managed landscape — forest, grassland, mangrove or reef — kept healthy by the people who hold it, through management recognisably their own, in which those communities can thrive.')
newp[71]=rt(newp[71],
  ' Whether that is the right wording, or even the right idea, is exactly what the participants must decide.',
  ' The word enduring is chosen so the landscape may last and adapt, not freeze; the people who hold it because conservation that is not owned does not hold; kept healthy because the test is the state of the land, not the drawing of a line around it; and in which communities can thrive as a condition the whole alliance must meet, not a task conservation performs alone. The definition is written for all of Papua New Guinea’s landscapes and seascapes, so it need not be re-argued for the sea, though this paper develops the terrestrial case. Whether that is the right wording, or even the right idea, is exactly what the participants must decide.')
# new paragraph after [71]: minimum descriptors
descriptors=para([
  run("What, then, counts as management “recognisably their own”? ",b=True),
  run("Rather than importing a checklist, the symposium might agree a short set of minimum descriptors of effective management, expressed in customary terms: known boundaries, where the community agrees where its landscape begins and ends and the clan boundaries within it are mapped and respected; rules that are owned and kept, with clan land-use rules set, understood and enforced locally; wise and lasting use, so resources are used in ways that can continue indefinitely while still providing a living; knowledge, shared and current, so the community can say what is in the landscape and how it is changing; tradition and tool together, respecting customary practice while adopting appropriate technology to strengthen it; and adaptive care, so management responds to change, slow and sudden alike, rather than assuming the landscape will stay as it is. These are what make effectiveness checkable and owner-legible at once, the rigorous core that the global accounting asks for and that the previous waves never defined. Both the definition and the descriptors are offered here as discussion points, not conclusions: they are for the symposium to settle.")])

# ---- assemble new body with insertions ----
# figures/table/reorder handled below by index operations on newp
# gazettal figure after [58] (legal/coverage, §5)
GAZ_CX=5669280; GAZ_CY=round(GAZ_CX*1440/2400)
gaz_fig=figpara("rId13",GAZ_CX,GAZ_CY,102)+capt("2","Protected areas gazetted in Papua New Guinea, 1962–2024 (cumulative), from the Protected Areas Act 2024 register, set against the waves of conservation. Most of the estate was gazetted during the imposition and ICAD eras; the consent era has added only a few. The register records only areas actually gazetted, not the many that were proposed, consented or brought close to gazettal but never declared, so the real effort under each wave was greater.")

# ---- reference entries: Mace (2014), O'Neill et al. (2026) ----
mace_ref=refpara([run("Mace, G. M. (2014). ‘Whose conservation?’ ",sz=20),
                  run("Science",i=True,sz=20),
                  run(" 345(6204): 1558–1560.",sz=20)])
oneill_ref=refpara([run("O’Neill, H. M. K. et al. (2026). ‘Global conservation area coverage substantially exceeds current estimates.’ ",sz=20),
                    run("Nature",i=True,sz=20),
                    run(". https://doi.org/10.1038/s41586-026-11157-4",sz=20)])

# Build final list with inserts (walk original indices)
inserts_after={58:[gaz_fig], 71:[descriptors], 114:[mace_ref], 117:[oneill_ref]}
# (pegs section already baked into newp[67])
final=[]
for i,pp in enumerate(newp):
    final.append(pp)
    if i in inserts_after:
        final.extend(inserts_after[i])

newbody=''.join(final)
newdoc=head+newbody+tail

# ---- rels: add image rels rId12 (pegs) rId13 (gazettal) ----
addrels=('<Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/pegs_v1.png"/>'
         '<Relationship Id="rId13" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/gazettal_v1.png"/>')
rels=rels.replace('</Relationships>',addrels+'</Relationships>')

# ---- write new docx ----
shutil.copy(SRC, OUT+".tmp")
zin=zipfile.ZipFile(SRC)
zout=zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data=zin.read(item.filename)
    if item.filename=='word/document.xml': data=newdoc.encode('utf-8')
    elif item.filename=='word/_rels/document.xml.rels': data=rels.encode('utf-8')
    elif item.filename=='word/footer1.xml': data=footer.encode('utf-8')
    zout.writestr(item, data)
zout.write(PEGS_PNG,'word/media/pegs_v1.png')
zout.write(GAZ_PNG,'word/media/gazettal_v1.png')
zout.close()
import os
os.remove(OUT+".tmp")
print("WROTE", OUT)
