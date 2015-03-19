##parameters=url

xsl_db="file:///usr/share/xml/docbook/stylesheet/nwalsh/html/pt_docbook.xsl"
try:
  chemin_doc='/' + url.split('//')[1].split('/', 1)[1]
except:
  chemin_doc = url


doc_db=context.exist.query(str(container.view_direct_xml_xq).replace('$DOC', chemin_doc.strip()))

return context.exist.getDoc(doc_db, xsl=xsl_db, xsl_base_uri='/usr/share/xml/docbook/stylesheet/nwalsh/', object_only=1, stylesheet_param=container.getDocbookOptions())