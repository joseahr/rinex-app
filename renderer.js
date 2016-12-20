// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
const bb       = require('bluebird')
const fs       = bb.promisifyAll(require('fs'))
const path     = require('path')
const spawn    = require('child_process').spawn
const request  = require('request-promise')
const reader   = new FileReader

const print = console.log.bind(console)
let [navFilePath, obsFilePath] = [null, null]
const projections = {}
const getProjStrUrl = epsg => `http://epsg.io/${epsg}.proj4`
const fetchProjWKT = epsg => request({ uri : getProjStrUrl(epsg) })

const readFile = f => new Promise((resolve, reject)=>{
    reader.onload = e => resolve(e.target.result)
    reader.onerror = reject
    reader.readAsText(f)
})
/*
const calcBBOX = data => data.reduce( (bbox, coord, idx)=>{
    if(coord.lon < bbox[0]) bbox[0] = coord.lon
    else if(coord.lon > bbox[2]) bbox[2] = coord.lon

    if(coord.lat < bbox[1]) bbox[1] = coord.lat
    else if(coord.lat > bbox[3]) bbox[3] = coord.lat

    return bbox
}, [Number.MAX_VALUE, Number.MAX_VALUE, Number.MIN_VALUE, Number.MIN_VALUE]) //Xmin, Ymin, Xmax, Ymax
//.map( (pt, index)=> ( (index + 1) < 2 ? pt - 0.00001 : pt + 0.00001))
*/

$('#btn-calc').click(function(e){
    if(!obsFilePath)
        return Materialize.toast('Debe añadir el fichero RINEX de observación', 2500)
    if(!navFilePath)
        return Materialize.toast('Debe añadir el fichero RINEX de navegación', 2500)
    // Ejecutar python
    console.log('python start')
    $('#modal-cargando').modal('open')
    let py = spawn('python',['resources/app.asar.unpacked/calc/ResolvePosition.py', obsFilePath, navFilePath])
    py.stdout.on('data', data => console.log('data : ', data.toString()))
    py.on('close', ()=>{
        console.log('Fin')
        $('#modal-cargando').modal('close')
        $.get('../app.asar.unpacked/calc/results/solucion.json', function(data){
            let coords = JSON.parse(data.replace(/\'/g, '"'))
            let bbox   = ol.extent.boundingExtent(coords.map( coo => [coo.lon, coo.lat]))
            print(bbox)
            coords.forEach(function(coord){
                let feature = new ol.Feature({
                    geometry : new ol.geom.Point([coord.lon, coord.lat])
                })
                layer.getSource().addFeature(feature)
            })
            navFilePath = obsFilePath = null
            $('.rinex').each(function(idx, el){ el.reset() })
            map.getView().fit(bbox, map.getSize(), { duration : 1000 })
        })
    })
})

$('input[type=file]').change(function(e){
    // Path absoluto
    let p       = $(this).val()
    let extname = path.extname(p)
    let idElem  = $(this).attr('id')
    //console.log(extname)
    //this.form.reset()

    if(idElem == 'obs-input'){
        if(!extname.match(/\.\d{2}[oO]/)) 
            return Materialize.toast('Debe añadir un fichero con extensión .XXo ó .XXO, por ejemplo .11o', 2500)

        let fpath = `resources/app.asar.unpacked/calc/data/obs${extname}`
        readFile(e.target.files[0])
        .then(ftext=> fs.writeFile(fpath, ftext))
        .then( ()=>{ obsFilePath = fpath })
        .catch( err =>{ Materialize.toast(`Error : ${err}`, 2500) })
        
    } else {
        if(!extname.match(/\.\d{2}[nN]/))
            return Materialize.toast('Debe añadir un fichero con extensión .XXn ó .XXN, por ejemplo .11n', 2500)
        
        let fpath = `resources/app.asar.unpacked/calc/data/nav${extname}`
        readFile(e.target.files[0])
        .then(ftext=> fs.writeFile(fpath, ftext))
        .then( ()=>{ navFilePath = fpath })
        .catch( err =>{ Materialize.toast(`Error : ${err}`, 2500) })
    }
});

$('#proj-input').keyup(function(e){
    if(e.which === 13){
        let epsg = $(this).val()
        fetchProjWKT(epsg)
        .then( projDef => {
            proj4.defs(`EPSG:${epsg}`, projDef)
            let proj = ol.proj.get(`EPSG:${epsg}`)
            print(projDef, proj)
            mousePositionControl.setProjection(proj)
            $(this).val('')
            $('#modal-select-proj').modal('close')
        })        
        .catch( err=>{ Materialize.toast(`Error : ${err}`, 2500) })
    }
})