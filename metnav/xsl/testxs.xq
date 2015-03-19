xquery version "%(xquery_version)s";
declare default collation "?lang=fr-FR;strength=primary;decomposition=standard";
declare namespace ld="http://namespaces.ens-lyon.fr/livredoc/";
declare namespace lom="http://ltsc.ieee.org/xsd/LOM";
declare namespace transform="http://exist-db.org/xquery/transform";
declare namespace xsl="http://www.w3.org/1999/XSL/Transform";
declare namespace util="http://exist-db.org/xquery/util";
let $results :=  document('/db/tests/userguide.xml')
return transform:transform($results, doc("file:///home/spilloz/Dev/workcopy/python/MetNav/xsl/docbook/docbook-xsl-1.71.1/html/docbook.xsl"), ())
(:: return transform:transform($results, document("/db/xsl/docbook/html/docbook.xsl"), ()) ::)