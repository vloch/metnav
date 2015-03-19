xquery version "%(xquery_version)s";
declare namespace ld="http://namespaces.ens-lyon.fr/livredoc/";
declare namespace lom="http://ltsc.ieee.org/xsd/LOM";
declare namespace transform="http://exist-db.org/xquery/transform";
declare namespace xsl="http://www.w3.org/1999/XSL/Transform";
declare namespace util="http://exist-db.org/xquery/util";
let $results := <results>{subsequence(
for $res in collection('/db/planetterre/metadata')/lom:lom[lom:educational/lom:learningResourceType &= "figure"]
order by $res/lom:metaMetadata/lom:contribute[lom:role='creator' or lom:role='createur'][1]/lom:date/lom:dateTime descending empty least
return
<res url="{document-uri($res)}">{$res}</res>, 1, 10)
}</results>
return transform:transform($results, "xmldb:exist:///db/xsl/lom2table.xsl",<parameters><param name="rss.copyright" value="Mon établissement" /><param name="rss.title" value="Nouveautés du site" /><param name="url.img" value="/XML" /><param name="url.server" value="http://localhost:9090/test" /><param name="rss.language" value="en" /><param name="site.webmaster" value="postmaster@localhost" /><param name="rss.desc" value="Toutes les nouveautés du site" /><param name="site.editor" value="postmaster@localhost" /><param name="url.doc.hide" value="/voir_xml?url" /><param name="url.doc" value="/XML" /><param name="elements.by.line" value="3" /></parameters>)


