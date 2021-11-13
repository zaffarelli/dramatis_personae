class OrbitalMap {
    constructor(data, parent) {
        let me = this;
        this.parent = parent;
        me.init(data);
    }

    zoom_check(x) {
        return x < this.zoom_val;
    }

    apply_zoom(x) {
        return x * this.zoom_factor;
    }

    setConstants() {
        let me = this;
        me.gate_stroke = "#111";
        me.gate_fill = "#666";
        me.panel_stroke = "#111";
        me.panel_fill = "#222";
        me.text_stroke = "#888";
        me.text_fill = "#DDD";
        me.radius = 0;
        me.flatten_factor = 5;
        me.zoom_val = (me.data.zoom_val > 0 ? me.data.zoom_val : 8);
        me.zoom_factor = (me.data.zoom_factor > 0 ? me.data.zoom_factor : 10);
        me.zoom_color = "#545"
        me.design = {
            "size": {
                "Sun": 5,
                "Asteroids Belt": 0,
                "Telluric": 4,
                "Gas Giant": 12,
                "Space Station": 3,
                "Jumpgate": 2
            },
            "fill": {
                "Sun": "#fc4",
                "Asteroids Belt": "#861",
                "Telluric": "#000",
                "Gas Giant": "#123",
                "Space Station": "#321",
                "Jumpgate": "#222"

            },
            "stroke": {
                "Sun": "#fc4",
                "Asteroids Belt": "#666",
                "Telluric": "#333",
                "Gas Giant": "none",
                "Jumpgate": "#868",
                "Space Station": "#CCC"
            },
            "label": {
                "Sun": "Star",
                "Asteroids Belt": "Asteroids Belt",
                "Telluric": "Telluric Planet",
                "Gas Giant": "Gas Giant",
                "Space Station": "Station",
                "Jumpgate": "Jumpgate",
            },
            "shape": {
                "Sun": "circle",
                "Asteroids Belt": "circle",
                "Telluric": "circle",
                "Gas Giant": "circle",
                "Station": "circle",
                "Jumpgate": "ellipse"
            }
        };
        me.size = 60;
        me.width = me.size * 30;
        me.height = me.size * 20;
        me.h = 1200;
        me.w = 1900;
        me.radius = 3 * me.width / 4;
        me.era = 5021;
        me.ox = me.width / me.size / 2;
        me.oy = me.height / me.size / 2;
        me.step_x = me.size;
        me.step_y = me.size;
        me.scaler = 10;
    }

    init(data) {
        let me = this;
        me.data = data;
        me.setConstants();
        me.radiused = d3.scaleLinear()
            .domain([0, 100])
            .range([0, me.radius]);
        me.translateAlong = function (path) {

            return function (d, i, a) {
                return function (t) {
                    let t_real = t;
                    if (t >= d.azimut) {
                        t_real = d.azimut;
                    }
                    let t_angle = (2 * Math.PI) * t_real * d.speed;
                    let t_x = (me.zoom_check(d.AU) ? me.apply_zoom(d.AU) : d.AU) * Math.cos(t_angle);
                    let t_y = (me.zoom_check(d.AU) ? me.apply_zoom(d.AU) : d.AU) * Math.sin(t_angle);
                    return "translate(" + me.radiused(t_x) + "," + me.radiused(t_y) / me.flatten_factor + ")";
                }
            }
        }
        _.forEach(me.data.planets, function (e, i) {
            e.id = i;
        })
    }

    buildGradients() {
        let me = this;
        me.gasGiantGradient = me.svg.append("svg:defs")
            .append("svg:linearGradient")
            .attr("id", "gas_giant_gradient")
            .attr("x1", "25%")
            .attr("y1", "0%")
            .attr("x2", "75%")
            .attr("y2", "100%")
            .attr("spreadMethod", "pad");


        me.gasGiantGradient.append("svg:stop")
            .attr("offset", "0%")
            .attr("stop-color", "#80E020")
            .attr("stop-opacity", 1);
        me.gasGiantGradient.append("svg:stop")
            .attr("offset", "40%")
            .attr("stop-color", "#666666")
            .attr("stop-opacity", 1);
        me.gasGiantGradient.append("svg:stop")
            .attr("offset", "80%")
            .attr("stop-color", "#888888")
            .attr("stop-opacity", 1);
        me.gasGiantGradient.append("svg:stop")
            .attr("offset", "100%")
            .attr("stop-color", "#80E020")
            .attr("stop-opacity", 1);

        me.telluricGradient = me.svg.append("svg:defs")
            .append("svg:linearGradient")
            .attr("id", "telluric_gradient")
            .attr("x1", "0%")
            .attr("y1", "0%")
            .attr("x2", "100%")
            .attr("y2", "100%")
            .attr("spreadMethod", "pad");


        me.telluricGradient.append("svg:stop")
            .attr("offset", "0%")
            .attr("stop-color", "#101030")
            .attr("stop-opacity", 1);

        me.telluricGradient.append("svg:stop")
            .attr("offset", "100%")
            .attr("stop-color", "#3080a0")
            .attr("stop-opacity", 1);

        me.sunGradient = me.svg.append("svg:defs")
            .append("svg:radialGradient")
            .attr("id", "sun_gradient")
            .attr("x1", "0%")
            .attr("y1", "0%")
            .attr("x2", "100%")
            .attr("y2", "100%")
            .attr("spreadMethod", "pad");


        me.sunGradient.append("svg:stop")
            .attr("offset", "0%")
            .attr("stop-color", "#FFFFFF")
            .attr("stop-opacity", 1);

        me.sunGradient.append("svg:stop")
            .attr("offset", "100%")
            .attr("stop-color", "#FFCC44")
            .attr("stop-opacity", 1);
    }


    drawLayout() {
        let me = this;


        me.svg.append('line')
            .attr('x1', 0)
            .attr('x2', 0)
            .attr('y1', -me.step_y * 5)
            .attr('y2', 0)
            .style("fill", "transparent")
            .style("stroke", me.zoom_color)
            .style("stroke-width", "2pt")
            .style("stroke-dasharray", "7 5")
            .style("opacity", 0.5);

        me.svg.append('ellipse')
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function (d) {
                return me.radiused(me.zoom_val);
            })
            .attr("ry", function (d) {
                return me.radiused(me.zoom_val) / me.flatten_factor;
            })
            .style("fill", "#4CF")
            .style("stroke", me.zoom_color)
            .style("opacity", 0.2);

        me.svg.append('ellipse')
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function (d) {
                return me.radiused(50);
            })
            .attr("ry", function (d) {
                return me.radiused(50) / me.flatten_factor;
            })
            .style("fill", "none")
            .style("stroke", "#EEE")
            .style("stroke-dasharray", "1 4 7 4")
            .style("opacity", 0.5);

    }


    drawOrbits() {
        let me = this;
        // Planetary orbit
        me.orbital_group.append('ellipse')
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function (d) {
                return me.radiused((me.zoom_check(d.AU) ? me.apply_zoom(d.AU) : d.AU));
            })
            .attr("ry", function (d) {
                return me.radiused((me.zoom_check(d.AU) ? me.apply_zoom(d.AU) : d.AU)) / me.flatten_factor;
            })
            .style("stroke", function (d) {
                let stroke = "#444"
                if (me.zoom_check(d.AU)) {
                    stroke = me.zoom_color;
                }
                if (d.type == 'Asteroids Belt') {
                    stroke = "#645";
                }
                return stroke;
            })
            .style("stroke-width", function (d) {
                if (d.type == 'Asteroids Belt') {
                    return d.size + "pt";
                }
                return "0.5pt";
            })
            .style("stroke-dasharray", function (d) {
                if (d.type == 'Asteroids Belt') {
                    return "8 1";
                }
                return "8 1";
            })
            .style("fill", "none")
            .style("opacity", function (d) {
                if (d.type == 'Asteroids Belt') {
                    return 0.5;
                }
                return 0.75;
            });


    }


    drawPlanets() {
        let me = this;
        // planet drawing
        me.item = me.orbital_group.append('g')
            .attr('id', function (d) {
                return "planet_" + d.id
            })
            .attr('class', "planetball")
            .attr("transform", function (d) {
                let t = "";
                t += " translate(" + me.radiused((me.zoom_check(d.AU) ? me.apply_zoom(d.AU) : d.AU)) + ",0)"
                return t;
            })

        // Draw sun shards
        me.item.append("path")
            .attr("d", function (d) {
                let s = 16 * 5;
                let m = s / 10;
                let x = m * 4;
                let str = "M -" + s + " 0";
                str += " L -" + m + " -" + m + ",";
                str += " -" + x + " -" + x + ", ";
                str += " -" + m + " -" + m + ", ";
                str += " 0 -" + s + ", ";
                str += " " + m + " -" + m + ", ";
                str += " " + x + " -" + x + ", ";
                str += " " + m + " -" + m + ", ";
                str += " " + s + " 0, ";
                str += " " + m + " " + m + ", ";
                str += " " + x + " " + x + ", ";
                str += " " + m + " " + m + ", ";
                str += " 0 " + s + ", ";
                str += " -" + m + " " + m + " ";
                str += " -" + x + " " + x + ", ";
                str += " -" + m + " " + m + ", ";
                str += " Z"
                return str;
            })
            .style("fill", function (d) {
                let tone = d.tone;
                return tone;
            })
            .style("stroke-width", "1pt")
            .style("stroke", function (d) {
                let s = d.tone;
                return s;
            })
            .attr("opacity", function (d) {
                if (d.type == "Sun") {
                    return 0.15;
                }
                return 0.0;
            });


        // Rings
        me.item.append("ellipse")
            .attr("transform", function (d) {
                let t = "";
                let tilt = d.tilt;
                if (d.rings) {
                    tilt -= d.rings.split("_")[0] * 3;
                }
                t += " rotate(" + tilt + ")"
                return t;
            })
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function (d) {
                let rx = 0;
                if (d.rings) {
                    rx = d.rings.split("_")[1] * 5;
                }
                return rx;
            })
            .attr("ry", function (d) {
                let ry = 0;
                if (d.rings) {
                    ry = ((d.rings.split("_")[1] * 4)) / (me.flatten_factor * 1.5);
                }
                return ry;
            })
            .style("stroke", d => d.tone)
            .style("stroke-width", function (d) {
                if (d.rings) {
                    console.log(((d.rings.split("_")[2]) / 10) + "pt")
                    return ((d.rings.split("_")[2]) / 10) + "pt";
                }
                return 0;
            })
            .style("fill", "none")
            .attr('opacity', function (d) {
                if (d.rings) {
                    return 0.90;
                }
                return 0;
            })


        // Draw planet ellipse or circle
        me.item.append("ellipse")
            .attr("transform", function (d) {
                let t = "";
                t += " rotate(" + d.tilt + ")"
                return t;
            })
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", function (d) {
                let rx = d.size;
                if (d.type == 'Jumpgate') {
                    rx = 6;
                }

                return rx;
            })
            .attr("ry", function (d) {
                let ry = d.size;
                if (d.type == 'Jumpgate') {
                    ry = 9;
                }
                return ry;
            })
            .style("fill", function (d) {
                let tone = d.tone;
                if (d.type == 'Jumpgate') {
                    tone = 'None';
                }
                if (d.type == 'Gas Giant') {
                    tone = 'url(#gas_giant_gradient)';
                }
                if (d.type == 'Telluric') {
                    tone = 'url(#telluric_gradient)';
                }
                if (d.type == 'Sun') {
                    tone = 'url(#sun_gradient)';
                }

                return tone;
            })
            .style("stroke-width", function (d) {
                let sw = "1pt";
                if (d.type == 'Jumpgate') {
                    sw = '3pt';
                }
                return sw;
            })
            .style("stroke", function (d) {
                let stroke = me.design.stroke[d.type];
                return stroke;
            })
            .attr("opacity", function (d) {
                if ((d.type == "Space Station") | (d.type == "Asteroids Belt") | (d.type == "Allied Forces")) {
                    return 0.0;
                }
                if (d.type == "Sun") {
                    return 1.0;
                }
                return 1;
            });


        // Draw icon or ships
        me.item.append("path")
            .attr("transform", function (d) {
                let t = "";
                t += " rotate(" + d.tilt + ")"
                return t;
            })

            .attr("d", function (d) {
                let s = 7;
                let str = "M -" + s + " 0 L 0 " + s + ", " + s + " 0, 0 -" + s + ", -" + s + " 0  Z"
                return str;
            })
            .style("fill", function (d) {
                let tone = d.tone;
                if (d.type == 'Jumpgate') {
                    tone = 'None';
                }
                if (d.type == 'Space Station') {
                    tone = me.design.fill[d.type];
                }
                return tone;
            })
            .style("stroke-width", function (d) {
                let sw = "1pt";
                if (d.type == 'Jumpgate') {
                    sw = '3pt';
                }
                return sw;
            })
            .style("stroke", function (d) {
                let s = me.design.stroke[d.type];
                return s;
            })
            .attr("opacity", function (d) {
                if (d.type == "Space Station") {
                    return 1;
                }
                return 0.0;
            });

        // Flag
        me.item.append("path")
            .attr("transform", function (d) {
                let t = "";
                t += " rotate(" + d.tilt + ")"
                return t;
            })
            .attr("d", function (d) {
                let str = "M -16 -16 h 12 v 9 h -12 Z"
                return str;
            })
            .style("fill", function (d) {
                let tone = d.tone;
                return tone;
            })
            .style("stroke-width", "0.25pt")
            .style("stroke", "#FFF")
            .attr("opacity", function (d) {
                if ((d.type == "Space Station") | (d.type == "Allied Forces")) {
                    return 1;
                }
                return 0;
            });

        // Army
        me.item.append("path")
            .attr("d", function (d) {
                let ship = "m 4 0 l 2 1, -1 2, -3 2, 1 -2 h -1 v -1 l -2 1, 2 -2, 2 -1 "
                let str = "M 0 0 " + ship;
                str += "M 0 6 " + ship;
                str += "M 0 12 " + ship;
                str += "M 0 18 " + ship;
                str += "M 6 6 " + ship;
                str += "M 6 12 " + ship;
                str += "M 6 18 " + ship;
                str += "M -6 6 " + ship;
                str += "M -6 12 " + ship;
                str += "M 12 6 " + ship;
                str += "M 12 12 " + ship;

                return str;
            })
            .style("fill", "#DDD")
            .style("stroke-width", "0.1pt")
            .style("stroke", "#C8C")
            .attr("opacity", function (d) {
                if (d.type == "Allied Forces") {
                    return 0.75;
                }
                return 0.0;
            });

        me.transition();


    }

    transition() {
        let me = this
        me.item.transition()
            .duration(20000)
            .ease(d3.easeLinear)
            .attrTween("transform", me.translateAlong())
            // .each("end", this.transition)
        ;
    }


    drawLegend() {
        let me = this;

        me.legend.append('text')
            .attr("x", -13 * me.step_x)
            .attr("y", -3.0 * me.step_y)
            .style("fill", "#FFF")
            .style("stroke", "#444")
            .style("font-size", "20pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "start")
            .text(me.data.title.toUpperCase())

        me.legend.append('text')
            .attr("x", -14 * me.step_x)
            .attr("y", -2.25 * me.step_y)
            .style("fill", "#777")
            .style("stroke", "#111")
            .style("font-size", "96pt")
            .style("font-family", "FadingSunsicons")
            .style("text-anchor", "middle")
            .attr("opacity", 0.5)
            .text(me.data.symbol)


        me.legend.append('text')
            .attr("x", -13 * me.step_x)
            .attr("y", -2.65 * me.step_y)
            .style("fill", "#FFF")
            .style("stroke", "#777")
            .style("font-size", "16pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "start")
            .text(me.data.alliance.toUpperCase())


        // Square links for interaction
        me.links = me.planets
            .append("g")
            .on("mouseover", function (e, d) {
                d3.selectAll(".planet_text_" + d.id).style("opacity", 1.0)
                d3.selectAll(".planet_panel_" + d.id).style("opacity", 1.0)
            })
            .on("mouseout", function (e, d) {
                d3.selectAll(".planet_text_" + d.id).style("opacity", 0.0)
                d3.selectAll(".planet_panel_" + d.id).style("opacity", 0)
            });

        me.links.append("rect")
            .attr("x", function (d) {
                return d.id * 26 - 13 * me.step_x;
            })
            .attr("y", -2.5 * me.step_y)
            .attr("width", 20)
            .attr("height", 20)
            .style("stroke", "#888")
            .style("fill", function (d) {
                return d.tone
            })
            .attr("opacity", 0.8);
        me.links.append("text")
            .attr("dx", "1ex")
            .attr("dy", "1em")
            .attr("x", function (d) {
                return d.id * 26 - 13 * me.step_x;
            })
            .attr("y", -2.15 * me.step_y)
            .style("fill", "#EEE")
            .style("stroke", "#444")
            .style("stroke-width", "#0.25pt")
            .style("font-size", "8pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "start")
            .text(function (d) {
                return d.type[0].toUpperCase();
            })
    }

    drawPanels() {
        let me = this;
        // Display panel
        me.item.append("path")
            .attr("transform", function (d) {
                return "rotate(" + d.tilt + ")"
            })
            .attr('class', function (d) {
                return "planet_panel_" + d.id;
            })
            .attr("d", function (d) {
                let str = "M -5 -10 l -20 -15 h -180 v -80 h 180 v 55 v 15  Z"
                return str;
            })
            .style("fill", "#111")
            .style("stroke-width", "0.5pt")
            .style("stroke", "#CCC")
            .attr("opacity", 0);

        me.labels = me.item.append('g')
            .attr("transform", function (d) {
                return "rotate(" + (d.tilt) + ")";
            });

        me.labels.append('text')
            .attr('class', function (d) {
                return "planet_text_" + d.id
            })
            .attr("dx", -30)
            .attr("dy", -90)
            .style("opacity", 0)
            .style("fill", "#FFF")
            .style("stroke", "#777")
            .style("font-size", "10pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "end")
            .text(function (d) {
                return d.name;
            })
        me.labels.append('text')
            .attr('class', function (d) {
                return "planet_text_" + d.id
            })
            .attr("dx", -30)
            .attr("dy", -70)
            .style("opacity", 0)
            .style("fill", "#FFF")
            .style("stroke", "#333")
            .style("font-size", "10pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "end")
            .text(function (d) {
                return d.AU + " AU (" + d.type + ")";
            })
        me.labels.append('text')
            .attr('class', function (d) {
                return "planet_text_" + d.id
            })
            .attr("dx", -30)
            .attr("dy", -50)
            .style("opacity", 0)
            .style("fill", "#FFF")
            .style("stroke", "#777")
            .style("font-size", "10pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "end")
            .text(function (d) {
                if (d.type == "Sun") {
                    return "Zoom (Factor:" + me.data.zoom_factor + " Value:" + me.data.zoom_val + ")";
                }
                return d.moon;
            })
        me.labels.append('text')
            .attr('class', function (d) {
                return "planet_text_" + d.id
            })
            .attr("dx", -30)
            .attr("dy", -30)
            .style("opacity", 0)
            .style("fill", "#FFF")
            .style("stroke", "#333")
            .style("font-size", "10pt")
            .style("font-family", "VL Gothic")
            .style("text-anchor", "end")
            .text(function (d) {
                return d.description;
            })

    }


    perform() {
        let me = this;
        // Prepare SVG Layout
        $(me.parent).css("padding", 0);
        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h)
        ;
        me.svg = me.vis.append("g")
            .attr("class", "all")
            .attr('transform', function (d) {
                return "translate(" + (8 * me.width / 16) + "," + (4 * me.height / 8) + ")";
            })
            .append('g');
        ;


        me.buildGradients();

        me.svg.append('rect')
            .attr('x', -me.w / 2)
            .attr('y', -me.h / 2)
            .attr('width', me.w)
            .attr('height', me.h)
            .style("fill", "#110011")
            .style("fill-stroke", 1)
            .style("opacity", 0.5);


        // Planets parsing
        me.planets = me.svg.append('g')
            .attr("class", "planet")
            .selectAll("planet")
            .data(me.data.planets).enter();

        me.orbital_group = me.planets
            .append('g')
            .attr("transform", function (d) {
                let t = "";
                t += "translate(0," + (me.zoom_check(d.AU) ? -me.step_y * 5 : 0) + ") "
                t += "rotate(" + -d.tilt + ")"
                return t;
            });

        me.legend = me.svg.append('g');
        me.drawLayout();
        me.drawOrbits();
        me.drawPlanets();
        me.drawLegend();

        me.planets.exit().remove();
        me.drawPanels();
        me.zoomActivate();
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


}
