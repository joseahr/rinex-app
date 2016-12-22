const { remote } = require('electron')
const { Menu, MenuItem } = remote
const bb       = require('bluebird')
const fs       = bb.promisifyAll(require('fs'))
const path     = require('path')
const spawn    = require('child_process').spawn
const request  = require('request-promise')
const reader   = new FileReader
const print    = console.log.bind(console)

let ctx        = $('#chart')
let chart
let dataChart
// Variables que hacen referencia al path para los ficheros RINEX
let [navFilePath, obsFilePath] = [null, null]
// Función para obtener la proyección de la página epsg.io
const fetchProj   = epsg => request({ uri : `http://epsg.io/${epsg}.proj4` })

const build             = false
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
    console.log('python start')
    $('#modal-cargando').modal('open')
    buildMenu(true)
    let py = spawn('python',[`${BuildResourcesDir}calc/ResolvePosition.py`, obsFilePath, navFilePath])

    navFilePath = obsFilePath = null
    buildMenu()

    py.stdout.on('data', data => console.log('data : ', data.toString()))
    py.on('close', ()=>{
        $('#modal-cargando').modal('close')
        let jsonPath = build ? '../app.asar.unpacked/calc/results/solucion.json' : 'calc/results/solucion.json'
        $.get(jsonPath, function(data){
            let coords = dataChart = JSON.parse(data.replace(/\'/g, '"'))
            let bbox   = ol.extent.boundingExtent(coords.map( coo => [coo.lon, coo.lat]))
            coords.forEach(function(coord){
                let feature = new ol.Feature({
                    geometry : new ol.geom.Point([coord.lon, coord.lat])
                })
                feature.setProperties(coord)
                layer.getSource().addFeature(feature)
            })
            $('.rinex').each(function(idx, el){ el.reset() })
            map.getView().fit(bbox, map.getSize(), { duration : 1000 })
            buildChart()
            buildMenu()
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

        let fpath = `${BuildResourcesDir}calc/data/obs${extname}`
        readFile(e.target.files[0])
        .then(ftext=> fs.writeFile(fpath, ftext))
        .then( ()=>{ obsFilePath = fpath })
        .catch( err =>{ Materialize.toast(`Error : ${err}`, 2500) })
        
    } else {
        if(!extname.match(/\.\d{2}[nN]/))
            return Materialize.toast('Debe añadir un fichero con extensión .XXn ó .XXN, por ejemplo .11n', 2500)
        
        let fpath = `${BuildResourcesDir}calc/data/nav${extname}`
        readFile(e.target.files[0])
        .then(ftext=> fs.writeFile(fpath, ftext))
        .then( ()=>{ navFilePath = fpath })
        .catch( err =>{ Materialize.toast(`Error : ${err}`, 2500) })
    }
    buildMenu()
});

$('#proj-input').keyup(function(e){
    if(e.which === 13){
        let epsg = $(this).val()
        fetchProj(epsg)
        .then( projDef => {
            proj4.defs(`EPSG:${epsg}`, projDef)
            let proj = ol.proj.get(`EPSG:${epsg}`)
            mousePositionControl.setProjection(proj)
            $(this).val('')
            $('#modal-select-proj').modal('close')
        })        
        .catch( err=>{ Materialize.toast(`Error : ${err}`, 2500) })
    }
})

$('#modal-chart').modal({
      ready : createChart
})

function buildChart(){
    fetchProj('25830')
    .then(projDef =>{
        proj4.defs('EPSG:25830', projDef)
        let proj = ol.proj.get('EPSG:25830')
        dataChart = dataChart.map( point =>{
            print(point)
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

// Función para crear/actualizar el menú principal
const buildMenu = disabled =>{
    let enabled = !disabled
    let menu     = Menu.buildFromTemplate([{   
        label   : 'Opciones'
        , submenu : [
            { label : 'Añadir ficheros', click(){ $('#modal-select-archivos').modal('open') }, enabled : enabled },
            { label : 'Calcular', click(){ $('#btn-calc').trigger('click') }, enabled : obsFilePath && navFilePath ? true : false },
            { label : 'Gráficos', click(){ $('#modal-chart').modal('open') }, enabled : dataChart ? true : false },
            { label : 'Configuración', click(){ $('#modal-select-proj').modal('open') }, enabled }
        ]
    },{
        label : 'Acerca de...',
        enabled
    }])
    Menu.setApplicationMenu(menu)
}
buildMenu()