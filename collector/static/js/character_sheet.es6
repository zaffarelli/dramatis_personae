/* Character Sheet Module, with everything about writing character data for tabletop usage */
class Sheet {
    constructor(data, parent, collector) {
        this.parent = parent;
        this.co = collector;
        this.config = data;
        this.disposition = 'portrait';
        this.xunits = 0;
        this.yunits = 0;

        console.debug("Character Sheet");
    }

    init() {
        let me = this;
        me.debug = false;
        me.blank = false;
        me.button_ox = 28;
        me.button_oy = 2;
        me.version = "0.9.5";
        if (me.disposition == 'portrait') {
            me.xunits = 24;
            me.yunits = 36;
            me.width = parseInt($(me.parent).css("width"), 10) * 0.75;
            me.height = me.width * 1.4;
            me.w = parseInt($(me.parent).css('width'));
            me.h = parseInt($(me.parent).css('height'));
            me.stepx = me.width / me.xunits;
            me.stepy = me.height / me.yunits;
        } else {
            me.xunits = 36;
            me.yunits = 24;
            me.width = parseInt($(me.parent).css("width"), 10) * 0.75;
            me.height = me.width / 1.4;
            me.w = parseInt($(me.parent).css('width'));
            me.h = parseInt($(me.parent).css('height'));
            me.stepx = me.width / me.xunits;
            me.stepy = me.height / me.yunits;
        }
        me.small_font_size = 12;
        me.medium_font_size = 14;
        me.big_font_size = 16;
        me.large_font_size = 22;
        me.fat_font_size = 8 * me.stepy / 5;

        me.small_inter = 0.5;

        me.margin = [0, 0, 0, 0];
        me.dot_radius = me.stepx / 8;
        me.stat_length = 150;
        me.stat_max = 5;
        me.shadow_fill = "#B0B0B0";
        me.shadow_stroke = "#A0A0A0";
        me.jumpgate_stroke = "#B8B8B8";
        me.draw_stroke = '#777';
        me.draw_fill = '#222';
        me.debug_stroke = '#FC4';
        me.debug_fill = '#FC8';
        me.user_stroke = '#888';
        me.user_fill = '#A22';
        me.user_font = 'Julee';//'East Sea Dokdo';
        me.mono_font = 'Syne Mono';
        me.title_font = 'Pompiere';
        me.logo_font = 'Trade Winds';
        me.base_font = 'Voltaire';
        me.strokedebris = "190 12 125 5 42 3";
        me.strokedebris_short = "125 5 35 2 3 4 85 9";
        me.x = d3.scaleLinear().domain([0, me.width]).range([0, me.width]);
        me.y = d3.scaleLinear().domain([0, me.height]).range([0, me.height]);

        me.pre_title = me.config['pre_title'];
        me.scenario = me.config['scenario'];
        me.post_title = me.config['post_title'];
        if (me.blank) {
            me.pre_title = "Pancreator Vobiscum Sit";
        }
        me.health_levels = ['Bruised/X', 'Hurt/-1', 'Injured/-1', 'Wounded/-2', 'Mauled/-2', 'Crippled/-5', 'Incapacitated/X'];
        me.roots_shorts = [
            {'root': 'Arts', 'short': 'A'},
            {'root': 'Dogma', 'short': 'B'},
            {'root': 'Driving', 'short': 'C'},
            {'root': 'Linguistics', 'short': 'D'},
            {'root': 'Local Expert', 'short': 'E'},
            {'root': 'Lore', 'short': 'F'},
            {'root': 'Performance', 'short': 'G'},
            {'root': 'Redemption', 'short': 'H'},
            {'root': 'Science', 'short': 'I'},
            {'root': 'Xenology', 'short': 'J'}
        ]
    }

    setButtonsOrigin(x, y) {
        let me = this;
        me.button_ox = x;
        me.button_oy = y;
    }


    // TOOLS ===========================================================================================================
    formatXml(xml) {
        let formatted = '';
        xml = xml.replace(/[\u00A0-\u2666]/g, function (c) {
            return '&#' + c.charCodeAt(0) + ';';
        })
        let reg = /(>)(<)(\/*)/g;
        /**/
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

    addButton(num, txt, action) {
        let me = this;
        let ox = me.button_ox * me.stepy;
        let oy = me.button_oy * me.stepy;
        let button = me.back.append('g')
            .attr('class', 'buttons do_not_print')
            .on('mouseover', function (d) {
                me.svg.select('#button' + num).style("stroke", "#882");
            })
            .on('mouseout', function (d) {
                me.svg.select('#button' + num).style("stroke", "#111");
            })
            .on('click', function (d) {
                if (action == 'browse') {
                    me.perform(null, num - 1);
                } else {
                    if (num == 0) {
                        me.saveSVG();
                    } else {
                        $("#d3area").css("display", "none");
                    }
                }
            })

        button.append('rect')
            .attr('id', "button" + num)
            .attr('x', ox + me.stepx * (-0.8))
            .attr('y', oy + me.stepy * (num - 0.4))
            .attr('rx', '3mm')
            .attr('ry', '3mm')
            .attr('width', me.stepx * 1.6)
            .attr('height', me.stepy * 0.8)
            .style('fill', '#828')
            .style('stroke', '#111')
            .style('stroke-width', '1mm')
            .attr('opacity', 1.0)
            .style('cursor', 'pointer')
        ;
        button.append('text')
            .attr('x', ox)
            .attr('y', oy + me.stepy * num)
            .attr('dy', 5)
            .style('font-family', me.base_font)
            .style('text-anchor', 'middle')
            .style("font-size", me.small_font_size + 'pt')
            .style('fill', '#000')
            .style('cursor', 'pointer')
            .style('stroke', '#333')
            .style('stroke-width', '0.05pt')
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
                    // me.saveSVG();
                    me.createPDF();
                } else if (num == 1) {
                    console.log('Recto');
                    me.perform(null, 0);
                } else if (num == 2) {
                    me.perform(null, 1);
                    console.log('Verso');
                } else if (num == 3) {
                    $("#d3area").css("display", "none");
                }
            })
        ;
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
        let lpage = "";
        let exportable_svg = '<?xml version="1.0" encoding="ISO-8859-1" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="fics_sheet" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink"> \
' + flist + base_svg + '</svg>';

        if (me.page == 0) {
            lpage = "_recto";
        } else {
            lpage = "_verso"
        }
        let fname = me.data['rid'] + lpage + ".svg"
        let nuke = document.createElement("a");
        nuke.href = 'data:application/octet-stream;base64,' + btoa(me.formatXml(exportable_svg));
        nuke.setAttribute("download", fname);
        nuke.click();
        me.svg.selectAll('.do_not_print').attr('opacity', 1);
    }

    createPDF() {
        let me = this;
        me.svg.selectAll('.do_not_print').attr('opacity', 0);
        let base_svg = d3.select("#d3area svg").html();
        let flist = '<style>';
        for (let f of me.config['fontset']) {

            flist += '@import url("https://fonts.googleapis.com/css2?family=' + f + '");';
        }
        // console.log(flist)
        flist += '</style>';
        let lpage = "";
        let exportable_svg = '<?xml version="1.0" encoding="ISO-8859-1" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="fics_sheet" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink" width="' + me.width + '" height="' + me.height + '"> \
' + flist + base_svg + '</svg>';

        lpage = "_p" + me.page;
        let svg_name = me.data['rid'] + lpage + ".svg"
        let pdf_name = me.data['rid'] + lpage + ".pdf"
        let sheet_data = {
            'pdf_name': pdf_name,
            'svg_name': svg_name,
            'svg': exportable_svg
        }
        me.svg.selectAll('.do_not_print').attr('opacity', 1);
        $.ajax({
            url: 'ajax/character/svg2pdf/' + me.data['rid'] + '/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: sheet_data,
            dataType: 'json',
            success: function (answer) {
                console.log("PDF generated for [" + me.data['rid'] + "]...")
            },
            error: function (answer) {
                console.error('Error generating the PDF...: ' + pdf_name);
                console.error(answer);
            }
        });
    }

    // LOW LEVEL DRAW METHODS ==========================================================================================
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

    drawLine(x1 = 1, x2 = 23, y1 = 1, y2 = 35, fill = '#000000', stroke = '#888888', size = 1, dasharray = "", opacity = 1) {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawLine !')
        } else {
            me.daddy.append('line')
                .attr('x1', me.stepx * x1)
                .attr('x2', me.stepx * x2)
                .attr('y1', me.stepy * y1)
                .attr('y2', me.stepy * y2)
                .style('fill', fill)
                .style('stroke', stroke)
                .style('stroke-width', size + 'pt')
                .style('stroke-dasharray', dasharray)
                .style('stroke-linecap', 'round');
        }
    }

    drawRect(x = 1, y = 1, width = 1, height = 1, fill = "#000000", stroke = "#88888", size = 1, dasharray = "", opacity = 1.0, round = 0) {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawRect !')
        } else {
            me.daddy.append('rect')
                .attr('x', x * me.stepx)
                .attr('y', y * me.stepy)
                .attr('rx', round)
                .attr('width', width * me.stepx)
                .attr('height', height * me.stepy)
                .style('fill', fill)
                .style('stroke', stroke)
                .style('stroke-width', size + 'pt')
                .style('stroke-dasharray', dasharray)
            ;
        }
    }

    drawText(x = 1, y = 1, fill = '#000000', stroke = '#888888', size = 10, position = 'start', text = 'n/a', opacity, font = "default") {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawLine !')
        } else {
            let f;
            if (font == 'default') {
                f = me.base_font;
            } else {
                f = font;
            }
            me.daddy.append('text')
                .attr('x', me.stepx * x)
                .attr('y', me.stepy * y)
                .style('fill', fill)
                .style('stroke', stroke)
                .style('stroke-width', '0.05pt')
                .style("text-anchor", position)
                .style("font-size", size + 'pt')
                .style("font-family", f)
                .text(text);
        }
    }

    drawCircle(radius, dash, x = 0, y = 0, width = 1) {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawCircle !')
        } else {
            me.daddy.append('circle')
                .attr('cx', x)
                .attr('cy', y)
                .attr('r', me.stepx * radius)
                .style('fill', 'transparent')
                .style('stroke', me.jumpgate_stroke)
                .style('stroke-dasharray', dash)
                .style('stroke-width', width + 'pt')
            ;
        }
    }

    drawPath(d, x, y, fill, stroke) {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawPath !')
        } else {
            let path = me.daddy.append('path')
                .attr('d', d)
                .style('fill', fill)
                .style('stroke', stroke)
                .style('stroke-width', '1pt');
            path.append('transform', "translate(" + x + "," + y + ")");
        }
    }

    //==================================================================================================================
    drawJumpgateLogo(x, y) {
        let me = this;
        let dad = me.daddy;
        me.jumpgate = me.back.append('g').attr('opacity', 0.65);
        me.daddy = me.jumpgate;
        me.drawCircle(2.25, "", 0, 0, 10);
        me.drawCircle(0.9, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(1.0, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(2.0, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(2.6, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(4.0, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(4.2, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(8.3, "100 20 35 10 50 350 60 125", 0, 0);
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
        me.drawPath(west, 0, 0, me.jumpgate_stroke, me.jumpgate_stroke);
        me.drawPath(east, 0, 0, me.jumpgate_stroke, me.jumpgate_stroke);
        me.drawPath(south, 0, 0, me.jumpgate_stroke, me.jumpgate_stroke);
        me.drawPath(north, 0, 0, me.jumpgate_stroke, me.jumpgate_stroke);
        me.daddy.attr('transform', 'translate(' + x + ',' + y + ') rotate(36)');
        me.daddy = dad;
    }

    wrap(par, bx, by, width, font = 'default') {
        let me = this;
        let xo = bx,
            yo = by;
        if (font == 'default') {
            font = me.user_font;
        }
        let text = me.daddy.append('text')
            .attr('x', xo * me.stepx)
            .attr('y', yo * me.stepy)
            .attr('dx', 0)
            .attr('dy', 0)
            .text(par)
            .style("text-anchor", 'left')
            .style("font-family", font)
            .style("font-size", me.small_font_size + 'pt')
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.05pt');
        let words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = me.small_font_size+2,
            x = text.attr("x"),
            y = text.attr("y"),
            tspan = text.text(null).append("tspan")
                .attr("x", x)
                .attr("y", y);
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width * me.stepy) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan")
                    .attr("x", x)
                    .attr("y", y)
                    .attr("dy", ++lineNumber * lineHeight)
                    .style("font-size", me.small_font_size + 'pt')
                    .style("stroke-width", '0.05pt')
                    .text(word);
            }
        }
        return (lineNumber);
    }

    drawWatermark(page = 0) {
        let me = this;
        me.page = page;
        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h);
        me.svg = me.vis.append('g')
            .attr("id", me.data['rid'])
            // .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.width)
            .attr("height", me.height)
            .append("svg:g")
            .attr("transform", "translate(0,0)")
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
                .data(d3.range(0, me.xunits, 1));
            verticals.enter()
                .append('line')
                .attr('x1', function (d) {
                    return d * me.stepx
                })
                .attr('y1', 0)
                .attr('x2', function (d) {
                    return d * me.stepx
                })
                .attr('y2', me.yunits * me.stepy)
                .style('fill', 'transparent')
                .style('stroke', '#CCC')
                .style('stroke-width', '0.25pt');
            let horizontals = me.back.append('g')
                .attr('class', 'horizontals')
                .selectAll("g")
                .data(d3.range(0, me.yunits, 1));
            horizontals.enter()
                .append('line')
                .attr('x1', 0)
                .attr('x2', me.xunits * me.stepx)
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
        me.drawPages(page);
    }

    drawPages(page = 0) {
        let me = this;
    }

    perform(character_data = null, page = 0) {
        console.debug('Sheet perform for page: ' + page);
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

    fillKarma(ox, oy) {
        let me = this;
        me.drawRect(ox + 0.5, oy + 0.75, 1, 1, "transparent", me.draw_fill, 3);
        me.drawRect(ox + 2.0, oy + 0.75, 1, 1, "transparent", me.shadow_stroke, 1);
        me.drawRect(ox + 3.5, oy + 0.75, 1, 1, "transparent", me.shadow_stroke, 1);
        me.drawText(ox + 1, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Wyrd", 1.0);
        me.drawText(ox + 2.5, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Current", 1.0);
        me.drawText(ox + 4.0, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Tabernacle", 1.0);
        if (me.blank === false) {
            me.drawText(ox + 1, oy + 1.37, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["SA_WYR"], 1.0, me.user_font);
        }

    }


    fillArmors(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        styles["labels"] = ["Armor", "Cat", "HE", 'TO', 'SA', 'WA', 'SL', 'WL', 'Enc', 'TL']
        styles["properties"] = ["reference", "category", "he_sp", 'to_sp', 'sa_sp', 'wa_sp', 'sl_sp', 'wl_sp', 'encumbrance', 'tech_level']
        styles["aligns"] = ["start", "start", "start", "start", "start", "start", "start", "start", "start"]
        styles["widths"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        styles["lefts"] = [0, 4, 6, 6.5, 7, 7.5, 8, 8.5, 9, 10]
        me.fillList(basex, basey, "armors", styles);
    }

    fillWeapons(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        styles["labels"] = ["Weapon", "Cat", "Caliber", 'WA', 'DC', 'RE', 'CO', 'Clip', 'ROF', 'RNG']
        styles["properties"] = ["reference", "category", "caliber", 'weapon_accuracy', 'damage_class', 'rel', 'conceilable', 'clip', 'rof', 'rng']
        styles["aligns"] = ["start", "start", "start", "start", "start", "start", "start", "start", "start", "start"]
        styles["widths"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        styles["lefts"] = [0, 4, 5, 6, 7, 9, 10, 11, 12, 13]
        me.fillList(basex, basey, "weapons", styles);
    }

    fillBC(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        styles["labels"] = ["Blessing/Curse", "Value", "Description"]
        styles["properties"] = ["reference", "value", "description"]
        styles["aligns"] = ["multiline", "start", "multiline"]
        styles["widths"] = [2, 0, 6.5]
        styles["lefts"] = [0, 2.5, 3.5]
        me.fillList(basex, basey, "BC", styles);
    }

    fillBA(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        styles["labels"] = ["Benefice/Affliction", "Value", "Description", "Note"]
        styles["properties"] = ["benefice_affliction_ref__reference", "benefice_affliction_ref__value", "benefice_affliction_ref__description", "description"]
        styles["aligns"] = ["multiline", "start", "multiline", "multiline"]
        styles["widths"] = [2, 0, 4.5, 3]
        styles["lefts"] = [0, 2.5, 3.5, 8]
        me.fillList(basex, basey, "BA", styles);
    }

    fillToDs(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        console.log(me.data["tods"])
        styles["labels"] = ["Cat", "Tour of Duty", "Pts","Details"]
        styles["properties"] = ["category", "reference", "value","description"]
        styles["aligns"] = ["start", "start", "start","multiline"]
        styles["widths"] = [0, 5, 0,16]
        styles["lefts"] = [0, 0.5, 5,6]
        me.fillList(basex, basey, "tods", styles);
    }

    fillOccult(basex = 0, basey = 0) {
        let me = this;
        me.drawRect(basex + 9.75, basey - 0.25, 0.75, 0.75, "transparent", me.draw_stroke, 2, "", 1, 5);
        me.drawRect(basex + 9.75, basey + 0.75, 0.75, 0.75, "transparent", me.draw_stroke, 2, "", 1, 5);
        me.drawText(basex, basey, me.draw_fill, me.draw_stroke, me.medium_font_size, "start", "Occult Arts", 1.0, me.base_font);
        me.drawText(basex, basey + 0.60, me.draw_fill, me.draw_stroke, me.small_font_size, "start", "Stigma:", 1.0, me.base_font);
        me.drawText(basex, basey + 1.10, me.draw_fill, me.draw_stroke, me.small_font_size, "start", "Pathes:", 1.0, me.base_font);
        me.drawText(basex + 9.00, basey + 0.25, me.draw_fill, me.draw_stroke, me.medium_font_size, "start", "LVL", 1.0, me.base_font);
        me.drawText(basex + 9.00, basey + 1.25, me.draw_fill, me.draw_stroke, me.medium_font_size, "start", "DRK", 1.0, me.base_font);
        if (!me.blank) {
            me.drawText(basex + 2.0, basey + 0.60, me.user_fill, me.user_stroke, me.medium_font_size, "start", me.data['stigma'], 1.0, me.user_font);
            me.drawText(basex + 2.0, basey + 1.10, me.user_fill, me.user_stroke, me.medium_font_size, "start", me.data['path'], 1.0, me.user_font);
            me.drawText(basex + 10.125, basey + 0.25, me.user_fill, me.user_stroke, me.medium_font_size, "start", me.data['OCC_LVL'], 1.0, me.user_font);
            me.drawText(basex + 10.125, basey + 1.25, me.user_fill, me.user_stroke, me.medium_font_size, "start", me.data['OCC_DRK'], 1.0, me.user_font);
        }
        let styles = {}
        styles["labels"] = ["Lvl", "Path", "Ritual", "G", "L", "P", "W", "Att", "Skill", "Value"]
        styles["properties"] = ["ref__level", "ref__path", "ref__reference", "ref__gesture|bool", "ref__liturgy|bool", "ref__prayer|bool", "ref__wyrd_cost", "attribute_name", "skill_name", "value"]
        styles["aligns"] = ["start", "start", "multiline", "start", "start", "start", "start", "start", "start", "start"]
        styles["widths"] = [0, 0, 3.5, 0, 0, 0, 0, 0, 0, 0]
        styles["lefts"] = [0, 0.5, 2.5, 6.0, 6.25, 6.5, 7.0, 7.5, 8.5, 9.5]
        me.fillList(basex, basey + 2.0, "rituals", styles);
    }

    fillWallet(basex = 0, basey = 0) {
        let me = this;
        me.drawText(basex, basey, me.draw_fill, me.draw_stroke, me.medium_font_size, "start", "Assets & Money", 1.0, me.base_font);
        me.drawText(basex, basey + 0.60, me.draw_fill, me.draw_stroke, me.small_font_size, "start", "Wallet Money:", 1.0, me.base_font);
        me.drawText(basex, basey + 1.10, me.draw_fill, me.draw_stroke, me.small_font_size, "start", "Bank Accounts:", 1.0, me.base_font);

        if (!me.blank) {
            // me.drawText(basex + 2.0, basey + 0.60, me.user_fill, me.user_stroke, me.small_font_size, "start", me.data['stigma'], 1.0, me.user_font);
            // me.drawText(basex + 2.0, basey + 1.10, me.user_fill, me.user_stroke, me.small_font_size, "start", me.data['path'], 1.0, me.user_font);
            // me.drawText(basex + 9.9, basey + 0.30, me.user_fill, me.user_stroke, me.large_font_size, "start", me.data['OCC_LVL'], 1.0, me.user_font);
            // me.drawText(basex + 9.9, basey + 1.30, me.user_fill, me.user_stroke, me.large_font_size, "start", me.data['OCC_DRK'], 1.0, me.user_font);
        }

    }

    fillGear(basex = 0, basey = 0) {
        let me = this;
        me.drawText(basex, basey, me.draw_fill, me.draw_stroke, me.medium_font_size, "start", "Possessions, Gear & Equipment", 1.0, me.base_font);
    }

    fillShortcuts(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        styles["labels"] = ["Shortcut", "Label", "Score"]
        styles["properties"] = ["rationale", "label", "score"]
        styles["aligns"] = ["multiline", "multiline", "start"]
        styles["widths"] = [5, 4, 0]
        styles["lefts"] = [0, 5.5, 9.5]
        me.fillList(basex, basey, "shortcuts", styles);
    }

    fillShield(basex = 0, basey = 0) {
        let me = this;
        let styles = {}
        me.drawText(basex, basey, me.draw_fill, me.draw_stroke, me.medium_font_size, "start", "Energy Shields", 1.0, me.base_font);
        styles["labels"] = ["Shield", "min", "MAX", "Hits"]
        styles["properties"] = ["reference", "protection_min", "protection_max", "hits"]
        styles["aligns"] = ["start", "start", "start"]
        styles["widths"] = [0, 0, 0, 0]
        styles["lefts"] = [0, 2.25, 2.85, 3.5]
        me.fillList(basex, basey + me.small_inter, "shields", styles);
    }


    fillPicture(basex, basey) {
        let me = this;
        let imglnk = 'media/images/f_' + me.data["rid"] + ".jpg";
        let x = new Image();
        x.src = imglnk;
        x.on_load = function () {
            me.daddy = me.character;
            me.daddy.append("svg:image")
                .attr("xlink:href", function (d) {
                    return imglnk;
                })
                .attr("x", basex * me.stepx)
                .attr("y", basey * me.stepy)
                .attr("width", 3.5 * me.stepx)
                .attr("height", 5 * me.stepx)
                .attr("class", "do_not_print")
            ;
        }
    }


    fillList(basex = 0, basey = 0, datasource = "ba", styles = {}) {
        let me = this;
        let ox = basex, oy = basey, lines = 1, offset = 0;
        let w = 0, l = 1;
        _.forEach(styles['lefts'], function (e, i) {
            if (e > w) {
                w = e;
            }
        });
        me.daddy = me.character.append("g").attr('class', datasource + 's');

        // Labels
        _.forEach(styles['labels'], function (e, i) {
            me.drawText(ox + styles["lefts"][i], oy, me.draw_fill, me.draw_stroke, me.small_font_size, "start", e);
        });
        _.forEach(me.data[datasource], function (e, i) {
            // let o = JSON.parse(e);
            let meta = "";
            let stroke = me.user_stroke,
                fill = me.user_fill,
                font = me.user_font,
                size = me.small_font_size,
                opac = 1.0, biggest = 0,
                small_inter = me.small_inter * 0.75;
            if (!me.blank) {
                l = 0;
                offset = i + (biggest) * small_inter;
                oy = basey + small_inter + offset;
                biggest = 0;
                _.forEach(styles["properties"], function (y, j) {
                    if (styles["aligns"][j] == "multiline") {
                        let data = undefined;
                        let a = y.split('|');
                        let x = a[0];
                        let z = undefined;
                        if (a.length == 2) {
                            z = a[1];
                        }

                        let property_components = x.split('__');
                        if (property_components.length < 2) {
                            data = e[x]
                        } else {
                            data = e[property_components[0]][property_components[1]]
                        }
                        if (z == undefined) {

                        } else if (z == "bool") {
                            if (data == false) {
                                data = "."
                            } else {
                                data = "x";
                            }
                        } else if (z == "lower") {
                            data = data.toLowerCase();
                        }
                        lines = me.wrap(data, ox + styles["lefts"][j], oy, styles["widths"][j], font) + 1;
                    } else {
                        lines = 0;
                    }
                    if (lines > biggest) {
                        biggest = lines;
                    }
                });
                _.forEach(styles["properties"], function (y, j) {
                    if (styles["aligns"][j] != "multiline") {
                        let data = undefined;
                        let a = y.split('|');
                        let x = a[0];
                        let z = undefined;
                        if (a.length == 2) {
                            z = a[1];
                        }
                        let property_components = x.split('__');
                        if (property_components.length < 2) {
                            data = e[x]
                        } else {
                            data = e[property_components[0]][property_components[1]]
                        }
                        if (z == undefined) {

                        } else if (z == "bool") {
                            if (data == false) {
                                data = "."
                            } else {
                                data = "x";
                            }
                        } else if (z == "lower") {
                            data = data.toLowerCase();
                        }
                        me.drawText(ox + styles["lefts"][j], oy, fill, stroke, size, styles["aligns"][j], data, opac, font);
                    }
                });
            }
        });
        if (me.debug) {
            me.drawRect(basex, basey + 0.25, w + 0.5 + styles["widths"][styles["widths"].length - 1], oy - basey, "transparent", '#A22')
        }
    }

    limbColumn(basex, basey, limb = "x") {
        let me = this;
        let oy = basey;
        let ox = basex;
        me.daddy = me.character;
        me.drawRect(ox + 1, oy + 1, 0.8, 0.8, "transparent", me.draw_fill, 2);
        me.drawRect(ox + 1, oy + 2, 0.8, 0.8, "transparent", me.draw_fill, 2, "5 3");
        me.drawRect(ox + 1, oy + 3, 0.8, 0.8, "transparent", me.draw_fill, 4);

        me.drawText(ox + 1.7, oy + 1.7, me.shadow_fill, me.shadow_stroke, me.small_font_size - 4, "end", "SP", 1.0);
        me.drawText(ox + 1.7, oy + 2.7, me.shadow_fill, me.shadow_stroke, me.small_font_size - 4, "end", "MW", 1.0);
        me.drawText(ox + 1.7, oy + 3.7, me.shadow_fill, me.shadow_stroke, me.small_font_size - 4, "end", "SW", 1.0);

    }

    fillExtras(basey) {
        let me = this;
        let oy = basey - 0.25;
        let ox = -0.5;
        me.daddy = me.character;
        me.drawText(ox + 3.25, oy + 0.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "HIT POINTS", 1.0);
        me.drawRect(ox + 2, oy + 1.0, 2.5, 1, "transparent", me.draw_fill, 4);
        me.drawText(ox + 2.5, oy + 2.50, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Stamina", 1.0);
        me.drawText(ox + 4.0, oy + 2.50, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Penality", 1.0);
        me.drawRect(ox + 2, oy + 2.75, 1, 1, "transparent", me.draw_fill, 2);
        me.drawRect(ox + 3.5, oy + 2.75, 1, 1, "transparent", me.draw_fill, 2);
        me.drawText(ox + 2.5, oy + 4.25, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Save", 1.0);
        me.drawText(ox + 4.0, oy + 4.25, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Shield Hits", 1.0);
        me.drawRect(ox + 2, oy + 4.5, 1, 1, "transparent", me.draw_fill, 2);
        me.drawRect(ox + 3.5, oy + 4.5, 1, 1, "transparent", me.draw_fill, 2);

        me.drawText(ox + 2.5, oy + 6.00, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Shield Power", 1.0);
        me.drawText(ox + 4.0, oy + 6.00, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Trigger Range", 1.0);
        me.drawRect(ox + 2, oy + 6.25, 1, 1, "transparent", me.draw_fill, 2);
        me.drawRect(ox + 3.5, oy + 6.25, 1, 1, "transparent", me.draw_fill, 2);

        if (me.blank === false) {
            me.drawText(ox + 2.5, oy + 1.5, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["SA_END"], 1.0, me.user_font);
            me.drawText(ox + 2.5, oy + 3.25, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["SA_STA"], 1.0, me.user_font);
            me.drawText(ox + 2.5, oy + 5, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["SA_STU"], 1.0, me.user_font);

            if (me.data['shields'].length > 0) {
                let shield = me.data['shields'][0]
                me.drawText(ox + 2.5, oy + 6.75, me.user_fill, me.user_stroke, me.medium_font_size, "middle", shield.hits, 1.0, me.user_font);
                me.drawText(ox + 4.0, oy + 6.75, me.user_fill, me.user_stroke, me.medium_font_size, "middle", shield.protection_min + "/" + shield.protection_max, 1.0, me.user_font);
            }

        }
        let locstring = [
            "Head ........... 12 ",
            "Strong Arm .. 10-11 ",
            "Torso ......... 7-9 ",
            "Weak Arm ...... 5-6 ",
            "Strong Leg .... 3-4 ",
            "Weak Leg ...... 1-2 "];
        _.forEach(locstring, function (v, k) {
            me.drawText(ox + 2.0, oy + 8.0 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "left", v, 1.0, me.mono_font);
        });


        ox = 5;
        me.drawText(ox + 0.4, oy + 1.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "WA", 1.0);
        me.drawText(ox + 1.4, oy + 0.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Head", 1.0);
        me.drawText(ox + 2.4, oy + 1.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "SA", 1.0);
        me.limbColumn(ox - 1, oy + 1);
        me.limbColumn(ox, oy);
        me.limbColumn(ox + 1, oy + 1);

        if (!me.blank) {
            if (me.data["armors"].length > 0) {
                let armor = me.data["armors"][0]
                if (armor.left_arm) {
                    me.drawText(ox + 0.4, oy + 2.50, me.user_fill, me.user_stroke, me.medium_font_size, "middle", armor.stopping_power, 1.0, me.user_font);
                }
                if (armor.head) {
                    me.drawText(ox + 1.4, oy + 1.50, me.user_fill, me.user_stroke, me.medium_font_size, "middle", armor.stopping_power, 1.0, me.user_font);
                }
                if (armor.right_arm) {
                    me.drawText(ox + 2.4, oy + 2.50, me.user_fill, me.user_stroke, me.medium_font_size, "middle", armor.stopping_power, 1.0, me.user_font);
                }
                if (armor.left_leg) {
                    me.drawText(ox + 0.4, oy + 6.50, me.user_fill, me.user_stroke, me.medium_font_size, "middle", armor.stopping_power, 1.0, me.user_font);
                }
                if (armor.torso) {
                    me.drawText(ox + 1.4, oy + 5.50, me.user_fill, me.user_stroke, me.medium_font_size, "middle", armor.stopping_power, 1.0, me.user_font);
                }
                if (armor.right_leg) {
                    me.drawText(ox + 2.4, oy + 6.50, me.user_fill, me.user_stroke, me.medium_font_size, "middle", armor.stopping_power, 1.0, me.user_font);
                }
            }
        }


        oy += 4;
        me.drawText(ox + 0.4, oy + 1.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "WL", 1.0);
        me.drawText(ox + 1.4, oy + 0.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Torso", 1.0);
        me.drawText(ox + 2.4, oy + 1.75, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "SL", 1.0);
        me.limbColumn(ox - 1, oy + 1);
        me.limbColumn(ox, oy);
        me.limbColumn(ox + 1, oy + 1);
        me.fillSanity(8.5, 25);
        me.fillGlamour(8.5, 28.5);
        me.fillKarma(8.5, 33);


        let constitution = 5;
        let body = 5;
        let wstep = 0.14;

        if (me.blank === false) {
            constitution = me.data['PA_CON'];
            body = me.data['PA_BOD'];
        }

        me.drawRect(5.0, oy + 5.5, wstep * body, 0.15, me.shadow_fill, me.shadow_stroke, 1);
        me.drawRect(5.0 + wstep * body, oy + 5.5, wstep * (constitution), 0.15, me.shadow_fill, me.draw_stroke, 1, "5 3");
        me.drawRect(5.0 + wstep * (body + constitution), oy + 5.5, wstep * (20 - constitution - body), 0.15, me.shadow_fill, me.draw_stroke, 2);

        me.drawText(5.0 + wstep * body, oy + 5.35, me.draw_fill, me.draw_stroke, me.small_font_size - 4, "middle", body, 1.0);
        me.drawText(5.0 + wstep * (body + constitution), oy + 5.35, me.draw_fill, me.draw_stroke, me.small_font_size - 4, "middle", (body + constitution), 1.0);


        me.drawText(5.0 + wstep * (body / 2), oy + 5.95, me.draw_fill, me.draw_stroke, me.small_font_size - 4, "middle", "ok", 1.0);
        me.drawText(5.0 + wstep * (body + constitution / 2), oy + 5.95, me.draw_fill, me.draw_stroke, me.small_font_size - 4, "middle", "MW", 1.0);
        me.drawText(5.0 + wstep * ((body + constitution) + (20 - constitution - body) / 2), oy + 5.95, me.draw_fill, me.draw_stroke, me.small_font_size - 4, "middle", "SW", 1.0);


        if (me.blank === false) {
            me.wrap(me.data['narrative'], 14, 25.5, 9, me.user_font);
        }
    }

    fillSanity(ox, oy) {
        let me = this;
        me.drawRect(ox + 0.5, oy + 0.75, 1, 1, "transparent", me.draw_fill, 3);
        me.drawRect(ox + 2.0, oy + 0.75, 1, 1, "transparent", me.shadow_stroke, 1);
        me.drawRect(ox + 3.5, oy + 0.75, 1, 1, "transparent", me.shadow_stroke, 1);
        me.drawText(ox + 1.0, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Sanity", 1.0);
        me.drawText(ox + 2.5, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Psychosis", 1.0);
        me.drawText(ox + 4.0, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size - 3, "middle", "Incompatibility", 1.0);
        if (me.blank === false) {
            me.drawText(ox + 1, oy + 1.37, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["SA_HUM"], 1.0, me.user_font);
        }
        let lines = [0, 0.5];
        _.forEach(lines, function (e, i) {
            me.drawLine(ox + 0.5, ox + 4.5, oy + 2.5 + e, oy + 2.5 + e, me.shadow_fill, me.shadow_stroke, 0.5, "");
        })

    }

    fillGlamour(ox, oy) {
        let me = this;
        me.drawRect(ox + 0.5, oy + 0.75, 1, 1, "transparent", me.draw_fill, 3);
        me.drawRect(ox + 2.0, oy + 0.75, 1, 1, "transparent", me.shadow_stroke, 1);
        me.drawRect(ox + 3.5, oy + 0.75, 1, 1, "transparent", me.shadow_stroke, 1);
        me.drawText(ox + 1.0, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size, "middle", "Glamour", 1.0);
        me.drawText(ox + 2.5, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Current", 1.0);
        me.drawText(ox + 4.0, oy + 0.5, me.draw_fill, me.draw_stroke, me.small_font_size - 2, "middle", "Crushes", 1.0);
        if (me.blank === false) {
            me.drawText(ox + 1, oy + 1.37, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["SA_PAS"], 1.0, me.user_font);

        }
        let lines = [0, 0.5, 1.0, 1.5];
        _.forEach(lines, function (e, i) {
            me.drawLine(ox + 0.5, ox + 4.5, oy + 2.5 + e, oy + 2.5 + e, me.shadow_fill, me.shadow_stroke, 0.5, "");
        })
    }


    baseStat(name, value, ox, oy, source, pos = 0, fat = false) {
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
                .style('stroke-width', '0.5pt');
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
            .style("font-size", me.small_font_size + 'pt')
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
            .attr("dy", me.medium_font_size * 1.5)
            .style("text-anchor", 'end')
            .style("font-family", function (d) {
                return me.user_font;
            })
            .style("font-size", function (d) {
                let res = me.medium_font_size * 1.0 + 'pt'
                if (fat) {
                    res = me.medium_font_size * 1.1 + 'pt';
                }
                return res;
            })
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", function (d) {
                let res = '0.25pt'
                if (fat) {
                    res = '0.50pt';
                }
                return res;
            })
            .text(function () {
                if (me.blank) {
                    return "";
                }
                if (fat) {
                    return value.toUpperCase();
                }
                return value;
            });

    }

    drawAttribute(name, desc, value, ox, oy, source, pos = 1, scale = 10) {
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
            .style('stroke-width', function () {
                let size = 0;
                if (scale === 50) {
                    size = 4;
                } else if (scale === 10) {
                    size = 2;
                } else {
                    size = 1;
                }
                return size;
            })
            .style('stroke-dasharray', function () {
                let dash = 0;
                if (scale == 100) {
                    dash = "";
                } else if (scale == 10) {
                    dash = "";
                } else {
                    dash = "4 2 4 3";
                }
                return dash;
            })
        ;
        item.append('text')
            .attr('x', function (d) {
                if (pos == 2) {
                    return ox + 4 * me.stepx;
                } else {
                    return ox + 2 * me.stepx;
                }
            })
            .attr("y", oy + me.stepy * 0.2)
            .style("text-anchor", function (d) {
                if (pos == 2) {
                    return "start"
                } else {
                    return "end"
                }
            })
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size + 'pt')
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
            .text(function (d) {
                return desc;
            });

        item.append('text')
            .attr('x', function (d) {
                if (pos == 2) {
                    return ox + me.stepx * 3.5 - 0 * me.stepx;
                } else {
                    return ox + me.stepx * 2.5 - 0 * me.stepx;
                }
            })
            .attr("y", oy + 0.50 * me.stepy)
            .attr("dy", '4pt')
            .style("text-anchor", 'middle')
            .style("font-family", function (d) {
                return me.user_font;
            })
            // .style("font-size", (me.medium_font_size * 1.4) + 'px')
            .style("font-size", function () {
                let s = me.medium_font_size * 1.2;
                if (scale === 10) {
                    s = me.medium_font_size * (1 + Math.floor(value / 2) * 0.08);
                }
                return s + 'pt';
            })
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.05pt')
            .text(function () {
                if (me.blank) {
                    return "";
                }
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
        me.drawAttribute("REC", "STR+CON", me.data["SA_REC"], bx, oy, me.character, 1, 20)
        me.drawAttribute("STA", "BOD/2-1", me.data["SA_STA"], bx, oy, me.character, 2, 5)
        me.drawAttribute("END", "(BOD+CON)x5", me.data["SA_END"], bx, oy + 1 * me.stepy, me.character, 1, 100)
        me.drawAttribute("STU", "BOD+CON", me.data["SA_STU"], bx, oy + 1 * me.stepy, me.character, 2, 20)

        me.drawAttribute("RES", "WIL+PRE", me.data["SA_RES"], bx, oy + 2 * me.stepy, me.character, 1, 20)
        me.drawAttribute("DMG", "STR/2-2", me.data["SA_DMG"], bx, oy + 2 * me.stepy, me.character, 2, 5)
        me.drawAttribute("TOL", "TEM+WIL", me.data["SA_TOL"], bx, oy + 3 * me.stepy, me.character, 1, 20)
        me.drawAttribute("HUM", "(TEM+WIL)x5", me.data["SA_HUM"], bx, oy + 3 * me.stepy, me.character, 2, 100)

        me.drawAttribute("PAS", "TEM+AWA", me.data["SA_PAS"], bx, oy + 4 * me.stepy, me.character, 1, 20)
        me.drawAttribute("WYR", "INT+REF", me.data["SA_WYR"], bx, oy + 4 * me.stepy, me.character, 2, 20)
        me.drawAttribute("SPD", "REF/2", me.data["SA_SPD"], bx, oy + 5 * me.stepy, me.character, 1, 100)
        me.drawAttribute("RUN", "MOVx2", me.data["SA_RUN"], bx, oy + 5 * me.stepy, me.character, 2, 20)


    }

    fillBasics(oy) {
        let me = this;
        let bx = 16.75 * me.stepx;
        let basex = 12;
        let basey = 9;
        me.baseStat("Player", me.data["player"], bx, oy + me.stepy * 0, me.character, 0, true);
        me.baseStat("Caste", me.data["caste"], bx, oy + me.stepy * 1, me.character);
        me.baseStat("Species", me.data["race"], bx, oy + me.stepy * 2, me.character);
        me.baseStat("Rank", me.data["rank"], bx, oy + me.stepy * 3, me.character);
        me.baseStat("Gender", me.data["gender"], bx, oy + me.stepy * 4, me.character, 1);
        me.baseStat("Age", me.data["age"], bx, oy + me.stepy * 4, me.character, 2);
        me.baseStat("Height (cm)", me.data["height"], bx, oy + me.stepy * 5, me.character, 1);
        me.baseStat("Weight (kg)", me.data["weight"], bx, oy + me.stepy * 5, me.character, 2);
        bx = 1.25 * me.stepx;
        me.baseStat("", me.data["full_name"], bx, oy + me.stepy * 0, me.character, 0, true);
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
            .attr('x', bx + 0.75 * me.stepx)
            .attr('y', oy + 2.85 * me.stepy)
            .attr('dx', 0)
            .attr('dy', 0)
            .text("Azurites")
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", me.medium_font_size * 0.8 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
        ;

        me.character.append('text')
            .attr('x', bx + 0.75 * me.stepx)
            .attr('y', oy + 3.85 * me.stepy)
            .attr('dx', 0)
            .attr('dy', 0)
            .text("Diamonds")
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", me.medium_font_size * 0.8 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
        ;

        me.character.append('text')
            .attr('x', bx + 0.75 * me.stepx)
            .attr('y', oy + 4.85 * me.stepy)
            .attr('dx', 0)
            .attr('dy', 0)
            .text("Rubies")
            .style("text-anchor", 'left')
            .style("font-family", me.base_font)
            .style("font-size", me.medium_font_size * 0.8 + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.05pt')
        ;

        let azurites = me.character.append('g').selectAll('circle')
            .data([0, 1, 2, 3, 4])
            .enter();
        azurites.append('circle')
            .attr('cx', function (d) {
                let res = bx + 2.5 * me.stepx + d * me.stepx * 0.4;
                return res;
            })
            .attr('cy', oy + 2.75 * me.stepy)
            .attr('r', me.stepx * 0.15)
            .style('fill', 'white')
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', '2pt');

        let diamonds = me.character.append('g').selectAll('circle')
            .data([0, 1, 2, 3, 4])
            .enter();
        diamonds.append('circle')
            .attr('cx', function (d) {
                let res = bx + 2.5 * me.stepx + d * me.stepx * 0.4;
                return res;
            })
            .attr('cy', oy + 3.75 * me.stepy)
            .attr('r', me.stepx * 0.15)
            .style('fill', 'white')
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', '2pt');

        let rubies = me.character.append('g').selectAll('circle')
            .data([0, 1, 2, 3, 4])
            .enter();
        rubies.append('circle')
            .attr('cx', function (d) {
                let res = bx + 2.5 * me.stepx + d * me.stepx * 0.4;
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

        me.daddy = me.character;
        me.drawCircle(0.4, "5 2", bx + 1.25 * me.stepx, oy + 6.15 * me.stepy, 2);
        me.drawText(basex + 1.75, basey + 0.25, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Experience Earned");
        me.drawText(basex + 1.25, basey + 0.25, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["xp_earned"], 1, me.user_font);
        me.drawCircle(0.4, "5 2", bx + 1.25 * me.stepx, oy + 7.15 * me.stepy, 2);
        me.drawText(basex + 1.75, basey + 1.25, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Experience Spent");
        me.drawText(basex + 1.25, basey + 1.25, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["xp_spent"], 1, me.user_font);
        me.drawCircle(0.4, "5 2", bx + 1.25 * me.stepx, oy + 8.15 * me.stepy, 2);
        me.drawText(basex + 1.75, basey + 2.25, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Experience Pool");
        me.drawText(basex + 1.25, basey + 2.25, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["xp_pool"], 1, me.user_font);


        if (me.blank == false) {
            me.wrap(me.data['entrance'], basex + 5, basey + 0.5, 6, me.user_font);
        }


    }


    fillSkills(basey) {
        let me = this;
        me.spe_col_max = 3;
        let oy = basey;
        me.column_amount = 12;
        let oy_spe = basey + 7.5 * me.stepy;
        let ox = 1.5 * me.stepx;
        let skills = me.character.append('g').selectAll('g')
            .data(me.data["skills_list"]);
        let skill_in = skills.enter();
        skill_in.append('line')
            .attr('x1', function (d) {
                let x = 0;
                if (!d['is_speciality']) {
                    x = ox + Math.floor(d.idx1 / me.column_amount) * (me.stepx * 4.25);
                } else {
                    x = ox + Math.floor(d.idx2 / me.spe_col_max) * (me.stepx * 4.25);
                }
                return x;
            })
            .attr('x2', function (d) {
                let x = 0;
                if (!d['is_speciality']) {
                    x = ox + (Math.floor((d.idx1) / me.column_amount)) * (me.stepx * 4.25) + 3.5 * me.stepx;
                } else {
                    x = ox + (Math.floor((d.idx2) / me.spe_col_max)) * (me.stepx * 4.25) + 3.5 * me.stepx;
                }
                return x;
            })
            .attr('y1', function (d) {
                let y = 0;
                if (!d['is_speciality']) {
                    y = oy + (d.idx1 % me.column_amount) * (me.stepy * me.small_inter) - 1;
                } else {
                    y = oy_spe + (d.idx2 % me.spe_col_max) * (me.stepy * me.small_inter) - 1;
                }
                return y;
            })
            .attr('y2', function (d) {
                let y = 0;
                if (!d['is_speciality']) {
                    y = oy + (d.idx1 % me.column_amount) * (me.stepy * me.small_inter) - 1;
                } else {
                    y = oy_spe + (d.idx2 % me.spe_col_max) * (me.stepy * me.small_inter) - 1;
                }
                return y;
            })
            .style("fill", function (d) {
                if ((!d['is_speciality'])) {
                    return me.shadow_fill;
                }
                return "transparent";
            })
            .style("stroke", function (d) {
                if ((!d['is_speciality'])) {
                    return me.shadow_fill;
                }
                return me.shadow_fill;
                // return "transparent";
            })
            .style("stroke-dasharray", "4 3")
            .style("stroke-width", '2pt')
            .attr("opacity", 0.3)
        ;
        skill_in.append('text')
            .attr('x', function (d, i) {
                let x = 0;
                if (!d['is_speciality']) {
                    x = ox + Math.floor(d.idx1 / me.column_amount) * (me.stepx * 4.25);
                } else {
                    x = ox + Math.floor(d.idx2 / me.spe_col_max) * (me.stepx * 4.25);
                }
                return x;
            })
            .attr('y', function (d, i) {
                let y = 0;
                if (!d['is_speciality']) {
                    y = oy + (d.idx1 % me.column_amount) * (me.stepy * me.small_inter);
                } else {
                    y = oy_spe + (d.idx2 % me.spe_col_max) * (me.stepy * me.small_inter);
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
                    return me.small_font_size + 'pt';
                } else {
                    return me.small_font_size + 'pt';
                }
            })
            .text(function (d) {
                    let stick = '';
                    let tag = '';
                    let skill = d['skill'];
                    if (d['is_root']) {
                        for (let i = 0; i < me.roots_shorts.length; i++) {
                            if (me.roots_shorts[i]['root'] === d['skill']) {
                                stick = '(' + me.roots_shorts[i]['short'] + ')';
                            }
                        }
                    }
                    if (d['is_speciality']) {

                        let words = d['skill'].split('(');
                        skill = words[1].split(')')[0];
                        for (let i = 0; i < me.roots_shorts.length; i++) {
                            if (me.roots_shorts[i]['root'] + ' ' === words[0]) {
                                tag = '(' + me.roots_shorts[i]['short'] + ') ';
                            }
                        }
                        if (me.blank) {
                            return "";
                        }
                    }
                    return tag + skill + stick;
                }
            );
        skill_in.append('text')
            .attr('x', function (d) {
                    let x = 0;
                    if (!d['is_speciality']) {
                        x = ox + Math.floor(d.idx1 / me.column_amount) * (me.stepx * 4.25) + (me.stepx * 3.5);
                    } else {
                        x = ox + Math.floor(d.idx2 / me.spe_col_max) * (me.stepx * 4.25) + (me.stepx * 3.5);
                    }
                    return x;
                }
            )
            .attr('y', function (d) {
                    let y = 0;
                    if (!d['is_speciality']) {
                        y = oy + (d.idx1 % me.column_amount) * (me.stepy * me.small_inter);
                    } else {
                        y = oy_spe + (d.idx2 % me.spe_col_max) * (me.stepy * me.small_inter);
                    }
                    return y;
                }
            )
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.05pt')
            .style("text-anchor", 'end')
            .style("font-family", me.user_font)
            .style("font-size", function (d) {
                    let size = me.medium_font_size * (1 + Math.floor(d.value / 3) * 0.25);
                    return size + 'pt';
                }
            )
            .text(function (d) {
                    if (me.blank) {
                        return "";
                    }
                    return d.value;
                }
            );
        skills.exit().remove();

        if (me.blank) {
            let lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];
            skill_in.append('line')
                .data(lines)
                .attr('x1', function (d) {
                    let x = 0;
                    x = ox + Math.floor(d / me.spe_col_max) * (me.stepx * 4.25) + me.stepx * 0.25;
                    return x;
                })
                .attr('x2', function (d) {
                    let x = 0;
                    x = ox + Math.floor(d / me.spe_col_max) * (me.stepx * 4.25) + me.stepx * 4;
                    return x;
                })
                .attr('y1', function (d) {
                    let y = 0;
                    y = oy_spe + (d % me.spe_col_max) * (me.stepy * me.small_inter) - 1;
                    return y;
                })
                .attr('y2', function (d) {
                    let y = 0;
                    y = oy_spe + (d % me.spe_col_max) * (me.stepy * me.small_inter) - 1;
                    return y;
                })
                .style("fill", function (d) {

                    return me.shadow_fill;


                })
                .style("stroke", function (d) {
                    return me.shadow_fill;

                })
                .style("stroke-dasharray", "4 3")
                .style("stroke-width", '2pt')
                .attr("opacity", 0.3)
            ;

        }


        me.daddy = me.character;

        let rollstable = [
            "Standard Roll: 1D12 + Skill + Attribute /vs/ DV",
            "Margin = Roll - DV",
            "Margin > DV => Critical Success ",
            "Margin < 0 => Failure ",
            "Roll < 0 => Critical Failure ",
            "12 on D12 => Roll += another D12, etc",
            "1 on D12 => Roll -= another D12, etc"
        ]

        let dvtable = [
            "NAME .............. DV ",
            "Very Hard ......... 30 ",
            "Hard .............. 25 ",
            "Challenging ....... 20 ",
            "Moderate .......... 15 ",
            "Easy .............. 10 ",
            "Piece of Cake ..... 5"
        ];
        let accenttable = [
            "[Optimistic Accent Roll]: min(NxD12) + Attribute + Skill (N-1xW) => margin = margin x N",
            "[Pessimistic Accent Roll]: max(NxD12) + Attribute + Skill (N-1xW)  => margin = margin / N",
            "[God Mode Roll]: 12! + D12 + Attribute + Skill (4W)  => margin = margin",
            "[Pancreator Is My Bitch Roll]: GM mid(3D12) + Attribute + Skill (1W)  => margin = margin ",
            "Melee/Fight additional damage = ((margin div 3)+DMG) x D6 + (margin mod 3) (Ex:8=>2D6+2)",
            "XP: Primary/Occult Lvl: Tx5xp; Skill: Txp; Occult Power/Fighting Style: Tx3xp",

        ];

        _.forEach(dvtable, function (v, k) {
            me.drawText(1.5, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
        });
        _.forEach(rollstable, function (v, k) {
            me.drawText(5.0, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
        });
        _.forEach(accenttable, function (v, k) {
            me.drawText(11.5, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
        });

    }

    fillListTgt(basex = 0, basey = 0, datasource = "ba", styles = {}, target) {
        let me = this;
        let ox = basex, oy = basey, lines = 1, offset = 0;
        let w = 0, l = 1;
        _.forEach(styles['lefts'], function (e, i) {
            if (e > w) {
                w = e;
            }
        });
        me.daddy = target.append("g").attr('class', datasource + 's');

        // Labels
        _.forEach(styles['labels'], function (e, i) {
            me.drawText(ox + styles["lefts"][i], oy, me.draw_fill, me.draw_stroke, me.small_font_size, "start", e);
        });
        _.forEach(me.data[datasource], function (e, i) {
            // let o = JSON.parse(e);
            let meta = "";
            let stroke = me.user_stroke,
                fill = me.user_fill,
                font = me.user_font,
                size = me.medium_font_size,
                opac = 1.0, biggest = 0;
            if (!me.blank) {
                l = 0;
                offset = (i + biggest) * me.small_inter;
                oy = basey + me.small_inter + offset;
                biggest = 0;
                _.forEach(styles["properties"], function (y, j) {
                    if (styles["aligns"][j] == "multiline") {
                        let data = undefined;
                        let a = y.split('|');
                        let x = a[0];
                        let z = undefined;
                        if (a.length == 2) {
                            z = a[1];
                        }

                        let property_components = x.split('__');
                        if (property_components.length < 2) {
                            data = e[x]
                        } else {
                            data = e[property_components[0]][property_components[1]]
                        }
                        if (z == undefined) {

                        } else if (z == "bool") {
                            if (data == false) {
                                data = "."
                            } else {
                                data = "x";
                            }
                        } else if (z == "lower") {
                            data = data.toLowerCase();
                        }
                        lines = me.wrap(data, ox + styles["lefts"][j], oy, styles["widths"][j], font) + 1;
                    } else {
                        lines = 0;
                    }
                    if (lines > biggest) {
                        biggest = lines;
                    }
                });
                _.forEach(styles["properties"], function (y, j) {
                    if (styles["aligns"][j] != "multiline") {
                        let data = undefined;
                        let a = y.split('|');
                        let x = a[0];
                        let z = undefined;
                        if (a.length == 2) {
                            z = a[1];
                        }
                        let property_components = x.split('__');
                        if (property_components.length < 2) {
                            data = e[x]
                        } else {
                            data = e[property_components[0]][property_components[1]]
                        }
                        if (z == undefined) {

                        } else if (z == "bool") {
                            if (data == false) {
                                data = "."
                            } else {
                                data = "x";
                            }
                        } else if (z == "lower") {
                            data = data.toLowerCase();
                        }
                        me.drawText(ox + styles["lefts"][j], oy, fill, stroke, size, styles["aligns"][j], data, opac, font);
                    }
                });
            }
        });
        if (me.debug) {
            me.drawRect(basex, basey + 0.25, w + 0.5 + styles["widths"][styles["widths"].length - 1], oy - basey, "transparent", '#A22')
        }
    }

}
