class FICSSheet {
    constructor(data, parent, collector) {
        let me = this;
        me.parent = parent;
        me.co = collector;
        me.config = data;
        me.init();
    }

    decorationText(x, y, d = 0, a = 'middle', f, s, b, c, w, t, v, o = 1) {
        let me = this;
        v.append('text')
            .attr("x", me.stepx * x)
            .attr("y", me.stepy * y)
            .attr("dy", d)
            .style("text-anchor", a)
            .style("font-family", f)
            .style("font-size", s + 'px')
            .style("fill", b)
            .style("stroke", c)
            .style("stroke-width", w + 'pt')
            .text(t)
            .attr('opacity', o);
    }

    init() {
        let me = this;
        me.debug = false;
        me.width = parseInt($(me.parent).css("width"), 10) * 0.75;
        me.height = me.width * 1.4;
        me.w = 1.25 * me.width;
        me.h = 1.25 * me.height;
        me.stepx = me.width / 24;
        me.stepy = me.height / 36;
        me.small_font_size = 1.5 * me.stepy / 5;
        me.medium_font_size = 2 * me.stepy / 5;
        me.big_font_size = 2.5 * me.stepy / 5;
        me.fat_font_size = 8 * me.stepy / 5;
        me.margin = [0, 0, 0, 0];
        me.dot_radius = me.stepx / 8;
        me.stat_length = 150;
        me.stat_max = 5;
        me.shadow_fill = "#B0B0B0";
        me.shadow_stroke = "#A0A0A0";
        me.jumpgate_stroke = "#B8B8B8";
        me.draw_stroke = '#111';
        me.draw_fill = '#222';
        me.user_stroke = '#911';
        me.user_fill = '#A22';
        me.user_font = 'Caveat';
        me.mono_font = 'Syne Mono';
        me.title_font = 'Pompiere';
        me.logo_font = 'Trade Winds';
        //me.logo_font = 'Reggae One';
        me.base_font = 'Voltaire';
        me.strokedebris = "90 12 125 15 25 3";
        me.strokedebris_short = "125 5 35 2 3 4 85 9";
        me.x = d3.scaleLinear().domain([0, me.width]).range([0, me.width]);
        me.y = d3.scaleLinear().domain([0, me.height]).range([0, me.height]);
        me.pre_title = me.config['pre_title'];
        me.scenario = me.config['scenario'];
        me.post_title = me.config['post_title'];
        me.health_levels = ['Bruised/X', 'Hurt/-1', 'Injured/-1', 'Wounded/-2', 'Mauled/-2', 'Crippled/-5', 'Incapacitated/X'];
        me.roots_shorts = [
            {'root': 'Arts', 'short': 'AR'},
            {'root': 'Dogma', 'short': 'DO'},
            {'root': 'Driving', 'short': 'DR'},
            {'root': 'Linguistics', 'short': 'LI'},
            {'root': 'Local Expert', 'short': 'LE'},
            {'root': 'Lore', 'short': 'LO'},
            {'root': 'Performance', 'short': 'PE'},
            {'root': 'Redemption', 'short': 'RE'},
            {'root': 'Science', 'short': 'SC'},
            {'root': 'Xenology', 'short': 'XE'}
        ]
    }

    midline(y, startx = 1, stopx = 23) {
        let me = this;
        me.back.append('line')
            .attr('x1', me.stepx * startx)
            .attr('x2', me.stepx * stopx)
            .attr('y1', me.stepy * y)
            .attr('y2', me.stepy * y)
            .style('fill', 'transparent')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '6pt')
            .style('stroke-dasharray', '90 5 140 3 450 7')
        //.attr('marker-end', "url(#arrowhead)")
        //.attr('marker-start', "url(#arrowhead)")
        ;
    }

    thinmidline(y, startx = 1, stopx = 23) {
        let me = this;
        me.back.append('line')
            .attr('x1', me.stepx * startx)
            .attr('x2', me.stepx * stopx)
            .attr('y1', me.stepy * y)
            .attr('y2', me.stepy * y)
            .style('fill', 'transparent')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '3pt')
            .style('stroke-dasharray', '90 5 140 3 450 7')
        ;
    }

    crossline(x, starty = 2, stopy = 35) {
        let me = this;
        me.back.append('line')
            .attr('x1', me.stepx * x)
            .attr('x2', me.stepx * x)
            .attr('y1', me.stepy * starty)
            .attr('y2', me.stepy * stopy)
            .style('fill', 'transparent')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '6pt')
            .style('stroke-dasharray', '90 5 140 3 450 7')
        // .attr('marker-end', "url(#arrowhead)")
        // .attr('marker-start', "url(#arrowhead)")
        ;
    }

    addCircle(radius, dash, target) {
        let me = this;
        target.append('circle')
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('r', me.stepx * radius)
            .style('fill', 'transparent')
            .style('stroke', me.jumpgate_stroke)
            .style('stroke-dasharray', dash)
            .style('stroke-width', '1pt')
        ;
    }

    drawJumpgateLogo(x, y) {
        let me = this;
        me.jumpgate = me.back.append('g')
            .attr('opacity', 0.35)
        ;
        me.jumpgate.append('circle')
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('r', me.stepx * 2.25)
            .style('fill', 'transparent')
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', '10pt');
        me.addCircle(0.9, "100 20 35 10 50 350 60 125", me.jumpgate);
        me.addCircle(1.0, "100 20 35 10 50 350 60 125", me.jumpgate);
        me.addCircle(2.0, "100 20 35 10 50 350 60 125", me.jumpgate);
        me.addCircle(2.6, "100 20 35 10 50 350 60 125", me.jumpgate);
        me.addCircle(4.0, "100 20 35 10 50 350 60 125", me.jumpgate);
        me.addCircle(4.2, "100 20 35 10 50 350 60 125", me.jumpgate);
        me.addCircle(8.3, "100 20 35 10 50 350 60 125", me.jumpgate);
        let s = me.stepx;
        let west = "M " + (-2.5 * s) + " " + (-0.5 * s)
            + " l " + (0 * s) + " " + (1 * s)
            + " l " + (1 * s) + " " + (-0.5 * s)
        ;
        let east = "M " + (+2.5 * s) + " " + (-0.5 * s)
            + " l " + (0 * s) + " " + (1 * s)
            + " l " + (-1 * s) + " " + (-0.5 * s)
        ;
        let south = "M " + (-0.5 * s) + " " + (+2.5 * s)
            + " l " + (1 * s) + " " + (0 * s)
            + " l " + (-0.5 * s) + " " + (-1 * s)
        ;
        let north = "M " + (-0.5 * s) + " " + (-2.5 * s)
            + " l " + (1 * s) + " " + (0 * s)
            + " l " + (-0.5 * s) + " " + (1 * s)
        ;
        me.jumpgate.append('path')
            .attr('d', west)
            .style('fill', me.jumpgate_stroke)
            .style('stroke', me.jumpgate_stroke)
            .style('stroke-width', '1pt');
        me.jumpgate.append('path')
            .attr('d', east)
            .style('fill', me.jumpgate_stroke)
            .style('stroke', me.jumpgate_stroke)
            .style('stroke-width', '1pt');
        me.jumpgate.append('path')
            .attr('d', north)
            .style('fill', me.jumpgate_stroke)
            .style('stroke', me.jumpgate_stroke)
            .style('stroke-width', '1pt');
        me.jumpgate.append('path')
            .attr('d', south)
            .style('fill', me.jumpgate_stroke)
            .style('stroke', me.jumpgate_stroke)
            .style('stroke-width', '1pt');
        me.jumpgate.attr('transform', 'translate(' + x + ',' + y + ') rotate(36)');
    }

    drawWatermark() {
        let me = this;
        d3.select(me.parent).selectAll("svg").remove();
        me.svg = d3.select(me.parent).append("svg")
            .attr("id", me.data['rid'])
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.width)
            .attr("height", me.height)
            .append("svg:g")
            .attr("transform", "translate(0,0)")
        // .call(d3.behavior.zoom().x(me.x).y(me.y).scaleExtent([2, 8]).on("zoom", function(e){
        //     })
        // )
        ;
        me.back = me.svg
            .append("g")
            .attr("class", "page")
            .attr("transform", "translate(" + 0 * me.stepx + "," + 0 * me.stepy + ")")
        ;
        me.defs = me.svg.append('defs');
        me.defs.append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 0)
            .attr('refY', 0)
            .attr('orient', 'auto-start-reverse')
            .attr('markerWidth', 9)
            .attr('markerHeight', 9)
            .attr('preserveAspectRatio', 'xMidYMid meet')
            .attr('xoverflow', 'visible')

            .append('svg:path')
            .attr('d', 'M 1,-1 l 3,1 -3,1 -1,-1 1,-1 M 5,-1 l  3,1 -3,1 -1,-1 1,-1   Z')
            .style('fill', me.draw_fill)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '0pt')
        ;
        me.back.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', me.width)
            .attr('height', me.height)
            .style('fill', 'white')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '0')
            .attr('opacity', 1.0)
        ;
        // Grid
        if (me.debug) {
            let verticals = me.back.append('g')
                .attr('class', 'verticals')
                .selectAll("g")
                .data(d3.range(0, 24, 1));
            verticals.enter()
                .append('line')
                .attr('x1', function (d) {
                    return d * me.stepx
                })
                .attr('y1', 0)
                .attr('x2', function (d) {
                    return d * me.stepx
                })
                .attr('y2', 36 * me.stepy)
                .style('fill', 'transparent')
                .style('stroke', '#CCC')
                .style('stroke-width', '0.25pt');
            let horizontals = me.back.append('g')
                .attr('class', 'horizontals')
                .selectAll("g")
                .data(d3.range(0, 36, 1));
            horizontals.enter()
                .append('line')
                .attr('x1', 0)
                .attr('x2', 24 * me.stepx)
                .attr('y1', function (d) {
                    return d * me.stepy
                })
                .attr('y2', function (d) {
                    return d * me.stepy
                })
                .style('fill', 'transparent')
                .style('stroke', '#CCC')
                .style('stroke-width', '0.25pt');
        }
        let lines = me.back.append('g');
        me.crossline(1, 2.3, 35.2);
        me.crossline(23, 2.3, 35.2);
        me.midline(2.5, 0.8, 23.2);
        me.midline(35, 0.8, 23.2);
        me.midline(12.25);
        me.thinmidline(22);
        me.midline(26);
        // Title
        let txt = 'Fading Suns'.toUpperCase();
        me.decorationText(12, 3.82, 0, 'middle', me.title_font, me.fat_font_size * 1.35, '#FFF', '#FFF', 25, txt, me.back, 1.0);
        me.drawJumpgateLogo(12 * me.stepx, 2.6 * me.stepy)
        me.decorationText(12, 3.82, 0, 'middle', me.title_font, me.fat_font_size * 1.35, me.draw_fill, me.draw_stroke, 1, txt, me.back, 1);
        me.decorationText(12, 4.8, 0, 'middle', me.title_font, 3 * me.fat_font_size / 5, me.draw_fill, me.draw_stroke, 0.5, me.scenario, me.back, 0.8);
        //me.decorationText(1.5, 35.8, -16, 'start', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, "Pancreator Vobiscum Sit", me.back);
        me.decorationText(22.5, 34.95, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "Fading Suns FICS Sheet 2021, Zaffarelli, created with DP", me.back);
        //me.decorationText(3, 1.75, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, "FuZion Interlock", me.back);
        me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, "FuZion Interlock Custom System v7.3", me.back);
        me.decorationText(21, 1.75, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.pre_title, me.back);
        me.decorationText(21, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.back);
        //me.decorationText(22.5, 34.8, 0, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, 'Challenge:' + me.data['freebies'], me.back);
        // Sheet content
        me.character = me.back.append('g')
            .attr('class', 'xover_sheet');
    }

    formatXml(xml) {
        var formatted = '';
        xml = xml.replace(/[\u00A0-\u2666]/g, function (c) {
            return '&#' + c.charCodeAt(0) + ';';
        })
        var reg = /(>)(<)(\/*)/g;
        /**/
        xml = xml.replace(reg, '$1\r\n$2$3');
        var pad = 0;
        jQuery.each(xml.split('\r\n'), function (index, node) {
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

    addButton(num, txt) {
        let me = this;
        let ox = 28 * me.stepy;
        let oy = 2 * me.stepy;
        let button = me.back.append('g')
            .attr('class', 'do_not_print')
        button.append('rect')
            .attr('id', "button" + num)
            .attr('x', ox + me.stepx * (-0.8))
            .attr('y', oy + me.stepy * (num - 0.4))
            .attr('width', me.stepx * 1.6)
            .attr('height', me.stepy * 0.8)
            .style('fill', '#CCC')
            .style('stroke', '#111')
            .style('stroke-width', '1pt')
            .attr('opacity', 1.0)
            .style('cursor', 'pointer')
            .on('mouseover', function (d) {
                me.svg.select('#button' + num).style("stroke", "#A22");
            })
            .on('mouseout', function (d) {
                me.svg.select('#button' + num).style("stroke", "#111");
            })
            .on('click', function (d) {
                if (num == 0) {
                    me.saveSVG();
                } else if (num == 1) {
                    me.savePNG();
                } else if (num == 2) {
                    me.savePDF();
                } else if (num == 3) {
                    me.editCreature();
                }
            })
        ;
        button.append('text')
            .attr('x', ox)
            .attr('y', oy + me.stepy * num)
            .attr('dy', 5)
            .style('font-family', me.base_font)
            .style('text-anchor', 'middle')
            .style("font-size", me.medium_font_size + 'px')
            .style('fill', '#000')
            .style('cursor', 'pointer')
            .style('stroke', '#333')
            .style('stroke-width', '0.5pt')
            .attr('opacity', 1.0)
            .text(txt)
            .on('mouseover', function (d) {
                me.svg.select('#button' + num).style("stroke", "#A22");
            })
            .on('mouseout', function (d) {
                me.svg.select('#button' + num).style("stroke", "#111");
            })
            .on('click', function (d) {
                if (num == 0) {
                    me.saveSVG();
                } else if (num == 1) {
                    me.savePNG();
                } else if (num == 2) {
                    me.savePDF();
                } else if (num == 3) {
                    me.editCreature();
                }
            })
        ;
    }

    drawButtons() {
        let me = this;
        me.addButton(0, 'Save SVG');
    }

    saveSVG() {
        let me = this;
        me.svg.selectAll('.do_not_print').attr('opacity', 0);
        let base_svg = d3.select("#d3area svg").html();
        let flist = '<style>';
        for (let f of me.config['fontset']) {
            flist += '@import url("https://fonts.googleapis.com/css2?family=' + f + '");';
        }
        flist += '</style>';

        let exportable_svg = '<?xml version="1.0" encoding="ISO-8859-1" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="crossover_sheet" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink"> \
' + flist + base_svg + '</svg>';
        let fname = me.data['rid'] + ".svg"
        let nuke = document.createElement("a");
        nuke.href = 'data:application/octet-stream;base64,' + btoa(me.formatXml(exportable_svg));
        nuke.setAttribute("download", fname);
        nuke.click();
        me.svg.selectAll('.do_not_print').attr('opacity', 1);
    }

    baseStat(name, value, ox, oy, source, pos = 0,fat = false) {
        let me = this;
        let item = source.append('g')
            .attr('class', 'fulldesc');

        if (me.debug) {
            item.append('rect')
                .attr('x', ox)
                .attr('y', oy)
                .attr('width', 5)
                .attr('height', 5)
                .style('fill', 'lime')
                .style('stroke', 'red')
                .style('stroke-width', '0.5pt')
            ;
        }

        item.append('rect')
            .attr('x', function (d) {
                if (pos == 1) {
                    return ox;
                } else if (pos == 2) {
                    return ox + me.stepx * 3.1;
                } else {
                    return ox;
                }
            })
            .attr('y', oy)
            .attr('rx', 8)
            .attr('width', function (d) {
                if (pos == 1) {
                    return me.stepx * 2.9;
                } else if (pos == 2) {
                    return me.stepx * 2.9;
                } else {
                    return me.stepx * 6;
                }
            })
            .attr('height', me.stepy * 0.8)
            .style('fill', 'transparent')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '1.5pt')
            .style('stroke-dasharray', me.strokedebris_short)
        ;
        item.append('text')
            .attr('x', function (d) {
                if (pos == 1) {
                    return ox;
                } else if (pos == 2) {
                    return ox + me.stepx * 3.1;
                } else {
                    return ox;
                }
            })
            .attr("y", oy)
            .attr("dx", 4)
            .attr("dy", me.stepy * 0.6)
            .style("text-anchor", 'start')
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.shadow_stroke)
            .style("stroke-width", '0.5pt')
            .text(function () {
                return name.charAt(0).toUpperCase() + name.slice(1);
            });
        item.append('text')
            .attr('x', function (d) {
                if (pos == 1) {
                    return ox + me.stepx * 2.9;
                } else if (pos == 2) {
                    return ox + me.stepx * 6;
                } else {
                    return ox + me.stepx * 6;
                }
            })
            .attr("y", oy)
            .attr("dx", -10)
            .attr("dy", me.medium_font_size*1.2)
            .style("text-anchor", 'end')
            .style("font-family", function (d) {
                return me.user_font;
            })
            .style("font-size", function(d){
                let res = me.small_font_size*1.2+'pt'
                if(fat){
                    res = me.medium_font_size*1.0+'pt';
                }
                return res;
            })
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", function(d){
                let res ='0.05pt'
                if (fat){
                    res = '0.50pt';
                }
                return res;
            })
            .text(function () {
                if (fat){
                    return value.toUpperCase();
                }
                return value;
            });

    }

    drawAttribute(name, desc, value, ox, oy, source, pos = 1) {
        let me = this;
        let item = source.append('g')
            .attr('class', 'attribute');
        if (me.debug) {
            item.append('rect')
                .attr('x', function (d) {
                    if (pos == 1) {
                        return ox + me.stepx * 0;
                    } else if (pos == 2) {
                        return ox + me.stepx * 3;
                    }
                })
                .attr('y', oy)
                .attr('width', 5)
                .attr('height', 5)
                .style('fill', 'lime')
                .style('stroke', 'red')
                .style('stroke-width', '0.5pt');
        }
        item.append('circle')
            .attr('cx', function (d) {
                if (pos == 2) {
                    return ox + me.stepx * 3.5;
                } else {
                    return ox + me.stepx * 2.5;
                }
            })
            .attr('cy', oy + me.stepy * 0.5)
            .attr('r', 0.4 * me.stepx)
            .style('fill', 'transparent')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '2pt')
        ;
        item.append('text')
            .attr('x', function (d) {
                if (pos == 2) {
                    return ox + 4 * me.stepx;
                } else {
                    return ox + 2 * me.stepx;
                }
            })
            .attr("y", oy + me.stepy * 0.4)
            .style("text-anchor", function (d) {
                if (pos == 2) {
                    return "start"
                } else {
                    return "end"
                }
            })
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size * 1.2 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.75pt')
            .text(function () {
                return name.charAt(0).toUpperCase() + name.slice(1);
            });
        item.append('text')
            .attr('x', function (d) {
                if (pos == 2) {
                    return ox + 4 * me.stepx;
                } else {
                    return ox + 2 * me.stepx;
                }
            })
            .attr("y", oy + me.stepy * 0.7)
            .style("text-anchor", function (d) {
                if (pos == 2) {
                    return "start"
                } else {
                    return "end"
                }
            })
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.shadow_stroke)
            .style("stroke-width", '0.5pt')
            .text(function () {
                return desc;
            });

        item.append('text')
            .attr('x', function (d) {
                if (pos == 2) {
                    return ox + me.stepx * 3.5 - 0.08 * me.stepx;
                } else {
                    return ox + me.stepx * 2.5 - 0.08 * me.stepx;
                }
            })
            .attr("y", oy + 0.60 * me.stepy)
            .style("text-anchor", 'middle')
            .style("font-family", function (d) {
                return me.user_font;
            })
            .style("font-size", (me.medium_font_size * 1.4) + 'px')
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.05pt')
            .text(function () {
                return value;
            });
    }

    fillAttributes(ot) {
        let me = this;
        let bx = 1 * me.stepx;
        let oy = ot + 0.5 * me.stepy;
        me.character.append('rect')
            .attr('x', bx + 0.5 * me.stepx)
            .attr('y', oy - 0.25 * me.stepy)
            .attr('rx', 10)
            .attr('width', 5 * me.stepx)
            .attr('height', 6.5 * me.stepy)
            .style("fill", 'transparent')
            .style("stroke", me.draw_stroke)
            .style("stroke-dasharray", "5 12 125 35 5 2 3 4 85 9")
            .style("stroke-width", '1pt')
        ;
        me.drawAttribute("STR", "strength", me.data["PA_STR"], bx, oy, me.character, 1)
        me.drawAttribute("CON", "constitution", me.data["PA_CON"], bx, oy, me.character, 2)
        me.drawAttribute("BOD", "body", me.data["PA_BOD"], bx, oy + 1 * me.stepy, me.character, 1)
        me.drawAttribute("MOV", "movement", me.data["PA_MOV"], bx, oy + 1 * me.stepy, me.character, 2)

        me.drawAttribute("INT", "intellect", me.data["PA_INT"], bx, oy + 2 * me.stepy, me.character, 1)
        me.drawAttribute("WIL", "willpower", me.data["PA_WIL"], bx, oy + 2 * me.stepy, me.character, 2)
        me.drawAttribute("TEM", "temper", me.data["PA_TEM"], bx, oy + 3 * me.stepy, me.character, 1)
        me.drawAttribute("PRE", "presence", me.data["PA_PRE"], bx, oy + 3 * me.stepy, me.character, 2)

        me.drawAttribute("TEC", "tech", me.data["PA_TEC"], bx, oy + 4 * me.stepy, me.character, 1)
        me.drawAttribute("REF", "reflexes", me.data["PA_REF"], bx, oy + 4 * me.stepy, me.character, 2)
        me.drawAttribute("AGI", "agility", me.data["PA_AGI"], bx, oy + 5 * me.stepy, me.character, 1)
        me.drawAttribute("AWA", "awareness", me.data["PA_AWA"], bx, oy + 5 * me.stepy, me.character, 2)

        bx = 6.5 * me.stepx;
        me.character.append('rect')
            .attr('x', bx + 0.5 * me.stepx)
            .attr('y', oy - 0.25 * me.stepy)
            .attr('rx', 10)
            .attr('width', 5 * me.stepx)
            .attr('height', 6.5 * me.stepy)
            .style("fill", 'transparent')
            .style("stroke", me.draw_stroke)
            .style("stroke-dasharray", me.strokedebris)
            .style("stroke-width", '1pt')
        ;
        me.drawAttribute("REC", "str+con", me.data["SA_REC"], bx, oy, me.character, 1)
        me.drawAttribute("STA", "bod/2-1", me.data["SA_STA"], bx, oy, me.character, 2)
        me.drawAttribute("END", "(BOD+CON)x5", me.data["SA_END"], bx, oy + 1 * me.stepy, me.character, 1)
        me.drawAttribute("STU", "BOD+CON", me.data["SA_STU"], bx, oy + 1 * me.stepy, me.character, 2)

        me.drawAttribute("RES", "WIL+PRE", me.data["SA_RES"], bx, oy + 2 * me.stepy, me.character, 1)
        me.drawAttribute("DMG", "STR/2-2", me.data["SA_DMG"], bx, oy + 2 * me.stepy, me.character, 2)
        me.drawAttribute("TOL", "TEM+WIL", me.data["SA_TOL"], bx, oy + 3 * me.stepy, me.character, 1)
        me.drawAttribute("HUM", "(TEM+WIL)x5", me.data["SA_HUM"], bx, oy + 3 * me.stepy, me.character, 2)

        me.drawAttribute("PAS", "TEM+AWA", me.data["SA_PAS"], bx, oy + 4 * me.stepy, me.character, 1)
        me.drawAttribute("WYR", "INT+REF", me.data["SA_WYR"], bx, oy + 4 * me.stepy, me.character, 2)
        me.drawAttribute("SPD", "REF/2", me.data["SA_SPD"], bx, oy + 5 * me.stepy, me.character, 1)
        me.drawAttribute("RUN", "MOVx2", me.data["SA_RUN"], bx, oy + 5 * me.stepy, me.character, 2)


    }

    fillBasics(oy) {
        let me = this;
        let bx = 16.75 * me.stepx;
        me.baseStat("Player", me.data["player"], bx, oy + me.stepy * 0, me.character,0,true);
        me.baseStat("Caste", me.data["caste"], bx, oy + me.stepy * 1, me.character);
        me.baseStat("Species", me.data["race"], bx, oy + me.stepy * 2, me.character);
        me.baseStat("Rank", me.data["rank"], bx, oy + me.stepy * 3, me.character);
        me.baseStat("Gender", me.data["gender"], bx, oy + me.stepy * 4, me.character, 1);
        me.baseStat("Age", me.data["age"], bx, oy + me.stepy * 4, me.character, 2);
        me.baseStat("Height (cm)", me.data["height"], bx, oy + me.stepy * 5, me.character, 1);
        me.baseStat("Weight (kg)", me.data["weight"], bx, oy + me.stepy * 5, me.character, 2);
        bx = 1.25 * me.stepx;
        me.baseStat("Name", me.data["full_name"], bx, oy + me.stepy * 0, me.character,0,true);
        me.baseStat("Alliance", me.data["alliance"], bx, oy + me.stepy * 1, me.character);
        bx = 12 * me.stepx;
        me.character.append('rect')
            .attr('x', bx + 0.5 * me.stepx)
            .attr('y', oy + 2.25 * me.stepy)
            .attr('rx', 10)
            .attr('width', 4 * me.stepx)
            .attr('height', 3.0 * me.stepy)
            .style("fill", 'transparent')
            .style("stroke", me.draw_stroke)
            .style("stroke-dasharray", "125 5 35 2 3 4 85 9")
            .style("stroke-width", '1pt')
        ;

        me.character.append('rect')
            .attr('x', bx + 0.5 * me.stepx)
            .attr('y', oy + 5.5 * me.stepy)
            .attr('rx', 10)
            .attr('width', 4 * me.stepx)
            .attr('height', 3.25 * me.stepy)
            .style("fill", 'white')
            .style("stroke", me.draw_stroke)
            .style("stroke-dasharray", "125 5 35 2 3 4 85 9")
            .style("stroke-width", '1pt')
        ;

        me.character.append('text')
            .attr('x',bx + 0.75 * me.stepx)
            .attr('y',oy + 2.85 * me.stepy)
            .attr('dx',0)
            .attr('dy',0)
            .text("Azurites")
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", me.medium_font_size*0.8 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
        ;

        me.character.append('text')
            .attr('x',bx + 0.75 * me.stepx)
            .attr('y',oy + 3.85 * me.stepy)
            .attr('dx',0)
            .attr('dy',0)
            .text("Diamonds")
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", me.medium_font_size*0.8 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
        ;

        me.character.append('text')
            .attr('x',bx + 0.75 * me.stepx)
            .attr('y',oy + 4.85 * me.stepy)
            .attr('dx',0)
            .attr('dy',0)
            .text("Rubies")
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", me.medium_font_size*0.8 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
        ;

        let azurites = me.character.append('g').selectAll('circle')
            .data([0,1,2,3,4])
            .enter();
        azurites.append('circle')
            .attr('cx', function(d){
                let res = bx + 2.5 * me.stepx + d*me.stepx*0.4;
                return res;
            })
            .attr('cy', oy + 2.75 * me.stepy)
            .attr('r', me.stepx * 0.15)
            .style('fill', 'white')
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', '2pt');

        let diamonds = me.character.append('g').selectAll('circle')
            .data([0,1,2,3,4])
            .enter();
        diamonds.append('circle')
            .attr('cx', function(d){
                let res = bx + 2.5 * me.stepx + d*me.stepx*0.4;
                return res;
            })
            .attr('cy', oy + 3.75 * me.stepy)
            .attr('r', me.stepx * 0.15)
            .style('fill', 'white')
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', '2pt');

        let rubies = me.character.append('g').selectAll('circle')
            .data([0,1,2,3,4])
            .enter();
        rubies.append('circle')
            .attr('cx', function(d){
                let res = bx + 2.5 * me.stepx + d*me.stepx*0.4;
                return res;
            })
            .attr('cy', oy + 4.75 * me.stepy)
            .attr('r', me.stepx * 0.15)
            .style('fill', 'transparent')
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', '2pt');

        me.character.append('rect')
            .attr('x', bx + 4.75 * me.stepx)
            .attr('y', oy + 6 * me.stepy)
            .attr('rx', 10)
            .attr('width', 6 * me.stepx)
            .attr('height', 2.75 * me.stepy)
            .style("fill", 'transparent')
            .style("stroke", me.draw_stroke)
            .style("stroke-dasharray", "125 5 35 2 36 4")
            .style("stroke-width", '1pt')
        ;

        me.wrap(me.data['entrance'], bx + 4.75 * me.stepx, oy + 6 * me.stepy ,6 * me.stepx);

    }


    wrap(txt, bx, by, width) {
        let me = this;
        let xo = bx+6,
            yo = by+me.medium_font_size;
        let text = me.character.append('text')
            .attr('x',xo)
            .attr('y',yo)
            .attr('dx',0)
            .attr('dy',0)
            .text(txt)
            .style("text-anchor", 'left')
            .style("font-family", me.user_font)
            .style("font-size", me.medium_font_size + 'px')
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.05pt')
        ;
        let words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = me.medium_font_size*1.1, // ems
            y = text.attr("y"),
            //dy = parseFloat(text.attr("dy")),
            tspan = text.text(null).append("tspan").attr("x", xo).attr("y", yo);//.attr("dy", dy);
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan").attr("x", xo).attr("y", yo).attr("dy", ++lineNumber * lineHeight).text(word);
            }
        }
    }


    fillSkills(basey) {
        let me = this;
        let oy = basey;
        let oy_spe = basey + 9.75 * me.stepy;
        let ox = 1.5 * me.stepx;
        let skills = me.character.append('g').selectAll('g')
            .data(me.data["skills_list"]);
        let skill_in = skills.enter();
        skill_in.append('line')
            .attr('x1', function (d) {
                let x = 0;
                if (!d['is_speciality']) {
                    x = ox + Math.floor(d.idx1 / 13) * (me.stepx * 4.25);
                } else {
                    x = ox + Math.floor(d.idx2 / 5) * (me.stepx * 4.25);
                }
                return x;
            })
            .attr('x2', function (d) {
                let x = 0;
                if (!d['is_speciality']) {
                    x = ox + (Math.floor((d.idx1) / 13)) * (me.stepx * 4.25) + 3.5 * me.stepx;
                } else {
                    x = ox + (Math.floor((d.idx2) / 5)) * (me.stepx * 4.25) + 3.5 * me.stepx;
                }
                return x;
            })
            .attr('y1', function (d) {
                let y = 0;
                if (!d['is_speciality']) {
                    y = oy + (d.idx1 % 13) * (me.stepy * 0.7) - 1;
                } else {
                    y = oy_spe + (d.idx2 % 5) * (me.stepy * 0.7) - 1;
                }
                return y;
            })
            .attr('y2', function (d) {
                let y = 0;
                if (!d['is_speciality']) {
                    y = oy + (d.idx1 % 13) * (me.stepy * 0.7) - 1;
                } else {
                    y = oy_spe + (d.idx2 % 5) * (me.stepy * 0.7) - 1;
                }
                return y;
            })
            .style("fill", me.shadow_fill)
            .style("stroke", me.shadow_stroke)
            .style("stroke-dasharray", "4 3")
            .style("stroke-width", '2pt')
            .attr("opacity", 0.3)
        ;
        skill_in
            .append('text')
            .attr('x', function (d, i) {
                let x = 0;
                if (!d['is_speciality']) {
                    x = ox + Math.floor(d.idx1 / 13) * (me.stepx * 4.25);
                } else {
                    x = ox + Math.floor(d.idx2 / 5) * (me.stepx * 4.25);
                }
                return x;
            })
            .attr('y', function (d, i) {
                let y = 0;
                if (!d['is_speciality']) {
                    y = oy + (d.idx1 % 13) * (me.stepy * 0.7);
                } else {
                    y = oy_spe + (d.idx2 % 5) * (me.stepy * 0.7);
                }
                return y;
            })
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", function (d) {
                if (d['is_speciality']) {
                    return me.small_font_size + 'px';
                } else {
                    return me.medium_font_size + 'px';
                }
            })
            .text(function (d) {
                    let stick = '';
                    let tag = '';
                    let skill = d['skill'];
                    if (d['is_root']) {
                        for (let i = 0; i < me.roots_shorts.length; i++) {
                            if (me.roots_shorts[i]['root'] == d['skill']) {
                                stick = '(' + me.roots_shorts[i]['short'] + ')';
                            }
                        }
                    }
                    if (d['is_speciality']) {
                        let words = d['skill'].split('(');
                        skill = words[1].split(')')[0];
                        for (let i = 0; i < me.roots_shorts.length; i++) {
                            if (me.roots_shorts[i]['root'] + ' ' == words[0]) {
                                tag = '(' + me.roots_shorts[i]['short'] + ') ';
                            }
                        }
                    }
                    return tag + skill + stick;
                }
            )
        ;
        skill_in.append('text')
            .attr(
                'x'
                ,

                function (d, i) {
                    let x = 0;
                    if (!d['is_speciality']) {
                        x = ox + Math.floor(d.idx1 / 13) * (me.stepx * 4.25) + (me.stepx * 3.5);
                    } else {
                        x = ox + Math.floor(d.idx2 / 5) * (me.stepx * 4.25) + (me.stepx * 3.5);
                    }
                    return x;
                }
            )
            .attr(
                'y'
                ,

                function (d, i) {
                    let y = 0;
                    if (!d['is_speciality']) {
                        y = oy + (d.idx1 % 13) * (me.stepy * 0.7);
                    } else {
                        y = oy_spe + (d.idx2 % 5) * (me.stepy * 0.7);
                    }
                    return y;
                }
            )
            .style(
                "fill"
                ,
                me
                    .user_fill
            )
            .style(
                "stroke"
                ,
                me
                    .user_stroke
            )
            .style(
                "stroke-width"
                ,
                '0.05pt'
            )
            .style(
                "text-anchor"
                ,
                'end'
            )
            .style(
                "font-family"
                ,
                me
                    .user_font
            )
            .style(
                "font-size"
                ,

                function (d) {
                    let size = me.medium_font_size * (1 + Math.floor(d.value / 3) * 0.5);
                    return size + 'px';
                }
            )
            .text(
                function (d) {
                    return d.value;
                }
            );
        skills.exit().remove();
    }

    fillCharacter() {
        let me = this;
        me.fillBasics(3 * me.stepy)
        me.fillAttributes(5 * me.stepy)
        me.fillSkills(13 * me.stepy)
    }

    perform(character_data) {
        let me = this;
        me.data = character_data;
        me.guideline = me.data['guideline']
        $(me.parent).css('display', 'block');
        me.drawWatermark();
        if (me.data['condition'] == "DEAD") {
            me.decorationText(12, 16, 0, 'middle', me.logo_font, me.fat_font_size * 3, me.shadow_fill, me.shadow_stroke, 0.5, "DEAD", me.back, 0.25);
        }
        me.fillCharacter();
        console.log(me.data);
        me.drawButtons();
    }
}


