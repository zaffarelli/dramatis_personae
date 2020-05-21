

class OrbitalMap {
    constructor(data) {
        console.log('Starting OrbitalMap');
        let me = this;
        me.init(data);
    }

    init(data){
        let me = this;
        me.size = 40;
        me.width = me.size * 80;
        me.height = me.size * 60;
        me.mj = false;
        me.era = (me.mj ? 0 : 5018);
        me.data = data;
        me.ox = me.width / me.size / 2;
        me.oy = me.height / me.size / 2;
        me.step_x = me.size, //me.width / 80;
          me.step_y = me.size, //me.width / 40;
          me.svg = d3.select(".details").append('svg')
          .attr("width", me.width)
          .attr("height", me.height);
        me.gate_stroke = "#111"
        me.gate_fill = "#666"
        me.panel_stroke = "#111"
        me.panel_fill = "#222"
        me.text_stroke = "#888"
        me.text_fill = "#DDD"        
    }

    let width = $(window).width() - 40,
      height = $(window).height() - 40,
      radius = 0,
      design = {
        "size": {
          "sun": 5,
          "belt": 0,
          "telluric": 4,
          "gas_giant": 12,
          "station": 3,
          "jumpgate": 5
        },
        "fill": {
          "sun": "#fc4",
          "belt": "#861",
          "telluric": "#000",
          "gas_giant": "#123",
          "station": "#321",
          "jumpgate": "#222"
        },
        "stroke": {
          "sun": "#fc4",
          "belt": "#111",
          "telluric": "#000",
          "gas_giant": "none",
          "station": "#000",
          "jumpgate": "#000"
        },
        "label": {
          "sun": "Yellow Star",
          "belt": "Asteroids Belt",
          "telluric": "Telluric Planet",
          "gas_giant": "Gas Giant",
          "station": "Artificial Station",
          "jumpgate": "Jumpgate"
        },
        "shape": {
          "sun": "circle",
          "belt": "circle",
          "telluric": "circle",
          "gas_giant": "circle",
          "station": "circle",
          "jumpgate": "ellipse"
        }

      };

    d3.json("icon_om.json", function(error, json) {
      if (error) throw error;



      let ox = 20,
        oy = 10,
        step_x = width / 40,
        step_y = width / 40,
        scaler = 10;

      let radius = 3 * width / 4,
        time = 0;

      let radiused = d3.scaleLinear()
        .domain([0, 100])
        .range([0, radius]);

      _.forEach(json.planets, function(e, i) {
        e.id = i;
      })

      // ---------

      let svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

      let planets = svg.append('g')
        .attr('class', 'suns')
        .attr("transform", function(d) {
          let trans = "translate("
          trans += ox * step_x;
          trans += ","
          trans += oy * step_y;
          trans += ")"
          return trans;
        });

      planets.append('text')
        .attr("x", 0)
        .attr("y", -7 * step_y)
        .style("fill", "#111")
        .style("stroke", "#777")
        .style("font-size", "24pt")
        .style("font-family", "VL Gothic")
        .style("text-anchor", "middle")
        .text(json.title)

      planets.append('ellipse')
        .attr("cx", 0)
        .attr("cy", 0)
        .attr("rx", function(d) {
          return radiused(50);
        })
        .attr("ry", function(d) {
          return radiused(50) / 3;
        })
        .style("fill", "#ECE")
        .style("stroke", "none")
        .style("opacity", 0.25);

      // planets.append('line')
      //   .attr('x1', -radiused(70))
      //   .attr('y1', 0)
      //   .attr('x2', radiused(70))
      //   .attr('y2', 0)
      //   .style("fill", "transparent")
      //   .style("stroke", "#222")
      //   //.style("stroke-dasharray", "5 3")
      //   .style("opacity", 0.5);
      //
      // planets.append('line')
      //   .attr('x1', 0)
      //   .attr('y1', -radiused(70) / 3)
      //   .attr('x2', 0)
      //   .attr('y2', radiused(70) / 3)
      //   .style("fill", "transparent")
      //   .style("stroke", "#222")
      //   //.style("stroke-dasharray", "5 3")
      //   .style("opacity", 0.5);

      let planets_enter = planets.append('g')
        .attr("class", "planet")
        .selectAll("planet")
        .data(json.planets).enter();

      let orbital_group = planets_enter
        .append('g')
        .attr("transform", function(d) {
          return "rotate(" + d.tilt + ")";
        })
      orbital_group.append('ellipse')
        .attr("cx", 0)
        .attr("cy", 0)
        .attr("rx", function(d) {
          return radiused(d.AU);
        })
        .attr("ry", function(d) {
          return radiused(d.AU) / 3;
        })
        .style("fill", "none")
        .style("stroke-width", function(d) {
          if (d.type == 'belt') {
            return "10pt";
          }
          return "1pt";
        })
        .style("stroke-dasharray", "17 3")
        .style("stroke", "#888")
        .style("opacity", function(d) {
          if (d.type == 'belt') {
            return "0.25";
          }
          return "0.85";
        })
        .on("mouseout", function(d) {
          d3.selectAll("#planet_text_" + d.id).style("opacity", 0.1)
          d3.selectAll("#planet_text_add_" + d.id).style("opacity", 0.1)
        })
        .on("mouseover", function(d) {
          d3.selectAll("#planet_text_" + d.id).style("opacity", 1.0)
          d3.selectAll("#planet_text_add_" + d.id).style("opacity", 1.0)
        });
      orbital_group.append('line')
        .attr('x1', function(d) {
          return -radiused(d.AU);
        })
        .attr('y1', 0)
        .attr('x2', function(d) {
          return radiused(d.AU);
        })
        .attr('y2', 0)
        .style("fill", "transparent")
        .style("stroke", "#222")
        .style("stroke-dasharray", "5 13")
        .style("opacity", 0.5);
      orbital_group.append('line')
        .attr('y1', function(d) {
          return -radiused(d.AU) / 3;
        })
        .attr('x1', 0)
        .attr('y2', function(d) {
          return radiused(d.AU) / 3;
        })
        .attr('x2', 0)
        .style("fill", "transparent")
        .style("stroke", "#222")
        .style("stroke-dasharray", "5 13")
        .style("opacity", 0.5);

      let translateAlong = function() {
        return function(d, i, a) {
          return function(t) {
            let t_angle = (2 * Math.PI) * t * d.speed * 100;
            let t_x = d.AU * Math.cos(t_angle);
            let t_y = d.AU * Math.sin(t_angle);
            return "translate(" + radiused(t_x) + "," + radiused(t_y) / 3 + ")";
          }
        }
      }


      let item = orbital_group.append('g')
        .attr('id', function(d) {
          return "planet_" + d.id
        })
        .attr('class', "planetball")
        .attr("transform", function(d) {
          return "translate(" + radiused(d.AU) + ",0)"
        })
      item.append("circle")
        .attr("cx", 0)
        .attr("cy", 0)
        .attr("rx", function(d) {
          rx = 0
          if (d.type == 'jumpgate'){
            rx = 3
          }
          return rx;
        })
        .attr("rx", function(d) {
          ry = 0
          if (d.type == 'jumpgate'){
            ry = 8
          }
          return ry;
        })

        .attr("r", function(d) {
          let size = design.size[d.type];
          return size;
        })
        .style("fill", function(d) {
          let size = d.tone;
          return size;
        })
        .style("stroke-width", "1pt")
        .style("stroke", function(d) {
          let size = design.stroke[d.type];
          return size;
        })
      item.append('text')
        .attr('id', function(d) {
          return "planet_text_" + d.id
        })
        .attr('class', "planet_text")
        .attr("y", function(d) {
          if (d.type == "sun") {
            return "-2em"
          }
          return "2em";
        })
        .style("opacity", 0.1)
        .style("fill", "#111")
        .style("stroke", "#777")
        .style("font-size", "10pt")
        .style("font-family", "VL Gothic")
        .style("text-anchor", "middle")
        .attr("transform", function(d) {
          return "rotate(" + (-d.tilt) + ")";
        })
        .text(function(d) {
          return d.name;
        })
      item.append('text')
        .attr('id', function(d) {
          return "planet_text_add_" + d.id
        })
        .attr('class', "planet_text_add")
        .attr("y", "3em")
        .style("opacity", 0.1)
        .style("fill", "#111")
        .style("stroke", "#777")
        .style("font-size", "10pt")
        .style("font-family", "VL Gothic")
        .style("text-anchor", "middle")
        .attr("transform", function(d) {
          return "rotate(" + (-d.tilt) + ")";
        })
        .text(function(d) {
          if (d.type == "sun") {
            return ""
          }
          return d.AU + " AU (" + design.label[d.type] + ")";
        })
      item.transition()
        .duration(365000)
        .ease(d3.easeLinear)
        .attrTween("transform", translateAlong());

      planets.exit().remove();

    });
  </script>
