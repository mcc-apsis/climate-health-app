function label() {
    if (data.carto) {
        switchview();
    }

    if (data.makeAnnotations) {
        if (data.showlabel) {
            data.showlabel = false;
            fadeout([".annotation-group"], (duration = 2700));
        } else {
            data.showlabel = true;
            fadein([".annotation-group"], (duration = 2700));
        }

        return 1;
    }

    if (d3.select(".annotation-group").node() != null) {
        return d3.select(".annotation-group").remove();
    }

    data.showlabel = false;

    const type = d3.annotationCalloutCircle;

    var left = data.labels.filter(d => d.left);
    var right = data.labels.filter(d => !d.left);

    var lh = height / (em * left.length);
    var rh = height / (em * right.length);

    var lc = 1;
    var rc = 1;

    var annotations = data.labels.map(d => {
        if (d.left) {
            var dh = lc * lh * em;
            lc += 1;
        } else {
            var dh = rc * rh * em;
            rc += 1;
        }
        var id = "label_" + d.label.replace(/[&\s-\/\.]/g, "_");

        return {
            note: {
                title: "32",
                label: d.label,
                bgPadding: 0,
                align: !d.left ? "left" : "right"
            },
            //can use x, y directly instead of data
            data: { x1: d.cx, y1: d.cy },
            x: d.cx + shift.x,
            y: d.cy + shift.y,

            id: id,
            ny: dh, //d.cy,
            nx: d.left ? shift.x - 20 : 20 + shift.width + shift.x,

            className: id,

            subject: {
                radius: 4
            }
        };
    });

    data.makeAnnotations = d3
        .annotation()
        .editMode(false)
        .notePadding(1.01)
        .type(type)
        .accessors({})
        .annotations(annotations);

    d3
        .select("#overlay")
        .append("g")
        .attr("class", "annotation-group")
        .style("opacity", 0)
        .call(data.makeAnnotations);

    // d3.selectAll('.annotation-note-label tspan').attr('dy','1.8em')
    d3.selectAll(".annotation-connector").attr("opacity", 0.3);
    d3
        .selectAll(".annotation-note-label")
        .style("pointer-events", "auto")
        .on("mouseover", function() {
            var p = d3.select(this);

            [
                ...p
                    .node()
                    .parentElement.parentElement.parentElement.querySelectorAll(
                        "path, text"
                    )
            ].forEach(d => {
                d3.select(d).classed("hilight", true);
            });
        })
        .on("mouseout", function() {
            var p = d3.select(this);
            [
                ...p
                    .node()
                    .parentElement.parentElement.parentElement.querySelectorAll(
                        "*"
                    )
            ].forEach(d => {
                d3.select(d).classed("hilight", false);
            });
        });
    //
}
