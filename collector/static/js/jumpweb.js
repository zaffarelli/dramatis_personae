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
  constructor(data) {
    console.log('Starting jumpweb');
    let me = this;
    me.init(data);
  }

  init() {
    let me = this;
    me.size = 70;
    me.width = me.size * 80;
    me.height = me.size * 60;
    me.mj = false;
    me.era = (me.mj ? 0 : 5018);
    me.data = data;
    me.ox = me.width / me.size / 2;
    me.oy = me.height / me.size / 2;
    me.step_x = me.size,
    me.step_y = me.size,
    me.svg = d3.select(".details").append('div').attr("class", "jumpweb")
      .append('svg')
      .attr("width", me.width*1.5)
      .attr("height", me.height*2)
      .style("background","#101010")
      .call(d3.zoom().on("zoom", function () {
          me.svg.attr("transform", d3.event.transform)
      }))
      .append('g')
      ;
    me.gate_stroke = "#111"
    me.gate_fill = "#666"
    me.panel_stroke = "#111"
    me.panel_fill = "#222"
    me.text_stroke = "#888"
    me.text_fill = "#DDD"
  }

  formatXml(xml) {
    var formatted = '';
    var reg = /(>)(<)(\/*)/g;
    xml = xml.replace(reg, '$1\r\n$2$3');
    var pad = 0;
    jQuery.each(xml.split('\r\n'), function(index, node) {
      var indent = 0;
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
      .style("stroke", "#333")
      .style("stroke-dasharray", "8 1")
      .style("stroke-width", function(d) {
        return (70 - d) / 4;
      })
      .style("opacity", function(d) {
        return 0.6 - d / 100;
      });

    layout.append('text')
      .style("font-family", "Roboto")
      .style("font-size", "20pt")
      .style("text-anchor", "middle")
      .style("fill", "#888")
      .style("strike", "#111")
      .style("strike-width", "0.1pt")
      .attr('y', me.step_y * 20)
      .text("The Known Worlds - circa " + me.era + " AD")
      .on('click', function(d) {
        console.log("exporting")
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
      .attr("class", "frame circle")
      .attr("r", "16")
      .style("stroke", function(d) {
        //if (d.group<100){
        return me.gate_fill;
        //}
        //return "#A22";
      })
      .style("fill", "none")
      .style("stroke-width", "4px");

    node.append("circle")
      .attr("r", "18")
      .style("stroke", me.gate_stroke)
      .style("fill", "none")
      .style("stroke-width", "1pt");

    node.append("circle")
      .attr("r", "14")
      .style("stroke", me.gate_stroke)
      .style("fill", "none")
      .style("stroke-width", "1pt");

    node.append("circle")
      .attr("r", "14")
      .style("stroke", "none")
      .style("fill", "#111")
      .style("stroke-width", "1pt")
      .style("opacity", 0.5);

    node.append("circle")
      .attr("r", 5)
      .attr("cx", -24)
      .style("stroke", "#111")
      .style("fill", function(d) {
        return (d.color ? d.color : '#CCC');
      })
      .attr("stroke-width", "1pt");

    node.append("circle")
      .attr("r", 8)
      .style("stroke", "#111")
      .style("fill", function(d) {
        return '#333';
      })
      .attr("stroke-width", "1pt");
    node.append("path")
      .attr("class", "frame triangle north")
      .attr("d", "M 0,-8 l -5,-10 h 10 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", function(d) {
        if (d.group < 100) {
          return me.gate_fill;
        }
        return "#A22";
      });
    node.append("path")
      .attr("class", "frame triangle south")
      .attr("d", "M 0,8 l -5,10 h 10 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", function(d) {
        if (d.group < 100) {
          return me.gate_fill;
        }
        return "#A22";
      });
    node.append("path")
      .attr("class", "frame triangle east")
      .attr("d", "M -8,0 l -10,5 v -10 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", function(d) {
        if (d.group < 100) {
          return me.gate_fill;
        }
        return "#A22";
      });
    node.append("path")
      .attr("class", "frame triangle west")
      .attr("d", "M 8,0 l 10,5 v -10 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", function(d) {
        if (d.group < 100) {
          return me.gate_fill;
        }
        return "#A22";
      })

    ;
    node.append("text")
      .attr("class", function(d) {
        return "nodetext_" + d.id;
      })
      .attr("dx", 0)
      .attr("dy", "26px")
      .style("font-family", "Lato")
      .style("font-size", "9pt")
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
      .attr("dx", 30)
      .attr("dy", 10)
      .style("font-family", "FadingSunsIcons")
      .style("font-size", "20pt")
      .style("fill", "#FFF")
      .style("stroke", "#444")
      .style("stroke-width", "0.25pt")
      .style("text-anchor", "middle")
      .text(function(d) {
        return d.symbol;
      });

    if (me.mj) {
      node.append("text")
        .attr("class", function(d) {
          return "nodetext_" + d.id;
        })
        .attr("dx", 0)
        .attr("dy", -24)
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
      .attr("dx", -24)
      .attr("dy", -8)
      .style("font-family", "Lato")
      .style("font-size", "9pt")
      .style("font-weight", "bold")
      .style("fill", "#DDD")
      .style("stroke", "#111")
      .style("stroke-width", "0.25pt")
      .style("text-anchor", "middle")
      .text(function(d) {
        return d.jump;
      });
    return node;
  }

  draw_known_worlds() {
    let me = this;
    let link = me.svg.selectAll(".link")
      .data(me.data.links)
      .enter()
      .append("line")
      .attr("class", function(d) {
        let k = "link"
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
        let source_emp = (source.group < 100);
        let target_emp = (target.group < 100);
        if (source_emp !== target_emp) {
          d.off = true
        }
        d.unknown = false
        //if (source_emp && target_emp) {

        if ((source.discovery > me.era) || (target.discovery > me.era)) {
          d.unknown = true
        }
        //}

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
        let res = (d.off ? "#A22" : "#A82");
        return res;
      })
      .style('stroke-width', function(d) {
        let res = (d.out ? "1pt" : (d.off ? "1pt" : (d.unknown ? "2pt" : "1pt")));
        return res;
      })
      .style('stroke-dasharray', function(d) {
        let res = (d.out ? "7 5" : "none");
        return res;
      })
      .style("opacity", function(d) {
        if (me.mj == false) {
          return (d.unknown ? 0.0 : 0.5);
        } else {
          return 0.5
        }
      })
      .on("mouseover", function(d) {
        d3.selectAll("#link_" + d.source + "_" + d.target).style("stroke-width", "5pt")
      })
      .on("mouseout", function(d) {
        d3.selectAll(".link").style('stroke-width', function(d) {
          let res = (d.out ? "1pt" : (d.off ? "1pt" : (d.unknown ? "2pt" : "1pt")));
          return res;
        })
      });


    let node = me.svg.selectAll(".node")
      .data(me.data.nodes)
      .enter().append("g")
      .attr("class", function(d) {
        let k = 'node'
        d.unknown = (d.group >= 100);
        if (d.discovery <= me.era) {
          d.unknown = false
        }
        return k;
      })
      .attr("transform", function(d) {
        let x = (d.x + me.ox) * me.step_x;
        let y = (d.y + me.oy) * me.step_y;
        return "translate(" + x + "," + y + ")";
      })
      .on("mouseover", function(d) {
        d3.event.preventDefault()
        d3.event.stopPropagation()

        d3.selectAll(".nodetext_" + d.id)
          .transition()
          .delay(0)
          .duration(250)
          .ease(d3.easeSin)
          .style("opacity", 0.0);
        d3.select("#aura_" + d.id)
          .transition()
          .delay(0)
          .duration(250)
          .ease(d3.easeSin)
          .style("opacity", 0.9)
        //.bringElementAsTopLayer();
      })
      .on("mouseout", function(d) {

        d3.selectAll(".aura")
          .transition()
          .delay(0)
          .duration(250)
          .ease(d3.easeSin)
          .style("opacity", 0.0)
        //.pushElementAsBackLayer();
        d3.selectAll(".nodetext_" + d.id)
          .transition()
          .delay(0)
          .duration(250)
          .ease(d3.easeSin)
          .style("opacity", 1.0);
      })
      .style("opacity", function(d) {
        if (me.mj == false) {
          return (d.unknown ? 0.0 : 1.0);
        } else {
          return 1.0
        }
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
      .style("stroke", "#FC4")
      .style("stroke-width", "3pt")
      .style("stroke-dasharray", "5 3");

    //
    // panel.append("rect")
    //   .attr("rx", 10)
    //   .attr("x", function(d) {
    //     return -me.step_x;
    //   })
    //   .attr("y", function(d) {
    //     return -me.step_y;
    //   })
    //   .attr("width", function(d) {
    //     return me.step_x * 8;
    //   })
    //   .attr("height", function(d) {
    //     return me.step_y * 2;
    //   })
    //   .style("stroke-width", "1pt")
    //   .style("fill", me.panel_stroke)
    //   .style("stroke", me.panel_fill);
    // panel.append("text")
    //   .attr("x", function(d) {
    //     return 0.8 * me.step_x;
    //   })
    //   .attr("y", '-1.8em')
    //   .style("stroke", me.text_stroke)
    //   .style("fill", me.text_fill)
    //   .style("text-anchor", "start")
    //   .style("font-variant", "small-caps")
    //   .style("font-size", "16pt")
    //   .style("font-family", "Lato")
    //   .text(function(d) {
    //     return d.name;
    //   });
    // panel.append("text")
    //   .attr("x", function(d) {
    //     return 0.8 * me.step_x;
    //   })
    //   .attr("y", '-0.7em')
    //   .style("stroke", me.text_stroke)
    //   .style("fill", me.text_fill)
    //   .style("text-anchor", "start")
    //   .style("font-size", "10pt")
    //   .style("font-family", "Lato")
    //   .text(function(d) {
    //     return d.alliance;
    //   });
    // panel.append("text")
    //   .attr("x", function(d) {
    //     return 0.8 * me.step_x;
    //   })
    //   .attr("y", '0.4em')
    //   .style("stroke", me.text_stroke)
    //   .style("fill", me.text_fill)
    //   .style("text-anchor", "start")
    //   .style("font-size", "10pt")
    //   .style("font-family", "Lato")
    //   .text(function(d) {
    //     return d.jump + " jump(s)";
    //   });
    // panel.append("text")
    //   .attr("x", function(d) {
    //     return 0.8 * me.step_x;
    //   })
    //   .attr("y", "1.5em")
    //   .style("stroke", me.text_stroke)
    //   .style("fill", me.text_fill)
    //   .style("text-anchor", "start")
    //   .style("font-size", "10pt")
    //   .style("font-family", "Lato")
    //   .text(function(d) {
    //     let res = ""
    //     if (d.garrison) {
    //       res += "Garrison: " + d.garrison;
    //       res += " Tech: " + d.tech;
    //       res += " Population: " + d.population / 1000000 + " M";
    //     }
    //     return res;
    //   });
    // panel.append("text")
    //   .attr("x", function(d) {
    //     return 0.8 * me.step_x;
    //   })
    //   .attr("y", "2.6em")
    //   .style("stroke", me.text_stroke)
    //   .style("fill", me.text_fill)
    //   .style("text-anchor", "start")
    //   .style("font-size", "10pt")
    //   .style("font-family", "Lato")
    //   .text(function(d) {
    //     let res = ""
    //     if (d.dtj) {
    //       res += "Distance to jumpgate " + d.dtj;
    //     }
    //     return res;
    //   });
  }

  perform() {
    let me = this;
    me.draw_layout()
    me.draw_known_worlds()
  }
}
