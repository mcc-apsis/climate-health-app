function canvasmove(ev) {
    if (ev) {
        var mouseX = ev.layerPoint.x;
        var mouseY = ev.layerPoint.y;
    } else {
        var mouseX = d3.event.layerX || d3.event.offsetX;
        var mouseY = d3.event.layerY || d3.event.offsetY;
    }

    var col = hiddencontext.getImageData(mouseX, mouseY, 1, 1).data;
    var colKey = "rgb(" + col[0] + "," + col[1] + "," + col[2] + ")";
    var nodeData = data.nodeclr[colKey];
    try {
        var doc = data.info.get("" + nodeData);
        title.text(doc.title);
        // tool
        // 	.style('opacity', 0.98)
        // 	.style('top', d3.event.pageY < halfwidth ? halfwidth:0)
        // 	.style('left',d3.event.pageX < halfwidth ? halfwidth:0)
        //     //.style('left', d3.event.pageX + 5 + 'px')
        // 	.html('Name: ' + doc.title + '<br>' + 'Content: ' + doc + '<br>' );
    } catch (e) {
        tool.style("opacity", 0);
    }
    //

    if (!data.carto) {
        if (imageData != undefined) {
            //reset image
            context.putImageData(imageData, 0, 0);
        } else {
            //copy image
            imageData = context.getImageData(0, 0, width, height);
        }

        context.save()
        var x = mouseX, y = mouseY;
        context.globalAlpha=1;
        context.strokeStyle='#222';
        context.beginPath();
        context.lineWidth = 2;
        context.moveTo(x - 4, y - 4);
        context.lineTo(x + 4, y + 4);
        context.moveTo(x + 4, y - 4);
        context.lineTo(x - 4, y + 4);
        context.stroke();
        context.beginPath();
        context.lineWidth = 1.5;
        context.arc(x, y, 20, 0, 2 * Math.PI);
        context.stroke();
        context.restore();
    }
}

function canvasdblclick(ev) {
    if (ev) {
        var mouseX = ev.layerPoint.x;
        var mouseY = ev.layerPoint.y;
    } else {
        var mouseX = d3.event.layerX || d3.event.offsetX;
        var mouseY = d3.event.layerY || d3.event.offsetY;
    }

    var col = hiddencontext.getImageData(mouseX, mouseY, 1, 1).data;
    var colKey = "rgb(" + col[0] + "," + col[1] + "," + col[2] + ")";
    var nodeData = data.nodeclr[colKey];
    try {
        var doc = data.info.get("" + nodeData);

        doi(doc.wosarticle__di);
    } catch (e) {}
}

function mousesetup(hiddencontext, mainCanvas, map) {
    mainCanvas.on("mouseout", function() {
        tool.style("opacity", 0);
        title.text("");
    });

    mainCanvas.on("mousemove", canvasmove);
    map.on("mousemove", canvasmove);

    mainCanvas.on("dblclick", canvasdblclick);
    map.on("dblclick", canvasdblclick);
}

function zoomed(transform) {
    imageData = undefined;

    var matrix = [1, 0, 0, 1, 0, 0];

    function translate(x, y) {
        matrix[4] += matrix[0] * x + matrix[2] * y;
        matrix[5] += matrix[1] * x + matrix[3] * y;
    }
    function scale(x, y) {
        matrix[0] *= x;
        matrix[1] *= x;
        matrix[2] *= y;
        matrix[3] *= y;
    }

    function getXY(mouseX, mouseY) {
        newX = mouseX * matrix[0] + mouseY * matrix[2] + matrix[4];
        newY = mouseX * matrix[1] + mouseY * matrix[3] + matrix[5];
        return { x: newX, y: newY };
    }

    //console.log(transform)
    data.zoom = (1 / transform.k) ** 0.5 
    data.zoom = data.zoom>=1?data.zoom : 1;

    //d3.selectAll(".annotation-group").remove();
    context.save();
    context.clearRect(0, 0, width, height);
    context.translate(transform.x, transform.y);
    context.scale(transform.k, transform.k);
    //map._resetView([51,0],8)
    hiddencontext.save();
    hiddencontext.clearRect(0, 0, width, height);
    hiddencontext.translate(transform.x, transform.y);
    hiddencontext.scale(transform.k, transform.k);

    draw();
    context.restore();
    hiddencontext.restore();

    window.scroll(0, 0);
    //
    translate(transform.x, transform.y);
    scale(transform.k, transform.k);

    try {
        data.makeAnnotations.annotations().forEach((d, i) => {
            var e = getXY(d.data.x1, d.data.y1);

            var me = d3.selectAll("." + d.id);

            if ((Math.max(e.x, e.y) > width) | (Math.min(e.x, e.y) < 0)) {
                me.attr("opacity", 0);
            } else {
                me.attr("opacity", 1);
                var dx = e.x - d.x + shift.x;
                d.dx -= dx;
                d.x = e.x + shift.x;
                var dy = e.y - d.y;
                d.dy -= dy;
                d.y = e.y;
            }
        });

        data.makeAnnotations.update();
    } catch (e) {
        console.log(e);
    }
}

function sliderchange() {
    window.data.filtered = window.data.tsne;
    if (window.data.topicfilter) {
        var topics = window.data.topicfilter.map(d => d.data.name);
        // topiics
        var toplev = window.data.hierarchy
            .filter(d => topics.includes(d.l3))
            .map(d => d.id);
        var pc =
            window.data.weight(parseFloat(document.getElementById("points").value)) **
            2;

        window.data.filtered = window.data.filtered.filter(d => {
            var d = window.data.topics.get(d.doc_id);
            return (d.score > pc) & toplev.includes("" + d.topic_id);
        });
    } else {
        var pc =
            window.data.weight(parseFloat(document.getElementById("points").value)) **
            2;

        window.data.filtered = window.data.filtered.filter(d => {
            return window.data.topics.get(d.doc_id).score > pc;
        });
    }

    if (window.data.continentselection) {
        console.log(data.continentselection, data.filtered);

        window.data.filtered = window.data.filtered.filter(d => {
            var cs = window.data.info.get(d.doc_id).continent;
            return window.data.continentselection.includes(cs);
        });
    }

    var pc =
        window.data.weight(parseFloat(document.getElementById("points").value)) ** 2;
    window.data.filtered = window.data.filtered.filter(
        d => window.data.topics.get(d.doc_id).score > pc
    );

    if (window.data.showlabel) {
        label();
    }
    draw();
    imageData = undefined; 
    // save an updated still
    
}
