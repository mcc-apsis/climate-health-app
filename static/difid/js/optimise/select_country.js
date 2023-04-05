var continentmap = {
    "South America": "SA",
    Oceania: "OC",
    "North America": "NA",
    Europe: "EU",
    Asia: "AS",
    Africa: "AF"
};

function draw_world(topology) {
    var graticule = d3.geoGraticule();
    var shift = d3.select(".mainCanvas").node().offsetLeft;
    var svg = d3
        .select("#countryselector")
        .attr("transform", `translate(${shift},0)`)
        .style("opacity", 0)
        .attr("width", width)
        .attr("height", height);

    svg.selectAll("g").remove();
    var g = svg.append("g");

    //https://bl.ocks.org/mbostock/3710082
    var projection = d3
        .geoPeirceQuincuncial()
        .fitSize([width, height], { type: "Sphere" })
        .rotate([20, -90, 45])
        .precision(0.1);

    var path = d3.geoPath().projection(projection);

    svg
        .append("path")
        .datum(graticule)
        .attr("class", "graticule")
        .attr("fill", "none")
        .attr("stroke", "#222")
        .attr("opacity", 0.13)
        .attr("d", path);

    var continents = topojson.feature(topology, topology.objects.continent)
        .features;

    var centroids = continents.map(function(d) {
        return projection(d3.geoCentroid(d));
    });

    svg
        .selectAll(".continent")
        .data(continents)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("title", function(d, i) {
            return d.properties.continent;
        })
        .attr("id", d => continentmap[d.properties.continent])
        .attr("stroke", d =>
            d3
                .color(cmap(continentmap[d.properties.continent]))
                .darker(0.4)
                .toString()
        )
        .on("click", d => clist(continentmap[d.properties.continent]))
        .style("fill", function(d, i) {
            return cmap(continentmap[d.properties.continent]);
        });

    svg
        .selectAll(".name")
        .data(centroids)
        .enter()
        .append("text")
        .attr("x", function(d) {
            return d[0];
        })
        .attr("y", function(d) {
            return d[1];
        })
        .style("font-family", "BalooDa")
        .style("fill", "whitesmoke")
        .attr("text-anchor", "middle")
        .text(function(d, i) {
            return continents[i].properties.continent;
        })
        .style("pointer-events", "none");

    svg
        .append("text")
        .attr("x", 10)
        .attr("y", 20)
        .text(
            "Click on continents to deselect/select them - then click on the red tab to return to previous plot"
        )
        .style("font-family", "BalooDa")
        .style("fill", "#222")
        .attr("text-anchor", "left");
}

function clist(t) {
    // contenent list

    data.continentselection =
        data.continentselection || Object.values(continentmap);

    cnt = d3.selectAll("#" + t);

    if (data.continentselection.includes(cnt.attr("id"))) {
        data.continentselection = data.continentselection.filter(
            e => e != cnt.attr("id")
        );
        cnt.attr("opacity", 0.3);
    } else {
        data.continentselection.push(cnt.attr("id"));
        cnt.attr("opacity", 1);
    }
    showcselect();
}

function showcselect() {
    context.clearRect(0, 0, width, height);

    sliderchange();
}
