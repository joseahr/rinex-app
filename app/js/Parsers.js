const readFile = require('bluebird').promisify(require('fs').readFile)

const Exec = require('bluebird').promisify(require('child_process').exec);

const path = require('path');


const parsers = {
    shp : {
        fromFile(path_, epsg){
            path_ = path.normalize(path_);
            let geojsonPath = path_.replace('.shp', '.geojson')
            return Exec(`ogr2ogr -f GeoJSON -t_srs EPSG:${epsg} ${geojsonPath} ${path_}`, {})
                .then( ()=>{
                    return readFile(geojsonPath, { encoding : 'utf-8' })
                    .then(text => JSON.parse(text));
                });
        },
    },
    csv : {
        fromFile(path_, delimiter){
            return readFile(path_, { encoding : 'utf-8' })
            .then(text => this.fromText(text, delimiter) )
        },
        fromText(text, delimiter){
            if(!delimiter) delimiter = ','
            //console.log(text)
            let lines = text.split('\n')
            console.log(lines)
            let parsed = lines.map(line => line.trim().split(delimiter).map(el=>{
                let number = parseFloat(el)
                return number ? number : el
            }))
            .filter(line => line.length > 4)
            console.log(parsed)
            return parsed
        }
    }
}

/*parsers.shp.fromFile('C:\\Users\\Jose\\Desktop\\SHP\\pedreguer.shp', 25830)
.then(console.log.bind(console))
.catch(console.log.bind(console))*/

module.exports = parsers;