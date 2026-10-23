import zipfile,xml.etree.ElementTree as E,re
def sheets(path):
    with zipfile.ZipFile(path) as z:
        strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('{*}si')] if 'xl/sharedStrings.xml' in z.namelist() else []
        rels={x.attrib['Id']:x.attrib['Target'] for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        out={}
        for sh in E.fromstring(z.read('xl/workbook.xml')).findall('.//{*}sheet'):
            t=rels[sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];t=t.lstrip('/') if t.startswith('/') else 'xl/'+t
            rows={}
            for c in E.fromstring(z.read(t)).findall('.//{*}c'):
                col,row=re.match(r'([A-Z]+)(\d+)',c.attrib['r']).groups();v=c.findtext('{*}v','')
                if c.attrib.get('t')=='s' and v:v=strings[int(v)]
                if c.attrib.get('t')=='inlineStr':v=''.join(c.find('{*}is').itertext())
                if v:rows.setdefault(int(row),{})[col]=v
            out[sh.attrib['name']]=rows
        return out
if __name__=='__main__':
    import sys
    for n,r in sheets(sys.argv[1]).items():
        print(n, 'rows',len(r));print(list(r.items())[:4])
