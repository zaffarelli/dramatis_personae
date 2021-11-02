/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
d3.selection.prototype.bringElementAsTopLayer = function() {
    return this.each(function() {
        this.parentNode.appendChild(this);
    });
};

d3.selection.prototype.pushElementAsBackLayer = function() {
    return this.each(function() {
        var firstChild = this.parentNode.firstChild;
        if (firstChild) {
            this.parentNode.insertBefore(this, firstChild);
        }
    });
}

class Jumpweb {
    constructor(data, parent) {
        let me = this;
        this.parent = parent;
        me.init(data);
    }

    init(data) {
        let me = this;
        me.size = 110;
        me.width = me.size * 80;
        me.height = me.size * 60;
        me.w = 1600;
        me.h = 1200;
        me.data = data;
        me.era = (me.data.mj ? 0 : 5018);
        //me.new_routes = me.data.new_routes
        me.ox = me.width / me.size / 2;
        me.oy = me.height / me.size / 2;
        me.step_x = me.size;
        me.step_y = me.size;
        // me.svg = d3.select("#d3area")
        //     .append('svg')
        //     .attr("width", me.width * 1.5)
        //     .attr("height", me.height * 2 )
        //     .style("background", "transparent")
        //     .call(d3.zoom().on("zoom", function() {
        //         me.svg.attr("transform", d3.event.transform)
        //     }))
        //     .attr('transform', function(d){
        //         return "translate("+ (-5.5*me.width/16)+","+ (-3*me.height/8)+")";
        //     })
        //     .append('g');



        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h)
        ;
        me.svg = me.vis.append("g")
            .attr("class", "all")
            .style("fill", "#331133")
            .attr('transform', function(d){
                 return "translate("+ (-5.5*me.width/16)+","+ (-3*me.height/8)+")";
             })
            .append('g');
        ;


        me.gate_stroke = "#333"
        me.gate_fill = "#999"
        me.panel_stroke = "#111"
        me.panel_fill = "#222"
        me.text_stroke = "#888"
        me.text_fill = "#DDD"
        me.gate_off = "#747"
        me.mark = 8;
    }

    formatXml(xml) {
        let formatted = '';
        let reg = /(>)(<)(\/*)/g;
        // */
        xml = xml.replace(reg, '$1\r\n$2$3');
        let pad = 0;
        jQuery.each(xml.split('\r\n'), function(index, node) {
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

            var padding = '';
            for (var i = 0; i < pad; i++) {
                padding += '  ';
            }

            formatted += padding + node + '\r\n';
            pad += indent;
        });

        return formatted;
    }

    draw_layout() {
        let me = this;
        let layout = me.svg.selectAll(".rings")
            .data([2, 6, 12, 18, 24, 30, 36, 42, 48, 54])
            .enter()
            .append("g")
            .attr("transform", function(d) {
                let x = me.ox * me.step_x;
                let y = me.oy * me.step_y;
                return "translate(" + x + "," + y + ")";
            });
        layout.append('ellipse')
            .attr('class', "rings")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function(d) {
                return d * me.step_x;
            })
            .attr("ry", function(d) {
                return d * me.step_y / 2;
            })
            .style("fill", "none")
            .style("stroke", "#535")
            .style("stroke-dasharray", "8 1")
            .style("stroke-width", function(d) {
                return (70 - d) / 4;
            })
            .style("opacity", function(d) {
                return 0.6 - d / 100;
            });

        layout.append('text')
            .style("font-family", "Lato")
            .style("font-size", "20pt")
            .style("text-anchor", "middle")
            .style("fill", "#888")
            .style("strike", "#111")
            .style("strike-width", "0.1pt")
            .attr('y', me.step_y * 20)
//            .text("The Known Worlds - circa " + me.era + " AD")
            .on('click', function(d) {
                // console.log("exporting")
                let now = new Date()
                    .toISOString()
                    .replace(/[^0-9]/g, "");
                $('svg .not_printable').css("opacity", 0);
                $('svg .only_printable').css("opacity", 1);
                let base_svg = d3.select("svg").html();
                $('svg .not_printable').css("opacity", 1);
                $('svg .only_printable').css("opacity", 0);

                let exportable_svg = '<?xml version="1.0" encoding="ISO-8859-1" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="fence_svg_export" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink" \
title="jumpweb_' + me.mode + '_' + now + '.svg"> \
' + base_svg + ' \
</svg>';
                let fname = "jumpweb_" + me.era + "_" + now + ".svg"
                let nuke = document.createElement("a");
                nuke.href = 'data:application/octet-stream;base64,' + btoa(me.formatXml(exportable_svg));
                nuke.setAttribute("download", fname);
                nuke.click();
            });
    }


    draw_node(node) {
        let me = this;

        node.append("circle")
            .attr("class", "bullet")
            .attr("r", me.mark*10)
            .attr("cx", 0)
            .style("stroke", "none")
            .style("fill", function(d) {
                return "none";
            })
            .attr("stroke-width", "1pt")
            .attr("opacity", "0.3");

        node.append("circle")
            .attr("class", "frame circle")
            .attr("r", me.mark*4)
            .style("stroke", function(d) {
                if (d.group<=10){
                    return me.gate_fill;
                }
                return "#666";
            })
            .style("fill", "none")
            .style("stroke-width", "8pt");

        node.append("circle")
            .attr("r", me.mark*4)
            .style("stroke", me.gate_stroke)
            .style("fill", "none")
            .style("stroke-width", "2pt");

        node.append("circle")
            .attr("r", me.mark*3)
            .style("stroke", me.gate_stroke)
            .style("fill", "none")
            .style("stroke-width", "4pt");

        node.append("circle")
            .attr("r", me.mark*4)
            .style("stroke", "none")
            .style("fill", function(d) {
                return "#333";


            })
            .style("stroke-width", me.mark+"pt")
            .style("opacity", 0.5);



        node.append("circle")
            .attr("r", me.mark*3)
            .style("stroke", "#111")
//            .style("fill", function(d) {
//                return '#333';
//            })
            .style("fill", function(d) {
                return (d.color ? d.color : '#CCC');
            })
            .attr("stroke-width", "1pt");
        node.append("path")
            .attr("class", "frame triangle north")
            .attr("d", "M 0,-"+me.mark*2+" l -"+me.mark*1.5+",-"+me.mark*3+" h "+me.mark*3+" Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function(d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_off;
            });
        node.append("path")
            .attr("class", "frame triangle south")
            .attr("d", "M 0,"+me.mark*2+" l -"+me.mark*1.5+","+me.mark*3+" h "+me.mark*3+" Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function(d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_off;
            });
        node.append("path")
            .attr("class", "frame triangle east")
            .attr("d", "M -"+me.mark*2+",0 l -"+me.mark*3+","+me.mark*1.5+" v -"+me.mark*3+" Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function(d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_off;
            });
        node.append("path")
            .attr("class", "frame triangle west")
            .attr("d", "M "+me.mark*2+",0 l "+me.mark*3+","+me.mark*1.5+" v -"+me.mark*3+" Z")
            .style("stroke", me.gate_stroke)
            .style("fill", function(d) {
                if (d.group < 10) {
                    return me.gate_fill;
                }
                return me.gate_off;
            });
        node.append("text")
            .attr("class", function(d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", 0)
            .attr("dy", me.mark*9+"px")
            .style("font-family", "Lato")
            .style("font-size", me.mark*2.5+"pt")
            .style("text-anchor", "middle")
            .style("fill", "#DDD")
            .style("stroke", "#111")
            .style("stroke-width", "0.25pt")
            .style("font-variant", "small-caps")
            .text(function(d) {
                return d.name;
            });

        node.append("text")
            .attr("class", function(d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", me.mark*8)
            .attr("dy", me.mark*1.5)
            .style("font-family", "FadingSunsIcons")
            .style("font-size", me.mark*4+"pt")
            .style("fill", "#EEE")
            .style("stroke", "#444")
            .style("stroke-width", "0.25pt")
            .style("text-anchor", "middle")
            .text(function(d) {
                return d.symbol;
            });

        if (me.data.mj) {
            node.append("text")
                .attr("class", function(d) {
                    return "nodetext_" + d.id;
                })
                .attr("dx", 0)
                .attr("dy", -me.mark*6)
                .style("font-family", "Lato")
                .style("font-size", "9pt")
                .style("font-weight", "bold")
                .style("fill", "#DDD")
                .style("stroke", "#111")
                .style("stroke-width", "0.25pt")
                .style("text-anchor", "middle")
                .text(function(d) {
                    return d.discovery;
                });
        }

        node.append("text")
            .attr("class", function(d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", -me.mark*8)
            .attr("dy", -me.mark*2)
            .style("font-family", "Lato")
            .style("font-size", "9pt")
            .style("font-weight", "bold")
            .style("fill", "#DDD")
            .style("stroke", "#111")
            .style("stroke-width", "0.25pt")
            .style("text-anchor", "middle")
            .text(function(d) {
                return "J "+d.jump;
            });
        node.append("text")
            .attr("class", function(d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", -me.mark*8)
            .attr("dy", me.mark)
            .style("font-family", "Lato")
            .style("font-size", "9pt")
            .style("font-weight", "bold")
            .style("fill", "#DDD")
            .style("stroke", "#111")
            .style("stroke-width", "0.25pt")
            .style("text-anchor", "middle")
            .text(function(d) {
                let res = ''
                if (d.dtj != 69){
                    res = "D "+d.dtj;
                }
                return res;
            });
        node.append("text")
            .attr("class", function(d) {
                return "nodetext_" + d.id;
            })
            .attr("dx", -me.mark*8)
            .attr("dy", 4*me.mark)
            .style("font-family", "Lato")
            .style("font-size", "9pt")
            .style("font-weight", "bold")
            .style("fill", "#DDD")
            .style("stroke", "#111")
            .style("stroke-width", "0.25pt")
            .style("text-anchor", "middle")
            .text(function(d) {
                let res = ''
                if (d.orbital_map == 1){
                    res = "ORBITAL";
                }
                return res;
            });
        return node;
    }

    isDiscovery(a, b) {
        let me = this;
        if (me.data.mj){
            return '';
        }
        let answer = '';
        let arr = me.data.new_routes.split("|");
        _.forEach(arr, function(item) {
            let systems = item.split("_");
            if (((systems[0] == a) & (systems[1] == b)) | ((systems[0] == b) & (systems[1] == a))) {
                if (systems.length == 3) {
                   answer = systems[2];
                }
            }
        })
        return answer;
    }


    isNoNewRoute(a, b) {
        let me = this;
        if (me.data.mj){
            return false;
        }
        let answer = true;
        let arr = me.data.new_routes.split("|");

        _.forEach(arr, function(item) {
            let systems = item.split("_");
            if (((systems[0] == a) & (systems[1] == b)) | ((systems[0] == b) & (systems[1] == a))) {
                answer = false;
            }
        })
        return answer;
    }

    isNoNewWorld(a) {
        let me = this;
        if (me.data.mj){
            return false;
        }
        let answer = true;
        let arr = me.data.new_systems.split("|");

        _.forEach(arr, function(item) {
            if (item == a) {
                answer = false;
            }
        })
        return answer;
    }

    draw_known_worlds() {
        let me = this;
        let link = me.svg.selectAll(".link")
            .data(me.data.links)
            .enter()
        link.append("line")
            .attr("class", function(d) {
                let k = "link ray"
                d.out = false
                d.off = false
                let source = _.find(me.data.nodes, {
                    id: d.source
                })
                let target = _.find(me.data.nodes, {
                    id: d.target
                })
                if (source.group != target.group) {
                    d.out = true
                }
                let source_emp = (source.group < 10);
                let target_emp = (target.group < 10);
                if (source_emp !== target_emp) {
                    d.off = true;
                }
                d.unknown = true;
                if (source_emp && target_emp) {
                    d.unknown = false;
                }
                if (d.unknown) {
                    d.unknown = me.isNoNewRoute(source.name, target.name);
                }
                d.discovery = me.isDiscovery(source.name, target.name)
                if (source.group == target.group){
                    k += " g"+source.group;
                }
                return k;
            })
            .attr('id', function(d) {
                return "link_" + d.source + "_" + d.target;
            })
            .attr("x1", function(l) {
                let source = _.find(me.data.nodes, {
                    id: l.source
                })
                return (source.x + me.ox) * me.step_x;
            })
            .attr("y1", function(l) {
                let source = _.find(me.data.nodes, {
                    id: l.source
                })
                return (source.y + me.oy) * me.step_y;
            })
            .attr("x2", function(l) {
                let target = _.find(me.data.nodes, {
                    id: l.target
                })
                return (target.x + me.ox) * me.step_x;
            })
            .attr("y2", function(l) {
                let target = _.find(me.data.nodes, {
                    id: l.target
                })
                return (target.y + me.oy) * me.step_y;
            })
            .style('stroke', function(d) {
                let res = (d.off ? "#444" : "#666");
                if (d.discovery) {
                    res = "#66E";
                }
                return res;
            })
            .style('stroke-width', function(d) {
                let res = (d.out ? "4pt" : (d.off ? "4pt" : (d.unknown ? "4pt" : "4pt")));
                if (d.discovery) {
                    res = "4pt";
                }
                return res;
            })
            .style('stroke-dasharray', function(d) {
                let res = (d.out ? "7 5" : "none");
                return res;
            })

            .style("opacity", function(d) {
                return (d.unknown ? 0.0 : 0.8);
            })
            .on("mouseover", function(d) {
                me.svg.select("#link_" + d.source + "_" + d.target)
                    .style("stroke-width", function(d) {

                        if (d.discovery) {
                            return '8pt';
                        }
                        return "5pt";
                    })
            })
            .on("mouseout", function(d) {
                me.svg.select(".link").style('stroke-width', function(d) {
                    let res = (d.out ? "1pt" : (d.off ? "1pt" : (d.unknown ? "2pt" : "1pt")));
                    if (d.discovery) {
                        res = '4pt';
                    }

                    return res;
                })
            });

        link.append("text")
            .attr("x",function(l){
                let source = _.find(me.data.nodes, {
                    id: l.source
                });
                let target = _.find(me.data.nodes, {
                    id: l.target
                });
                return (((source.x+target.x)/2 + me.ox) * me.step_x);
             })
            .attr("y",function(l){
                let source = _.find(me.data.nodes, {
                    id: l.source
                });
                let target = _.find(me.data.nodes, {
                    id: l.target
                });
                return (((source.y+target.y)/2 + me.oy) * me.step_y);
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
            .text(function(d) {
                if (d.source.name == "Rimpoche"){
                    // console.log(d);
                }
                return d.discovery;
            });



        let node = me.svg.selectAll(".node")
            .data(me.data.nodes)
            .enter().append("g")
            .attr("class", function(d) {
                let k = 'node'
                d.unknown = (d.group > 10);
                if (d.unknown) {
                    d.unknown = me.isNoNewWorld(d.name);
                }

                // if (d.discovery <= me.era) {
                //     d.unknown = false
                // }
                k += " g"+d.group
                return k;
            })
            .attr("transform", function(d) {
                let x = (d.x + me.ox) * me.step_x;
                let y = (d.y + me.oy) * me.step_y;
                return "translate(" + x + "," + y + ")";
            })
            .on("click", function(d) {
                if (d.orbital_map) {
                    // console.log("Launch orbital map for " + d.name);
                    window.location = "/orbital_map/show/"+d.id+"/";
                }
            })

            .on("mouseover", function(d) {
                // d3.event.preventDefault();
                // d3.event.stopPropagation();
                me.svg.select("#aura_" + d.id)
                    .transition()
                    .delay(0)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("opacity", 0.9)
                me.svg.selectAll(".g" + d.group+" .bullet")
                    .transition()
                    .delay(100)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("fill","#B8B");
                me.svg.selectAll(".g" + d.group+".ray")
                    .transition()
                    .delay(250)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("stroke-width","20pt");
               })

            .on("mouseout", function(d) {

                me.svg.selectAll(".aura")
                    .transition()
                    .delay(0)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("opacity", 0.0)
                me.svg.selectAll(".g" + d.group+" .bullet")
                    .transition()
                    .delay(250)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("fill","none");
                me.svg.selectAll(".g" + d.group+".ray")
                    .transition()
                    .delay(100)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("stroke-width","4pt");
                //.pushElementAsBackLayer();
                me.svg.selectAll(".nodetext_" + d.id)
                    .transition()
                    .delay(0)
                    .duration(250)
                    .ease(d3.easeSin)
                    .style("opacity", 1.0);
            })
            .style("opacity", function(d) {
                //if (me.data.mj == false) {
                return (d.unknown ? 0.0 : 1.0);
                //} else {
                //    return 1.0
                //}
            });
        node = me.draw_node(node);
        let panel = node.append("g")
            .attr("class", "aura")
            .attr("id", function(d) {
                return "aura_" + d.id;
            })
            .style("opacity", 0.0);
        panel.append("circle")
            .attr("r", me.step_y * 0.85)
            .style("stroke-width", "1pt")
            .style("fill", "none")
            .style("stroke-width", "2pt")
            .style("stroke-dasharray", function(d) {
                return (d.orbital_map == 1 ? "1" : "1 5");
            })
            .style("stroke", function(d) {
                return (d.orbital_map == 1 ? "#FFF" : "#888");
            });
    }

    zoomActivate() {
        let me = this;
        me.zoom = d3.zoom()
            .scaleExtent([0.25, 4])
            .on('zoom', function (event) {
                me.svg.attr('transform', event.transform)
            });
        me.vis.call(me.zoom);
    }

    perform() {
        let me = this;
        me.draw_layout();
        me.draw_known_worlds();
        me.zoomActivate();
    }
}
