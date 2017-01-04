console.log(process.versions.node)
const readFile = require('bluebird').promisify(require('fs').readFile)
const path = require('path')
const shp = require('gtran-shapefile')



module.exports = {
    shp : {
        fromFile(path_){
            return shp.toGeoJson(path_)
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