class Jumpweb {
    constructor(data, parent) {
        let me = this;
        this.parent = parent;
        me.init(data);
    }

    init(data) {
        let me = this;
        me.size = 150;
        me.width = me.size * 80
        me.height = me.size * 60
        me.base_font = "Khand"
        me.selectedNode = undefined
        me.w = parseInt($(me.parent).css('width'))
        me.h = parseInt($(me.parent).css('height'))
        me.data = data
        me.era = 10000
        me.GLOBAL_HEIGHT = 60
        me.GLOBAL_WIDTH = 90
        //me.new_routes = me.data.new_routes
        me.ox = me.GLOBAL_WIDTH / 2 ;
        me.oy = me.GLOBAL_HEIGHT / 2 ;
        me.step_x = me.size;
        me.step_y = me.size;

        me.infotxt = []

        d3.select(me.parent).select("#jumpweb").remove();
        // console.log(parseInt(me.w)+"/"+parseInt(me.h));
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", (-me.ox)+" "+(-me.oy)+" " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h)
            .attr("id", "jumpweb");
        me.layout = me.vis.append("g")
            .attr("class", "layout")
             .attr('transform', function (d) {
                 return "translate(" + (-me.ox * me.step_x) + "," + (-me.oy * me.step_y) + ")";
             })
        me.back = me.layout.append("g")
            .attr("class", "back")
        me.svg = me.layout.append("g")
            .attr("class", "all")
        me.ui = me.vis.append("g")
            .attr("class", "ui")
        me.gate_stroke = "#333"
        me.gate_fill = "#999"
        me.panel_stroke = "#111"
        me.panel_fill = "#222"
        me.text_stroke = "#888"
        me.text_fill = "#DDD"
        me.gate_off = "#747"
        me.mark = 8;

        // Spots
        me.spot_refs = []
        _.forEach([...Array(me.GLOBAL_WIDTH-1).keys()], function (i) {
            _.forEach([...Array(me.GLOBAL_HEIGHT-1).keys()], function (j) {
                me.spot_refs.push({'x': i - (me.ox), 'y': j - (me.oy)});
            });
        });
        // Nodes
        _.forEach(me.data.nodes, function (item, index) {
            if (item.discovery > me.era) {
                item.secret = true;
            }
        })
        console.log(me.data.nodes);
        // Links
        me.selected_routes = {}
        _.forEach(me.data.links, function (item, index) {
            let a = _.find(me.data.nodes, {id: item.source})
            let b = _.find(me.data.nodes, {id: item.target})
            item.name = a.name + "_" + b.name
            item.code = a.id + "_" + b.id
            item.source_node = a.id
            item.target_node = b.id
            if (a.secret | b.secret) {
                item.secret = true;
            }
        });
        console.log(me.data.links);
    }

    formatXml(xml) {
        let formatted = '';
        let reg = /(>)(<)(\/*)/g;
        // */
        xml = xml.replace(reg, '$1\r\n$2$3');
        let pad = 0;
        jQuery.each(xml.split('\r\n'), function (index, node) {
            let indent = 0;
            if (node.match(/.+<\/\w[^>]*>$/)) {
                indent = 0;
            } else if (node.match(/^<\/\w/)) {
                if (pad != 0) {
                    pad -= 1;
                }
            } else if (node.match(/^<\w[^>]*[^\/]>.*$/)) {
                indent = 1;
            } else {
                indent = 0;
            }

            let padding = '';
            for (let i = 0; i < pad; i++) {
                padding += '  ';
            }

            formatted += padding + node + '\r\n';
            pad += indent;
        });

        return formatted;
    }

    drawLayout() {
        let me = this
//         me.layout.append('rect')
//             .attr("x",0)
//             .attr("y",0)
//             .attr("width",me.step_x*me.GLOBAL_WIDTH)
//             .attr("height",me.step_y*me.GLOBAL_HEIGHT)
//             .style("fill","none")
//             .style("stroke","#A02020")
//             .style("stroke-width","3pt")
        me.drawSpots()
        me.drawRings()
    }

    drawSpots(){
        let me = this
        let spots = me.back.selectAll(".spots")
            .data(me.spot_refs)
            .enter()
            .append("g")
            .attr("transform", function (d) {
                let x = (me.ox+1) * me.step_x;
                let y = (me.oy+1) * me.step_y;
                return "translate(" + x + "," + y + ")";
            });
        spots.append('circle')
            .attr('class', 'spots not_printable')
            .attr('id', function (d) {
                return 'spot_' + d.x + '_' + d.y;
            })
            .attr('r', '5pt')
            .attr('cx', function (d) {
                return d.x * me.step_x;
            })
            .attr('cy', function (d) {
                return d.y * me.step_x;
            })
            .attr('stroke-width', '1pt')
            .attr('stroke', '#111')
            .attr('fill', '#222')
            .attr('opacity', 1)
            .on('mouseover', function (e, d) {

                    // me.svg.selectAll('.spots').attr('r', '5pt').attr('fill', '#111');
                    // me.svg.select("#spot_" + d.x + "_" + d.y).attr('r', '15pt').attr('fill', '#fc4');
                    // console.log(d)

            })
            .on('mouseout', function (e, d) {

                    // me.svg.selectAll('.spots').attr('r', '5pt');
                    // me.svg.select("#spot_" + d.x + "_" + d.y).attr('r', '5pt').attr('fill', '#111');

            })
            .on('click', function (e, d) {
                if (e.ctrlKey) {
                    if (me.selectedNode) {
                        console.log('Spot ' + d.x + " " + d.y + " and selected node is [" + me.selectedNode.name + "]!");
                        let tgt = _.find(me.data.nodes, {id: me.selectedNode.id})
                        tgt.x = d.x
                        tgt.y = d.y
                        // me.update();
                        me.selectedNode = undefined;
                    }
                    me.svg.selectAll('.spots').attr('r', '5pt').attr('fill', '#111');
                    me.svg.select("#spot_" + d.x + "_" + d.y).attr('r', '20pt').attr('fill', '#fc4');

                }
            })
        ;
    }

    drawRings(){
        let me = this
        let rings = me.back.selectAll(".rings")
            .data([2, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60])
            .enter()
            .append("g")
            .attr("transform", function (d) {
                let x = me.ox * me.step_x;
                let y = me.oy * me.step_y;
                return "translate(" + x + "," + y + ")";
            });
        rings.append('ellipse')
            .attr('class', "rings")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function (d) {
                return d * me.step_x;
            })
            .attr("ry", function (d) {
                return d * me.step_y / 2;
            })
            .style("fill", "none")
            .style("stroke", "#FC4")
            .style("stroke-dasharray", "4 1")
            .style("stroke-width", function (d) {
                return (70 - d) / 40;
            })
            .style("opacity", function (d) {
                return 0.6 - d / 100;
            });

        }


    drawUI(){
        let me = this
        me.ui.append('text')
            .style("font-family", me.base_font)
            .style("font-size", "30pt")
            .style("text-anchor", "middle")
            .style("fill", "#888")
            .style("stroke", "#111")
            .style("stroke-width", "0.5pt")
            .attr('x', me.w / 2)
            .attr('y', me.h * 0.96)
            .text("The Known Worlds - circa " + me.era + " AD")
            .on('click', function(d) {
                console.log("exporting")
                let now = new Date()
                    .toISOString()
                    .replace(/[^0-9]/g, "");
                $('svg .not_printable').css("opacity", 0);
                $('svg .only_printable').css("opacity", 1);
                let base_svg = d3.select("#jumpweb").html();
                let flist = '<style>';
                for (let f of me.data['fontset']) {
                    flist += '@import url("https://fonts.googleapis.com/css2?family=' + f + '");';
                }
                flist += '</style>';

                $('svg .not_printable').css("opacity", 1);
                $('svg .only_printable').css("opacity", 0);

                let exportable_svg = '<?xml version="1.0" encoding="ISO-8859-1" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="fence_svg_export" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink" \
title="jumpweb_' + me.mode + '_' + now + '.svg"> \
'+ flist + base_svg + '</svg>';

                let fname = "jumpweb_" + me.era + "_" + now + ".svg"
                let nuke = document.createElement("a");
                nuke.href = 'data:application/octet-stream;base64,' + btoa(me.formatXml(exportable_svg));
                nuke.setAttribute("download", fname);
                nuke.click();
            })

        me.infoBlock = me.ui.append("g")
            .attr('id', "infoblock")
            .style('opacity', 0)

        me.refreshInfoBlock()
    }

    refreshInfoBlock(){
        let me = this
        me.ui.select("#inforect").remove()
        me.infoBlock.append("rect")
            .attr("id","inforect")
            .attr('width', me.step_x*3)
            .attr('height', (me.infotxt.length+1)*me.step_y/5)
            .attr('rx', me.step_x/20)
            .attr('ry', me.step_y/20)
            .style("fill", "#111")
            .style("stroke", "#FC4")
            .style("stroke-width", "1pt")
            .on("click", (e,d) => {
                me.ui.select("#infoblock")
                    .transition()
                    .delay(50)
                    .duration(500)
                    .ease(d3.easeSin)
                    .style("opacity", 0)
            })
        _.forEach(me.infotxt, (v,k) => {
            me.ui.select("#infotxt"+k).remove()
            me.infoBlock.append('text')
                .attr("id","infotxt"+k)
                .attr('x', me.step_x/10)
                .attr('y', (k+1)*(me.step_y/5))
                .style("font-family", me.base_font)
                .style("font-size", "16pt")
                .style("text-anchor", "start")
                .style("fill", "#FFF")
                .style("stroke", "#999")
                .style("stroke-width", "0.5pt")
                .text(v)
        })
    }


    lefttext(node, x, y, txt, key) {
        let me = this;
        node.append("text")
            .attr("class", function (d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", me.mark * x)
            .attr("dy", me.mark * y)
            .style("font-family", me.base_font)
            .style("font-size", "9pt")
            .style("font-weight", "bold")
            .style("fill", "#DDD")
            .style("stroke", "#111")
            .style("stroke-width", "0.25pt")
            .style("text-anchor", "end")
            .text(function (d) {
                if (key != '') {
                    return txt + d[key];
                } else {
                    return '';
                }
            })
        ;
    }

    draw_node(node) {
        let me = this
        node.append("circle")
            .attr("class", "bullet")
            .attr("r", me.mark * 10)
            .attr("cx", 0)
            .style("stroke", "none")
            .style("fill", function (d) {
                return "none";
            })
            .attr("stroke-width", "1pt")
            .attr("opacity", "0.3")
        node.append("circle")
            .attr("class", "frame circle")
            .attr("r", me.mark * 4)
            .style("stroke", function (d) {
                if (d.secret) {
                    return "#A22";
                }
                if (d.group <= 10) {
                    return me.gate_fill;
                }
                return "#666";
            })
            .style("fill", "none")
            .style("stroke-width", "8pt")

        node.append("circle")
            .attr("r", me.mark * 4)
            .style("stroke", me.gate_stroke)
            .style("fill", "none")
            .style("stroke-width", "2pt")

        node.append("circle")
            .attr("r", me.mark * 3)
            .style("stroke", me.gate_stroke)
            .style("fill", "none")
            .style("stroke-width", "4pt")

        node.append("circle")
            .attr("r", me.mark * 4)
            .style("stroke", "none")
            .style("fill", function (d) {
                return "#333"
            })
            .style("stroke-width", me.mark + "pt")
            .style("opacity", 0.5)
        node.append("circle")
            .attr("r", me.mark * 3)
            .style("stroke", "#111")
            .style("fill", function (d) {
                return (d.color ? d.color : '#CCC');
            })
            .attr("stroke-width", "1pt");
        let ecu = 40
        node.append("path")
            .attr("class", "second_color")
            .attr("d", "M " + 0 + " -" + ecu / 2 + " a 2 2 0 0 0 0 " + ecu + " Z")
            .style("stroke", function (d) {
                return d.color2;
            })
            .style("fill", function (d) {
                return d.color2;
            });
        node.append("path")
            .attr("class", "frame triangle north")
            .attr("d", "M 0,-" + me.mark * 2 + " l -" + me.mark * 1.5 + ",-" + me.mark * 3 + " h " + me.mark * 3 + " Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function (d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_fill;
            });
        node.append("path")
            .attr("class", "frame triangle south")
            .attr("d", "M 0," + me.mark * 2 + " l -" + me.mark * 1.5 + "," + me.mark * 3 + " h " + me.mark * 3 + " Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function (d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_fill;
            });
        node.append("path")
            .attr("class", "frame triangle east")
            .attr("d", "M -" + me.mark * 2 + ",0 l -" + me.mark * 3 + "," + me.mark * 1.5 + " v -" + me.mark * 3 + " Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function (d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_fill;
            });
        node.append("path")
            .attr("class", "frame triangle west")
            .attr("d", "M " + me.mark * 2 + ",0 l " + me.mark * 3 + "," + me.mark * 1.5 + " v -" + me.mark * 3 + " Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function (d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_fill;
            });
        node.append("text")
            .attr("class", function (d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", 0)
            .attr("dy", me.mark * 9 + "px")
            .style("font-family", me.base_font)
            .style("font-size", me.mark * 2.5 + "pt")
            .style("text-anchor", "middle")
            .style("fill", function (d) {
                return me.selectedNode == d ? '#A22' : "#DDD";
            })
            .style("stroke", "#111")
            .style("stroke-width", "0.25pt")
            .style("font-variant", "small-caps")
            .text(function (d) {
                return d.name;
            });

        node.append("text")
            .attr("class", function (d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", me.mark * 8)
            .attr("dy", me.mark * 1.5)
            .style("font-family", "FadingSunsIcons")
            .style("font-size", me.mark * 4 + "pt")
            .style("fill", "#EEE")
            .style("stroke", "#444")
            .style("stroke-width", "0.25pt")
            .style("text-anchor", "middle")
            .text(function (d) {
                return d.symbol;
            });

        // if (me.data.mj) {
//         node.append("text")
//             .attr("class", function (d) {
//                 return "nodetext_" + d.id;
//             })
//             .attr("dx", 0)
//             .attr("dy", -me.mark * 6)
//             .style("font-family", me.base_font)
//             .style("font-size", "9pt")
//             .style("font-weight", "bold")
//             .style("fill", "#DDD")
//             .style("stroke", "#111")
//             .style("stroke-width", "0.25pt")
//             .style("text-anchor", "middle")
//             .text(function (d) {
//                 return d.discovery + " AD";
//             });
//         // }

//         me.lefttext(node, -6, -2, 'Jumps:', 'jump')
//         me.lefttext(node, -6, -0.5, 'Distance to Jumpgate:', 'dtj')
//         me.lefttext(node, -6, 1, 'OM:', 'orbital_map')
        return node;
    }

    draw_known_worlds() {
        let me = this;
        let link = me.svg.selectAll(".link")
            .data(me.data.links)
            .enter()
        link.append("line")
            .attr("class", function (d) {
                let k = "link ray"
                d.out = (d.source_node.group !== d.target_node.group);                       // Off House
                d.off = (d.source_node.group < 100) !== (d.target_node.group < 100);         // Off Empire
                d.unknown = (d.source_node.group > 100) & (d.target_node.group > 100);
                d.focus = (d.source_node.focus & d.target_node.focus);
                if (d.source_node.group == d.target_node.group) {
                    k += " g" + d.source_node.group;
                }
                return k;
            })
            .attr('id', function (d) {
                return "link_" + d.source + "_" + d.target;
            })
            .attr("x1", function (l) {
                let source = _.find(me.data.nodes, {
                    id: l.source
                })
                return (source.x + me.ox) * me.step_x;
            })
            .attr("y1", function (l) {
                let source = _.find(me.data.nodes, {
                    id: l.source
                })
                return (source.y + me.oy) * me.step_y;
            })
            .attr("x2", function (l) {
                let target = _.find(me.data.nodes, {
                    id: l.target
                })
                return (target.x + me.ox) * me.step_x;
            })
            .attr("y2", function (l) {
                let target = _.find(me.data.nodes, {
                    id: l.target
                })
                return (target.y + me.oy) * me.step_y;
            })
            .style('stroke', function (d) {
                let res = (d.out ? "#888" : (d.off ? "#880" : (d.unknown ? "#811" : "#222")));
                if (d.secret) {
                    res = "#A22";
                }
                if (me.selected_routes.hasOwnProperty(d.code)){
                    res = "#FC4"
                }
                return res;
            })
            .style('stroke-width', function (d) {
                return me.widthForLink(d);
            })
            .style('stroke-dasharray', function (d) {
                let res = (d.out ? "7 5" : (d.off ? "3 5" : (d.unknown ? "1 5 " : "")));
                return res;
            })

            .style("opacity", function (d) {
                return (d.secret ? 0.0 : 1.0);
            })
            .on("mouseover", function (e, d) {
                console.log(e)
                me.svg.select("#link_" + d.source + "_" + d.target)
                    .style("stroke-width", function (d) {
                        return "5pt";
                    })
            })
            .on("mouseout", function (e, d) {
                me.svg.select(".link").style('stroke-width', function (d) {
                    // console.log("mouseout");
                    let res = (d.out ? "2pt" : (d.off ? "4pt" : (d.unknown ? "2pt" : "6pt")))
                    //let res = (d.out ? "2pt" : (d.off ? "4pt" : (d.unknown ? "2pt" : "6pt")))
                    return res;
                })
            })
            .on("click", function (e, d) {
                    e.preventDefault()
                    e.stopPropagation()
                    if (me.selected_routes.hasOwnProperty(d.code)){
                        me.selected_routes.remove(d.code)
                    }
                    else{
                        me.selected_routes[d.code] = d
                    }
                    me.updateSelectedLinks()
                })
        ;

        link.append("text")
            .attr("x", function (l) {
                let source = _.find(me.data.nodes, {
                    id: l.source
                });
                let target = _.find(me.data.nodes, {
                    id: l.target
                });
                return (((source.x + target.x) / 2 + me.ox) * me.step_x);
            })
            .attr("y", function (l) {
                let source = _.find(me.data.nodes, {
                    id: l.source
                });
                let target = _.find(me.data.nodes, {
                    id: l.target
                });
                return (((source.y + target.y) / 2 + me.oy) * me.step_y);
            })
            .attr("dx", "-5pt")
            .attr("dy", "-5pt")
            .style("font-family", "Lato")
            .style("font-size", "12pt")
            .style("font-weight", "bold")
            .style("fill", "#DDD")
            .style("stroke", "#000")
            .style("stroke-width", "0.5pt")
            .style("text-anchor", "middle")
            .text(function (d) {
                return d.discovery;
            });


        let node = me.svg.selectAll(".node")
            .data(me.data.nodes)
            .enter().append("g")
            .attr("class", function (d) {
                let k = 'node'
                d.unknown = (d.group > 10);
                k += " g" + d.group
                return k;
            })
            .attr('id', function(d){
                return "node_"+d.id
            })
            .attr("transform", function (d) {
                let x = (d.x + me.ox) * me.step_x;
                let y = (d.y + me.oy) * me.step_y;
                return "translate(" + x + "," + y + ")";
            })
            .on("click", function (e, d) {
                if (e.ctrlKey) {
                    me.selectedNode = d;
                    //console.log(me.selectedNode.name + " has been selected")
                    me.infotxt = []
                    me.infotxt.push(d.name.toUpperCase())
                    if (d.notes.length > 0){
                        me.infotxt.push(d.notes)
                    }
                    me.infotxt.push("Alliance: "+d.alliance)
                    me.infotxt.push("Sector: "+d.sector)
                    me.infotxt.push("Discovery: "+d.discovery+" AD")
                    me.refreshInfoBlock()
                    me.ui.select("#infoblock")
                        .transition()
                        .delay(50)
                        .duration(500)
                        .ease(d3.easeSin)
                        .style("opacity", 1)

                } else if (e.altKey) {
                    if (d.orbital_map) {
                        // console.log("Launch orbital map for " + d.name);
                        $('#customize').val(d.name);
                        $('#orbital_map').click();
                        // window.location = "/ajax/orbital/"+d.name+"/";
                    }
                }
            })
            .on("mouseover", function (e, d) {
                // d3.event.preventDefault();
                // d3.event.stopPropagation();
                me.svg.select("#aura_" + d.id)
                    .transition()
                    .delay(0)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("opacity", 0.9)
                me.svg.selectAll(".g" + d.group + " .bullet")
                    .transition()
                    .delay(100)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("fill", "#B8B");
                me.svg.selectAll(".g" + d.group + ".ray")
                    .transition()
                    .delay(250)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("stroke-width", "20pt");
            })

            .on("mouseout", function (e, d) {

                me.svg.selectAll(".aura")
                    .transition()
                    .delay(0)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("opacity", 0.0)
                me.svg.selectAll(".g" + d.group + " .bullet")
                    .transition()
                    .delay(250)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("fill", "none");
                me.svg.selectAll(".g" + d.group + ".ray")
                    .transition()
                    .delay(100)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("stroke-width", "4pt")
                ;
                me.svg.selectAll(".nodetext_" + d.id)
                    .transition()
                    .delay(0)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("opacity", 1.0);
            })
            .style("opacity", function (d) {
                return (d.secret ? 0.0 : 1.0)

            })

        node = me.draw_node(node);
        let panel = node.append("g")
            .attr("class", "aura")
            .attr("id", function (d) {
                return "aura_" + d.id;
            })
            .style("opacity", 0.0);
        panel.append("circle")
            .attr("r", me.step_y * 0.85)
            .style("stroke-width", "1pt")
            .style("fill", "none")
            .style("stroke-width", "2pt")
            .style("stroke-dasharray", function (d) {
                return (d.orbital_map == 1 ? "1" : "1 5");
            })
            .style("stroke", function (d) {
                return (d.orbital_map == 1 ? "#FFF" : "#888");
            });

    }

    widthForLink(d){
        let me = this
        let res = (d.out ? "2pt" : (d.off ? "4pt" : (d.unknown ? "2pt" : "6pt")))
        if (d.discovery) {
            res = "6pt";
        }
        if (me.selected_routes.hasOwnProperty(d.code)){
            res = "10pt"
        }
        return res
    }

    colorForLink(){
        }


    zoomActivate() {
        let me = this;
        me.zoom = d3.zoom()
            .scaleExtent([0.125, 16])
            .on('zoom', function (event) {
                me.layout.attr('transform', event.transform)
            });
        me.vis.call(me.zoom);
    }

    update(){
        let me = this;
        me.draw_known_worlds();
    }


    perform() {
        let me = this;
        $(me.parent).css("padding", 0);
        me.drawLayout();
        me.drawUI();
        me.update();
        me.zoomActivate();
    }
}
