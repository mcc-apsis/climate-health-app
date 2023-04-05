

function legend(keys,color){
    //console.log(keys,color)
    var keys = keys.filter(d=>d)
    var s = d3.select("#overlay")
    
    s.selectAll('.legend').remove()
    
    sg = s.append('g').classed('legend',true)

// Add one dot in the legend for each name.
sg.selectAll("ldot")
  .data(keys)
  .enter()
  .append("circle")
  .classed('legend',true)
    .attr("cx", 20)
    .attr("cy", function(d,i){ return 30 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
    .attr("r", 3)
    .style('float','right')
    .style("fill", function(d){ return color(d)})

// Add one dot in the legend for each name.
sg.selectAll("llab")
  .data(keys)
  .enter()
  .append("text")
   .classed('legend',true)
    .attr("x",30)
    .attr("y", function(d,i){ return 30 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
    .style("fill", function(d){ return color(d)})
    .text(function(d){ return d})
    .attr("text-anchor", "left")
    .style("alignment-baseline", "middle")
    
    
    
}