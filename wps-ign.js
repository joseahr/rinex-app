const request = require('request-promise');
const print = console.log.bind(console)

const data = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <wps:Execute service="WPS" version="0.4.0" store="false" status="false" 
        xmlns:wps="http://www.opengeospatial.net/wps" 
        xmlns:ows="http://www.opengis.net/ows" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="http://www.opengeospatial.net/wps..wpsExecute.xsd"> 
        <ows:Identifier>GetProfileTxt</ows:Identifier> 
        <wps:DataInputs> 
            <wps:Input> 
                <ows:Identifier>Resolution</ows:Identifier> 
                <ows:Title>Resolution</ows:Title> 
                <ows:Abstract>Resolution</ows:Abstract> 
                <wps:LiteralValue dataType="urn:ogc:def:dataType:OGC:0.0:Double" uom="urn:ogc:def:dataType:OGC:0.0:Double">100</wps:LiteralValue> 
            </wps:Input> 
            <wps:Input> 
            <ows:Identifier>Profile</ows:Identifier> 
            <ows:Title>Profile</ows:Title> 
            <ows:Abstract>Profile</ows:Abstract> 
            <wps:LiteralValue dataType="urn:ogc:def:dataType:OGC:0.0:String" uom="urn:ogc:def:dataType:OGC:0.0:String"> 
                720881.20793,4737909.94751,720861.25339,4737944.15525,720835.59756,4737961.25911,720701.61714,
                4738021.12259,720681.6626,4738049.62904,720607.54577,4738086.68739,720584.7406,4738095.23932,720533.42897,
                4738086.68734,720524.87706,4738052.47958,720507.7732,4738021.12246,720487.81868,4738009.71986,
                720456.46158,4737995.46661,720422.25384,4737975.51206,720388.0461,4737958.40816,720385.19546,
                4737952.70686,720311.07866,4737944.15487,720288.27351,4737921.34969,720288.27352,
                4737898.54452,720285.42289,4737875.73934,720271.16967,4737855.78481,720268.31905,4737830.12899,
                720268.31906,4737804.47317,720271.16972,4737787.3693,720251.21521,4737773.11605,720228.41004,
                4737773.11604,720202.75422,4737778.81731,720188.501,4737753.16148,720162.84519,4737741.75888,
                720137.1894,4737707.55111,720128.63747,4737690.44722,720105.83232,4737673.34333,720083.02716,
                4737650.53814,720045.96877,4737641.98618,720043.11813,4737622.03165,720023.16363,4737599.22647,720000.35846,
                4737584.97322,719966.15071,4737582.12255,719946.19619,4737576.42124 
            </wps:LiteralValue> 
            </wps:Input> 
            <wps:Input> 
                <ows:Identifier>URLCoverageServer</ows:Identifier> 
                <ows:Title>URLCoverageServer</ows:Title> 
                <ows:Abstract>URLCoverageServer</ows:Abstract> 
                <wps:LiteralValue dataType="urn:ogc:def:dataType:OGC:0.0:String" uom="urn:ogc:def:dataType:OGC:0.0:String"> 
                    http://www.ign.es/wcs/mdt?SERVICE=WCS&REQUEST=GetCoverage&VERSION=1.0.0&CRS=EPSG:25830&BBOX=719153.7163877804,4736940.727420838,721662.2850917999,4738636.86200795&COVERAGE=mdt:Elevacion25830_25&RESX=25&RESY=25&EXCEPTIONS=XML&FORMAT=ArcGrid                
                </wps:LiteralValue> 
            </wps:Input> 
            <wps:Input> 
                <ows:Identifier>CRS</ows:Identifier> 
                <ows:Title>CRS</ows:Title> 
                <ows:Abstract>CRS</ows:Abstract> 
                <wps:LiteralValue dataType="urn:ogc:def:dataType:OGC:0.0:String" uom="urn:ogc:def:dataType:OGC:0.0:String">EPSG:23030</wps:LiteralValue> 
            </wps:Input> 
        </wps:DataInputs> 
        <wps:OutputDefinitions> 
            <wps:Output format="text/xml" encoding="UTF-8" schema="http://schemas.opengis.net/gml/3.0.0/base/gml.xsd" uom="urn:ogc:def:dataType:OGC:0.0:Integer"> 
                <ows:Identifier>Profile</ows:Identifier> 
                <ows:Title>Profile</ows:Title> 
                <ows:Abstract>Profile</ows:Abstract> 
            </wps:Output> 
        </wps:OutputDefinitions> 
    </wps:Execute>
`;

const options = {
      method : 'POST'
    , uri : 'http://www.ign.es/wps-analisis/servicios?'
    , headers : {
        'Content-Type' : 'text/xml'
    }
    , body : encodeURIComponent(data)

};


const urlWPSIGN = 'http://www.ign.es/wps-analisis/servicios'
const describeProcess = process => request({ uri : `${urlWPSIGN}?request=DescribeProcess&service=WPS&Identifier=${process}&version=0.4.0` })



request(options).then(print).catch(print)

