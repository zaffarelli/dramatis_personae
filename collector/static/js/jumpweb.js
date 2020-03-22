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
    let me = this;
    me.init(data);
  }

  init() {
    let me = this;
    me.size = 1600;
    me.width =  me.size * 1.50 - 25,
    me.height = me.size * 1.5 - 25,
    me.mj = false;
    me.data = data;
    me.ox = 16;
    me.oy = 16;
    me.step_x = me.width / 40;
    me.step_y = me.width / 40;
    me.svg = d3.select(".details").append('svg')
      .attr("width", me.width)
      .attr("height", me.height)
      ;
    me.gate_stroke = "#666"
    me.gate_fill = "#111"
    me.panel_stroke = "#666"
    me.panel_fill = "#FFF"
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
        d.unknown = false
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
        if (source_emp != target_emp) {
          d.off = true
        }
        if (me.mj == false) {
          if (((source_emp == false) && (source.discovered != true)) || ((target_emp == false) && (target.discovered != true))) {
            d.unknown = true
          }
        }
        return k;
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
        let res = (d.off ? "#A22" : "#EEE");
        return res;
      })
      .style('stroke-width', function(d) {
        let res = (d.out ? "3pt" : (d.off ? "5pt" : (d.unknown ? "3pt" : "4pt")));
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
      });

    let node = me.svg.selectAll(".node")
      .data(me.data.nodes)
      .enter().append("g")
      .attr("class", function(d) {
        let k = 'node'
        if (me.mj == false) {
          if (d.group >= 100) {
            if (d.discovered != true) {
              d.unknown = true
            }
          }
        }
        return k;
      })
      .attr("transform", function(d) {
        let x = (d.x + me.ox) * me.step_x;
        let y = (d.y + me.oy) * me.step_y;
        return "translate(" + x + "," + y + ")" //" scale(0.75,0.75)";
      })
      .on("mouseover", function(d) {
        d3.select(this).bringElementAsTopLayer();
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
          .style("opacity", 0.9);
      })
      .on("mouseout", function(d) {
        //d3.select(this).pushElementAsBackLayer();
        d3.selectAll(".aura")
          .transition()
          .delay(0)
          .duration(250)
          .ease(d3.easeSin)
          .style("opacity", 0.0);
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
    let panel = node.append("g")
      .attr("class", "aura")
      .attr("id", function(d) {
        return "aura_" + d.id;
      })
      .style("opacity", 0.0);

    node.append("circle")
      .attr("class", "frame circle")
      .attr("r", "32")
      .style("stroke", me.gate_stroke)
      .style("fill", me.gate_fill)
      ;
    node.append("circle")
      .attr("r", "24")
      .style("stroke", "#444")
      .style("fill", function(d) {
        return (d.color ? d.color : '#CCC');
      })
      .attr("stroke-width", "1pt");
    node.append("path")
      .attr("class", "frame triangle north")
      .attr("d", "M 0,-16 l -10,-20 h 20 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", me.gate_fill)
      ;
    node.append("path")
      .attr("class", "frame triangle south")
      .attr("d", "M 0,16 l -10,20 h 20 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", me.gate_fill)
      ;
    node.append("path")
      .attr("class", "frame triangle east")
      .attr("d", "M -16,0 l -20,10 v -20 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", me.gate_fill)
      ;
    node.append("path")
      .attr("class", "frame triangle west")
      .attr("d", "M 16,0 l 20,10 v -20 Z")
      .style("stroke", me.gate_stroke)
      .style("fill", me.gate_fill)

    ;
    node.append("text")
      .attr("class", function(d) {
        return "nodetext_" + d.id;
      })
      .attr("dx", 0)
      .attr("dy", "50px")
      .style("font-family", "Lato")
      .style("font-size", "10pt")
      .style("text-anchor", "middle")
      .style("fill", "#FFF")
      .style("stroke", "#BBB")
      .style("font-variant", "small-caps")
      .text(function(d) {
        return d.name;
      });
      /*
    node.append("text")
      .attr("class", function(d) {
        return "nodetext_" + d.id;
      })
      .attr("dx", 0)
      .attr("dy", "65px")
      .style("font-family", "Lato")
      .style("font-size", "10pt")
      .style("fill", "#CCC")
      .style("stroke", "#888")
      .style("text-anchor", "middle")
      .text(function(d) {
        return d.alliance;
      });
      */
    node.append("text")

      .attr("dx", 0)
      .attr("dy", "0.35em")
      .style("font-family", "Lato")
      .style("font-size", "18pt")
      .style("font-weight", "bold")
      .style("fill", "#000")
      .style("stroke", "#333")
      .style("text-anchor", "middle")
      .text(function(d) {
        return d.jump;
      });



    panel.append("rect")
      .attr("rx", 10)
      .attr("x", function(d) {
        return -me.step_x;
      })
      .attr("y", function(d) {
        return -me.step_y;
      })
      .attr("width", function(d) {
        return me.step_x * 8;
      })
      .attr("height", function(d) {
        return me.step_y * 2;
      })
      .style("stroke-width", "1pt")
      .style("fill", me.gate_fill)
      .style("stroke", me.gate_stroke);
    panel.append("text")
      .attr("x", function(d) {
        return 0.8 * me.step_x;
      })
      .attr("y", '-1.8em')
      .style("stroke", me.panel_stroke)
      .style("fill", me.panel_fill)
      .style("text-anchor", "start")
      .style("font-variant", "small-caps")
      .style("font-size", "16pt")
      .style("font-family", "Lato")
      .text(function(d) {
        return d.name;
      });
    panel.append("text")
      .attr("x", function(d) {
        return 0.8 * me.step_x;
      })
      .attr("y", '-0.7em')
      .style("stroke", me.panel_stroke)
      .style("fill", me.panel_fill)
      .style("text-anchor", "start")
      .style("font-size", "10pt")
      .style("font-family", "Lato")
      .text(function(d) {
        return d.alliance;
      });
    panel.append("text")
      .attr("x", function(d) {
        return 0.8 * me.step_x;
      })
      .attr("y", '0.4em')
      .style("stroke", me.panel_stroke)
      .style("fill", me.panel_fill)
      .style("text-anchor", "start")
      .style("font-size", "10pt")
      .style("font-family", "Lato")
      .text(function(d) {
        return d.jump + " jump(s)";
      });
    panel.append("text")
      .attr("x", function(d) {
        return 0.8 * me.step_x;
      })
      .attr("y", "1.5em")
      .style("stroke", me.panel_stroke)
      .style("fill", me.panel_fill)
      .style("text-anchor", "start")
      .style("font-size", "10pt")
      .style("font-family", "Lato")
      .text(function(d) {
        let res = ""
        if (d.garrison) {
          res += "Garrison: " + d.garrison;
          res += " Tech: " + d.tech;
          res += " Population: " + d.population / 1000000 + " M";
        }
        return res;
      });
    panel.append("text")
      .attr("x", function(d) {
        return 0.8 * me.step_x;
      })
      .attr("y", "2.6em")
      .style("stroke", me.panel_stroke)
      .style("fill", me.panel_fill)
      .style("text-anchor", "start")
      .style("font-size", "10pt")
      .style("font-family", "Lato")
      .text(function(d) {
        let res = ""
        if (d.dtj) {
          res += "Distance to jumpgate " + d.dtj;
        }
        return res;
      });
  }

  perform() {
    let me = this;
    me.draw_known_worlds()
  }
}
