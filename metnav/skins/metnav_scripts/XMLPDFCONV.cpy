context.REQUEST.RESPONSE.setHeader('Content-type','application/pdf')
context.REQUEST.RESPONSE.setHeader('Content-disposition','attachment; filename="%s.pdf"' % ( 'article' ) )
return context.restrictedTraverse("XMLPDFCONVVIEW").get_pdf(traverse_subpath)
