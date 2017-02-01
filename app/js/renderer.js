const { remote, ipcRenderer } = require('electron')
const { BrowserWindow } = remote
const { Menu, MenuItem } = remote

const bb       = require('bluebird')
const fs       = bb.promisifyAll(require('fs'))
const path     = require('path')
const url      = require('url')
const spawn    = require('child_process').spawn
const request  = require('request-promise')
const reader   = new FileReader
const print    = console.log.bind(console)

const Parsers = require('./Parsers')
const allowedFormats = Object.keys(Parsers)

let ctx        = $('#chart')
let chart
let buildingsWindow
let dataChart
// Variables que hacen referencia al path para los ficheros RINEX
let [navFilePath, obsFilePath] = [null, null]
// Función para obtener la proyección de la página epsg.io
const fetchProj   = epsg => request({ uri : `http://epsg.io/${epsg}.proj4` })

const build             =  false //process.env.build === 'true'
//console.log('build', build, typeof build)
const BuildResourcesDir = build ? 'resources/app.asar.unpacked/' : ''

const readFile = f => new Promise((resolve, reject)=>{
    reader.onload = e => resolve(e.target.result)
    reader.onerror = reject
    reader.readAsText(f)
})

$('#btn-calc').click(function(e){
    if(!obsFilePath)
        return Materialize.toast('Debe añadir el fichero RINEX de observación', 2500)
    if(!navFilePath)
        return Materialize.toast('Debe añadir el fichero RINEX de navegación', 2500)
    // Ejecutar python
    //console.log('python start')
    $('#modal-cargando').modal('open')
    buildMenu(true)
    let py = spawn('python',[`${BuildResourcesDir}app/calc/ResolvePosition.py`, obsFilePath, navFilePath])

    py.stdout.on('data', data => console.log('data : ', data.toString()))
    py.on('close', ()=>{
        navFilePath = obsFilePath = null

        $('#modal-cargando').modal('close')
        let jsonPath = build ? '../../app.asar.unpacked/app/calc/results/solucion.json' : 'calc/results/solucion.json'
        $.get(jsonPath, function(data){
            let coords = dataChart = JSON.parse(data.replace(/\'/g, '"'))
            let bbox   = ol.extent.boundingExtent(coords.map( coo => [coo.lon, coo.lat]))

            coords.forEach(function(coord){
                let feature = new ol.Feature({
                    geometry : new ol.geom.Point([coord.lon, coord.lat, coord.h], 'XYZ')
                })
                feature.setProperties(coord)
                layer.getSource().addFeature(feature)
            })

            let coordsLs = coords
                //.sort( (a, b)=> new Date(a.tobs).getTime() - new Date(b.tobs).getTime())
                .map( coo => [coo.lon, coo.lat, coo.h.toFixed(3), (new Date(coo.tobs).getHours()*60*60) + (new Date(coo.tobs).getMinutes() * 60) + new Date(coo.tobs).getSeconds() ])
            //console.log(coordsLs)
            let ls3d = new ol.geom.LineString(coordsLs, 'XYZM')
            profil.setGeometry(ls3d)

            $('.rinex').each(function(idx, el){ el.reset() })
            map.getView().fit(bbox, map.getSize(), { duration : 1000 })
            buildChart()
            buildMenu()
        })
    })
})

$('#btn-aux-data').click(function(e){
    let p = $('#aux-data').get(0).files[0].path
    let extname = path.extname(p).replace('.', '')

    if(allowedFormats.find( format => format == extname)){

        let parser = Parsers[extname]

        parser.fromFile(p, 4326)
        .then( geojson=>{

            let geojsonParser = new ol.format.GeoJSON()
            let features = geojsonParser.readFeatures(geojson, 
                { dataProjection : `EPSG:4326`, featureProjection : 'EPSG:4326' })
            
            layerExtraInfo.getSource().addFeatures(features)

            let coords = features.map(f => f.getGeometry().getCoordinates())
            let bbox = ol.extent.boundingExtent(coords)

            map.getView().fit(bbox, map.getSize())

            return Promise.resolve()

        })
        .then(()=>Materialize.toast('Datos auxiliares añadidos', 2500))
        .catch(()=>Materialize.toast('Error añadiendo datos auxiliares', 2500))

    } else {
        return Materialize.toast(`Formato ${extname} no soportado. Los formatos soportados son : ${allowedFormats.join(', ')}`, 2500)
    }
})

$('#nav-input, #obs-input').change(function(e){
    console.log(e.target.files[0].path)
    // Path absoluto
    let p       = e.target.files[0].path
    let extname = path.extname(p)
    let idElem  = $(this).attr('id')
    //console.log(extname)
    //this.form.reset()

    if(idElem == 'obs-input'){
        if(!extname.match(/\.\d{2}[oO]/)) 
            return Materialize.toast('Debe añadir un fichero con extensión .XXo ó .XXO, por ejemplo .11o', 2500)
        obsFilePath = p
/*
        let fpath = `${BuildResourcesDir}app/calc/data/obs${extname}`
        readFile(e.target.files[0])
        .then(ftext=> fs.writeFile(fpath, ftext))
        .then( ()=>{ obsFilePath = fpath })
        .catch( err =>{ Materialize.toast(`Error : ${err}`, 2500) })
*/

    } else if(idElem == 'nav-input'){
        if(!extname.match(/\.\d{2}[nN]/))
            return Materialize.toast('Debe añadir un fichero con extensión .XXn ó .XXN, por ejemplo .11n', 2500)
        navFilePath = p
/*        
        let fpath = `${BuildResourcesDir}app/calc/data/nav${extname}`
        readFile(e.target.files[0])
        .then(ftext=> fs.writeFile(fpath, ftext))
        .then( ()=>{ navFilePath = fpath })
        .catch( err =>{ Materialize.toast(`Error : ${err}`, 2500) })
*/
    }
    buildMenu()
});

$('#proj-input').keyup(function(e){
    if(e.which === 13){
        let epsg = $(this).val()
        fetchProj(epsg)
        .then( projDef => {
            proj4.defs(`EPSG:${epsg}`, projDef)

            let format = getFormat(projDef)
            let proj = ol.proj.get(`EPSG:${epsg}`)

            mousePositionControl.setProjection(proj)
            mousePositionControl.setCoordinateFormat(format)
            $(this).val('')
            $('#modal-select-proj').modal('close')
        })        
        .catch( err=>{ Materialize.toast(`Error : ${err}`, 2500) })
    }
})

$('#modal-chart').modal({
      ready : createChart
})

function getFormat(projDef){
    if(projDef.match(/\+proj=longlat/)) 
        return coordinate => ol.coordinate.toStringHDMS(coordinate, 2)
    return coordinate => ol.coordinate.toStringXY(coordinate, 3)

}

function buildChart(){
    fetchProj('25830')
    .then(projDef =>{
        proj4.defs('EPSG:25830', projDef)
        let proj = ol.proj.get('EPSG:25830')
        dataChart = dataChart.map( point =>{
            //print(point)
            let [x, y] = ol.proj.transform([point.lon, point.lat], 'EPSG:4326', 'EPSG:25830') 
            return {x, y}
        })
    })
}

function createChart(){
    chart = new Chart(document.getElementById('chart'), {
            type : 'line'
        , data : {
            datasets : [{
                  label : 'Plot X, Y'
                , data : dataChart
                , fill : false
                , pointRadius : 0.5
            }]
        }
        , options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    })
}

function openBuildingsWindow(){

    if(buildingsWindow) return

    let child = buildingsWindow = new BrowserWindow({parent : remote.getCurrentWindow(), modal: false, show: false})

    buildMenu()

    child.loadURL(url.format({
        pathname: path.join(__dirname, '../buildings.html'),
        protocol: 'file:',
        slashes: true
    }))
    //child.webContents.openDevTools()
    child.setMenu(null)
    let [listenerCenter, listenerResolution, listenerRotation] = [];
    let listenerIpc = function(event, view){
        map.getView().set('center', [view.center.longitude, view.center.latitude], true)
        map.getView().set('zoom', view.zoom, true)
        map.getView().set('rotation', view.rotation, true)
    }

    ipcRenderer.on('child-change-view', listenerIpc)
    child.once('ready-to-show', () => {
        child.show()
        let view = map.getView()
        let [center, zoom, rotation] = [view.getCenter(), view.getZoom(), view.getRotation()]
        ipcRenderer.send('main-change-view', {center, zoom, rotation})

        listenerCenter = map.getView().on('change:center', change);
        listenerResolution = map.getView().on('change:resolution', change);
        listenerRotation = map.getView().on('change:rotation', change);

        function change(){
            console.log('seeend to child')
            let view = map.getView()
            let [center, zoom, rotation] = [view.getCenter(), view.getZoom(), view.getRotation()]
            ipcRenderer.send('main-change-view', {center, zoom, rotation})
        }
    })

    child.on('close', ()=>{
        map.getView().unByKey(listenerCenter)
        map.getView().unByKey(listenerResolution)
        map.getView().unByKey(listenerRotation)
        ipcRenderer.removeListener('main-change-view', listenerIpc)
        buildingsWindow = null;
        buildMenu()
    })
}

// Función para crear/actualizar el menú principal
const buildMenu = disabled =>{
    let enabled = !disabled
    let menu     = Menu.buildFromTemplate([{   
        label   : 'Opciones'
        , submenu : [
            { label : 'Añadir ficheros', click(){ $('#modal-select-archivos').modal('open') }, enabled : enabled },
            { label : 'Añadir datos auxiliares', click(){ $('#modal-select-aux').modal('open') }, enabled : enabled },
            { label : 'Calcular', click(){ $('#btn-calc').trigger('click') }, enabled : enabled && obsFilePath && navFilePath ? true : false },
            { label : 'Gráficos', click(){ $('#modal-chart').modal('open') }, enabled : enabled && dataChart ? true : false },
            { label : 'Edificios', click(){ openBuildingsWindow() }, enabled : buildingsWindow == null },
            { label : 'Configuración', click(){ $('#modal-select-proj').modal('open') }, enabled }
        ]
    },{
        label : 'Acerca de...',
        click(){
            let child = new BrowserWindow({parent : remote.getCurrentWindow(), modal: true, show: false})
            child.setMenu(null)
            child.loadURL(url.format({
                pathname: path.join(__dirname, '../about.html'),
                protocol: 'file:',
                slashes: true
            }))
            child.webContents.openDevTools()
            child.once('ready-to-show', () => {
                child.show()
            })
        }
    }])
    Menu.setApplicationMenu(menu)
}
buildMenu()