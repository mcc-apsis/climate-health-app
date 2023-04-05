table2Tree = function(data, attribs, value = undefined) {
  const valueFn = v =>
    value === undefined
      ? v.length // Default value count nodes
      : value instanceof Function // If value is a function just pass it
      ? value(v)
      : d3.sum(v, d => +d[value]); // If value is not a function assume it is an attribute and sum it

  return rollupsToTree(
    d3.rollups(...[data, valueFn].concat(...attribs.map(a => d => d[a])))
  );
}

rollupsToTree = function(rollupsData) {
  const makeTreeNode = d => {
    let res = {
      name: d[0]
    };

    if (Array.isArray(d[1])) res.children = rollupsToTree(d[1]);
    else res.value = d[1];
    return res;
  };

  function rollupsToTree(groupedData) {
    if (!groupedData) return;

    return groupedData.map(makeTreeNode);
  }

  return {
    name: "",
    children: Array.isArray(rollupsData)
      ? rollupsToTree(rollupsData)
      : [{ name: "", value: rollupsData }]
  };
}


function draw_topics(data,width){
    
    data.treeData = table2Tree(data.hierarchy, 'l1 l2 l3'.split(' '), v => d3.sum(v, d => parseFloat(d.id)))
    


var shift = d3.select('.mainCanvas').node().offsetLeft
    var svg = d3.select("#topicselector").attr('transform',`translate(${shift},0)`).style('opacity',0)
    .attr("width", width).attr("height", width)

    // d3.select('#container').remove()

var i = 0,
    duration = 750,
    slide=30,
    root;

// declares a tree layout and assigns the size
var treemap = d3.tree().size([height, width]);

// Assigns parent, children, height, depth
root = d3.hierarchy(data.treeData, function(d) { return d.children; });
root.x0 = height / 2;
root.y0 = 0;

// Collapse after the second level
//root.children.forEach(collapse);

update(root);


function update(source) {

  // Assigns the x and y position for the nodes
  data.treeData = treemap(root);

  // Compute the new tree layout.
  var nodes = data.treeData.descendants(),
      links = data.treeData.descendants().slice(1);
      
  data.topicfilter = nodes.filter(d=> !d.ignore & d.depth===3)
  sliderchange()


  // Normalize for fixed-depth.
  nodes.forEach(function(d){ d.y = d.depth * 180; 
      //d.children = d.children||true
  });

  // ****************** Nodes section ***************************

  // Update the nodes...
  var node = svg.selectAll('g.node')
      .data(nodes, function(d) {return d.id || (d.id = ++i); });

  // Enter any new modes at the parent's previous position.
  var nodeEnter = node.enter().append('g')
      .attr('class', 'node')
      .attr("transform", function(d) {
        return "translate(" + source.y0 + "," + source.x0 + ")";
    })
    .on('click', click);

  // Add Circle for the nodes
  nodeEnter.append('circle')
      .attr('class', 'node')
      .attr('r', 1e-6)
      .style("fill", function(d) {
          return d._children ? "grey" : "#fff";
      });

  // Add labels for the nodes
  nodeEnter.append('text')
      .attr("dy", ".35em")
      .attr("x", function(d) {
          return d.children || d._children ? -13 : 13;
      })
      .attr("text-anchor", function(d) {
          return d.children || d._children ? "end" : "start";
      })
      .text(function(d) { return d.data.name; });

  // UPDATE
  var nodeUpdate = nodeEnter.merge(node);

  // Transition to the proper position for the node
  nodeUpdate.transition()
    .duration(duration)
    .attr("transform", function(d) { 
        return "translate(" + (d.y+slide) + "," + d.x + ")";
     });

  // Update the node attributes and style
  nodeUpdate.select('circle.node')
    .attr('r', d=>(4-d.depth)*5)
    .style("fill", function(d) {
        return d._children ? "grey" : "#fff";
    })
    .attr('cursor', 'pointer');


  // Remove any exiting nodes
  var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) {
          return "translate(" + (source.y+slide) + "," + source.x + ")";
      })
      .remove();

  // On exit reduce the node circles size to 0
  nodeExit.select('circle')
    .attr('r', 1e-6);

  // On exit reduce the opacity of text labels
  nodeExit.select('text')
    .style('fill-opacity', 1e-6);

  // ****************** links section ***************************

  // Update the links...
  var link = svg.selectAll('path.link')
      .data(links, function(d) { return d.id; });

  // Enter any new links at the parent's previous position.
  var linkEnter = link.enter().insert('path', "g")
      .attr("class", "link")
      .attr('d', function(d){
        var o = {x: source.x0, y: source.y0}
        return diagonal(o, o)
      });

  // UPDATE
  var linkUpdate = linkEnter.merge(link);

  // Transition back to the parent element position
  linkUpdate.transition()
      .duration(duration)
      .attr('d', function(d){ return diagonal(d, d.parent) });

  // Remove any exiting links
  var linkExit = link.exit().transition()
      .duration(duration)
      .attr('d', function(d) {
        var o = {x: source.x, y: source.y}
        return diagonal(o, o)
      })
      .remove();

  // Store the old positions for transition.
  nodes.forEach(function(d){
    d.x0 = d.x;
    d.y0 = d.y;
  });



}
          





// Creates a curved (diagonal) path from parent to the child nodes
function diagonal(s, d) {

  path = `M ${s.y} ${s.x}
          C ${(s.y + d.y) / 2} ${s.x},
            ${(s.y + d.y) / 2} ${d.x},
            ${d.y} ${d.x}`

  return path
}



// Collapse the node and all it's children
function collapse(d) {
  if(d.children) {
    d._children = d.children
    d._children.forEach(collapse)
    d.children = null
  }
}

// Toggle children on click.
function click(d) {
// console.log(d,this,d3.select(this).select('circle').node(),d.ignore)
  if (d.depth===0){return false}
  
  // select end 
  if (d.children === undefined){
      if (d.ignore){
          d3.select(this).select('circle').style('stroke','steelblue')
           d3.select(this).select('text').style('opacity','1')
          d.ignore = false
      }else{
          d3.select(this).select('circle').style('stroke','#222')
           d3.select(this).select('text').style('opacity','0.2')
          d.ignore=true
          
      }
      
      return update(d)
  }
  
  
  if (d.children) {      
      d._children = d.children;
      d.children = null;
      d3.select(this).select('circle').style('stroke','#222')
    } else {
      d.children = d._children.map(e=>{e.ignore=false;return e});
      d._children = null;
      d3.select(this).select('circle').style('stroke','steelblue')
    }
  update(d);
}


}