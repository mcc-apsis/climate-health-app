var map;

function setMap(){
    
    var w = d3
        .select('#world')
        .style("width", width)
        .style("height", height)
        .style("left", `${(window.innerWidth - width) / 2}`);
        

        
    map = L.map('world',{ zoomControl: false }).setView([-0.2858, 0.7068], 1);
    mapLink = 
        '<a href="https://openstreetmap.org">OpenStreetMap</a>';
    L.tileLayer(
        'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; ' + mapLink + ' | DIFID | CEMAC   <br> '+'',
        maxZoom: 17,
        minZoom:1
        }).addTo(map);
        
    map.dragging.disable();  
    


    // map.on("viewreset", function () {
    //     draw();
    // });
    // 
    map.on('zoomstart',function(){context.clearRect(0,0,width,height)})
    map.on('zoomend',draw)
    
        // w.node().innerHTML += '<button type="button" onclick="map._resetView([-0.2858, 0.7868], 1);draw()" class="recentre">ReCentre Map</button>'
    
    w.append('button')
     .classed('recentre',true)
     .text('ReCentre')
     .on('click',function(){map._resetView([-0.2858, 0.7868], 1);draw()})
    
    
}
        
            
    /* Initialize the SVG layer */
    // map._initPathRoot()    

//     /* We simply pick up the SVG from the map object */
//     var svg = d3.select("#world").select("svg"),
//     g = svg.append("g");
// 
// 
// /* Add a LatLng object to each item in the dataset */
// collection.objects.forEach(function(d) {
//     d.LatLng = new L.LatLng(d.circle.coordinates[0],
//                             d.circle.coordinates[1])
// })
// 
// var feature = g.selectAll("circle")
//     .data(collection.objects)
//     .enter().append("circle")
//     .style("stroke", "black")  
//     .style("opacity", .6) 
//     .style("fill", "red")
//     .attr("r", 20);  

// map.on("viewreset", update);
// update();
// 
// function update() {
//     draw(true)
//     d3.select({}).transition()
//       .duration(1500)
//       .ease(d3.easeCubicInOut)//.ease(Math.sqrt)
//       .tween("link", function(i) {
//           console.log('adding links')
//           //var g0 = document.getElementById('graph0')
//           //g0.style.opacity=0.5
//           g.nodes.documents.visible=true
//           g.links.visible=false
//           g.nodes.topics.visible=false
//           return function (i){
//           color3d()
//           g.nodes.documents.children.forEach(d=>d.material.opacity=i*.8)
//       }
// 
//       });
// 
// 
// 
//     feature.attr("transform", 
//     function(d) { 
//         return "translate("+ 
//             map.latLngToLayerPoint(d.LatLng).x +","+ 
//             map.latLngToLayerPoint(d.LatLng).y +")";
//         }
//     )
//  }
// 
// 
// 
// 
// 
// test = {"objects":[
// {"circle":{"coordinates":[-41.28,174.77]}},
// {"circle":{"coordinates":[-41.29,174.76]}},
// {"circle":{"coordinates":[-41.30,174.79]}},
// {"circle":{"coordinates":[-41.27,174.80]}},
// {"circle":{"coordinates":[-41.29,174.78]}}
// ]}
