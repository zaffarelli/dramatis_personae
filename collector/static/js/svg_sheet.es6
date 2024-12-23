/* Character Sheet Module, with everything about writing character data for tabletop usage
 * Try to keep all coordinates as steps. Only multiply inside the deepest function.
 */
class Sheet {
    constructor(data, parent, collector) {
        this.parent = parent;
        this.co = collector;
        this.config = data;
        this.disposition = 'portrait';
        this.xunits = 0;
        this.yunits = 0;
        this.report = {
            "lines": 0,
            "maxlines": -1,
            "settings": {}
        }
        console.debug("Character Sheet");
    }

    init() {
        let me = this
        me.debug = me.config.debug
        me.blank = me.config.blank
        me.translation = true
        me.button_ox = 28;
        me.button_oy = 2;
        me.version = "10.2";
        me.white = me.debug ? "#FFF0FF" : "#FFFFFF"
        if (me.disposition == 'portrait') {
            me.xunits = 24;
            me.yunits = 34;
            me.width = parseInt($(me.parent).css("width"), 10) * 0.75;
            me.height = me.width * 1.4;
            me.w = parseInt($(me.parent).css('width'));
            me.h = parseInt($(me.parent).css('height'));
            me.step = me.width / me.xunits;
            
        } else {
            me.xunits = 34;
            me.yunits = 24;
            me.width = parseInt($(me.parent).css("width"), 10) * 0.75;
            me.height = me.width / 1.4;
            me.w = parseInt($(me.parent).css('width'));
            me.h = parseInt($(me.parent).css('height'));
            me.step = me.width / me.xunits;
            
        }

        me.small_font_size = me.step * 0.2
        me.medium_font_size = me.small_font_size * 1.2
        me.big_font_size = me.medium_font_size*1.5
        me.large_font_size = me.big_font_size*1.5
        me.fat_font_size = me.large_font_size*2.75

        me.small_inter = 0.5;

        me.margin = [0, 0, 0, 0];
        me.dot_radius = me.step / 8;
        me.stat_length = 150;
        me.stat_max = 5;
        me.shadow_fill = "#B0B0B0";
        me.shadow_stroke = "#A0A0A0";
        me.jumpgate_stroke = "#B8B8B8";
        me.draw_stroke = '#777';
        me.draw_fill = '#222';
        me.debug_stroke = '#FC4';
        me.debug_fill = '#FC8';
        me.user_stroke = '#A060A0';
        me.user_fill = '#903090';
        me.user_font = 'Long Cang'
        me.mono_font = 'Syne Mono';
        me.title_font = 'Anton';
        me.logo_font = 'Trade Winds'
        me.base_font = 'Voltaire';
//         me.strokedebris = "190 12 125 5 42 3";
//         me.strokedebris_short = "125 5 35 2 3 4 85 9";
        me.strokedebris = me.strokedebris_short = ""
        me.x = d3.scaleLinear().domain([0, me.width]).range([0, me.width]);
        me.y = d3.scaleLinear().domain([0, me.height]).range([0, me.height]);

        me.pre_title = me.config['pre_title'];
        me.scenario = me.config['scenario'];
        me.post_title = me.config['post_title'];
//         if (me.blank) {
//             me.pre_title = "Pancreator Vobiscum Sit";
//         }
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
        let ox = me.button_ox * me.step;
        let oy = me.button_oy * me.step;
        let button = me.ui.append('g')
            .attr('class', 'buttons do_not_print')
            .attr('transform', `translate(${me.w-me.step*3},${me.step*(1+num)})`)
            .on('mouseover', function (d) {
                me.ui.select('#button' + num).style("stroke", "#882");
            })
            .on('mouseout', function (d) {
                me.ui.select('#button' + num).style("stroke", "#111");
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
            .attr('x', 0)
            .attr('y', 0)
            .attr('rx', '3mm')
            .attr('ry', '3mm')
            .attr('width', me.step * 1.6)
            .attr('height', me.step * 0.8)
            .style('fill', '#888')
            .style('stroke', '#111')
            .style('stroke-width', '1mm')
            .attr('opacity', 1.0)
            .style('cursor', 'pointer')
        ;
        button.append('text')
            .attr('x', me.step * 1.6 * 0.5)
            .attr('y', me.step * 0.8 * 0.5)
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
                me.svg.select('#button' + num).style("stroke", "#FC4");
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
            .attr("x", me.step * x)
            .attr("y", me.step * y)
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
                .attr('x1', me.step * x1)
                .attr('x2', me.step * x2)
                .attr('y1', me.step * y1)
                .attr('y2', me.step * y2)
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
                .attr('x', x * me.step)
                .attr('y', y * me.step)
                .attr('rx', round)
                .attr('width', width * me.step)
                .attr('height', height * me.step)
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
            console.log(text)
            let sentences = (""+text).split("; ")
            let lineCnt=0
            let t = me.daddy.append('text')
                .attr('x', me.step * x)
                .attr('y', me.step * y)
                .style('fill', fill)
                .style('stroke', stroke)
                .style('stroke-width', '0.5pt')
                .style("text-anchor", position)
                .style("font-size", size + 'pt')
                .style("font-family", f)
                .text("")
            _.forEach(sentences,(sentence) => {
                console.log(" ---> "+sentence)
                t.append("tspan")
                    .attr('x', me.step * x)
                    .attr('y', me.step * y)
                    .attr('dy', (size*lineCnt++) + "pt")
                    .text(sentence)
            })

        }
    }

    defaultWriteText(){
        let me = this
        let def = {
            "x" : 1,
            "y" : 1,
            "dx" : 1,
            "dy" : 1,
            "fill" : '#101060',
            "stroke" : '#8080F0',
            "stroke-width" : "0.5pt",
            "size" : 0.2,
            "position" : 'start',
            "opacity": 1,
            "font" : me.base_font,
            "width" : 0,
            "text" : 'n/a'
        }
        return def
    }

    writeText(opt = {}) {
        let me = this
        let settings = me.defaultWriteText()
        _.forEach(opt,(v,k)=>{
            if (settings.hasOwnProperty(k)){
                settings[k] = v
            }else{
                console.warn("Don't know what to do with "+k+".")
            }
        })
        if (!me.daddy) {
            console.error('Daddy is undefined for writeText!')
        } else {
            let sentences = (""+settings["text"]).split("; ")
            let lineCnt=0
            let t = me.daddy.append('text')
                .attr('x', me.step * settings["x"])
                .attr('y', me.step * settings["y"])
                .style('fill', settings["fill"])
                 .style('stroke', settings["stroke"])
                .style('stroke-width', settings["stroke-width"])
                .style("text-anchor", settings["position"])
                .style("font-size", me.step*settings["size"] + 'pt')
                .style("font-family", settings["font"])
                .text("")
            let breaknext = false
            _.forEach(sentences,(sentence) => {
                let realword = sentence
                if (realword == "false"){
                    realword = "/!\\"
                }else if (realword == "true"){
                    realword = ""
                }
                if (settings.width==0){
                    let tspan = t.append("tspan")
                        .attr('x', me.step * settings["x"])
                        .attr('y', me.step * settings["y"])
                        .attr('dy', (me.step*settings["size"]*lineCnt++) + "pt")
                        .text(realword)
                }else{
                    let words = realword.split(" ")
                    _.forEach(words,(word) => {
                        let tspan = t.append("tspan")
                            .attr('x', me.step * settings["x"])
                            .attr('y', me.step * settings["y"])
                            .attr('dy', (me.step*settings["size"]*lineCnt++) + "pt")
                            .text(word)
                        /* @todo */
//                         if ((tspan.node().getComputedTextLength() > settings.width * me.step) ) {
//
//                         }else{
//
//                         }
                    })


                }
            })
            me.report["lines"] = lineCnt
            if (me.report.lines > me.report.maxlines){
                me.report.maxlines = me.report.lines
            }
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
                .attr('r', me.step * radius)
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
        me.jumpgate = me.mid.append('g').attr('opacity', 0.65);
        me.daddy = me.jumpgate;
        me.drawCircle(2.25, "", 0, 0, 20);
        me.drawCircle(0.9, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(1.0, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(2.0, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(2.6, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(4.0, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(4.2, "100 20 35 10 50 350 60 125", 0, 0);
        me.drawCircle(8.3, "100 20 35 10 50 350 60 125", 0, 0);
        let s = me.step;
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
        //me.daddy = dad;
    }

    wrap(par, bx, by, width, font = 'default') {
        let me = this;
        let xo = bx,
            yo = by;
        if (font == 'default') {
            font = me.user_font;
        }
        let text = me.daddy.append('text')
            .attr('x', xo * me.step)
            .attr('y', yo * me.step)
            .attr('dx', 0)
            .attr('dy', 0)
            .text(par)
            .style("text-anchor", 'left')
            .style("font-family", font)
            .style("font-size", me.small_font_size + 'pt')
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.5pt');
        //let words = text.text().split(/\s+/).reverse(),
        let words = text.text().split(' ').reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = me.medium_font_size,
            x = text.attr("x"),
            y = text.attr("y"),
            tspan = text.text(null).append("tspan")
                .attr("x", x)
                .attr("y", y);
        while (word = words.pop()) {
            let nl = false
            console.log("["+word+"]")
            if (word=="§"){
                nl = true
                word = ""
            }else{
                line.push(word);
                tspan.text(line.join(" "));
            }
            if ((tspan.node().getComputedTextLength() > width * me.step) || (nl==true)) {
                line.pop();
                if (nl == false){
                    tspan.text(line.join(" "));
                }
                line = [word];
                tspan = text.append("tspan")
                    .attr("x", x)
                    .attr("y", y)
                    .attr("dy", ++lineNumber * lineHeight +'pt')
                    .style("font-size", me.medium_font_size + 'pt')
                    .style("stroke-width", '0.5pt')
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

        me.back = me.svg.append("g")
            .attr("class", "page")
            .attr("transform", "translate(" + 0 * me.step + "," + 0 * me.step + ")")

        me.mid = me.svg.append("g")
            .attr("class", "page")
            .attr("transform", "translate(" + 0 * me.step + "," + 0 * me.step + ")")

        me.front = me.svg.append("g")
            .attr("class", "page")
            .attr("transform", "translate(" + 0 * me.step + "," + 0 * me.step + ")")

        me.ui = me.vis.append('g')


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
            .attr('width', me.step*me.xunits)
            .attr('height', me.step*me.yunits)
            .style('fill', me.white)
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
                    return d * me.step
                })
                .attr('y1', 0)
                .attr('x2', function (d) {
                    return d * me.step
                })
                .attr('y2', me.yunits * me.step)
                .style('fill', 'transparent')
                .style('stroke', '#888')
                .style('stroke-width', '0.5pt');
            let horizontals = me.back.append('g')
                .attr('class', 'horizontals')
                .selectAll("g")
                .data(d3.range(0, me.yunits, 1));
            horizontals.enter()
                .append('line')
                .attr('x1', 0)
                .attr('x2', me.xunits * me.step)
                .attr('y1', function (d) {
                    return d * me.step
                })
                .attr('y2', function (d) {
                    return d * me.step
                })
                .style('fill', 'transparent')
                .style('stroke', '#888')
                .style('stroke-width', '0.5pt');
        }

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
            me.drawText(ox + 1, oy + 1.37, me.user_fill, me.user_stroke, me.big_font_size, "middle", me.data["SA_WYR"], 1.0, me.user_font);
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
        styles["labels"] = ["Type", "History", "Valid", "Pts","Details"]
        styles["properties"] = ["category_text", "reference","valid", "value","description"]
        styles["aligns"] = ["start", "start", "start","start","start"]
        styles["widths"] = [0, 5, 0,0,16]
        styles["lefts"] = [0, 1, 1.75,4.5,5.5]
        me.daddy = me.front
        me.standardBlock({"x":basex-0.25,"y":basey-0.35,"width":21.5,"height":9.5,"title":"Life Path Overview"})
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
                .attr("x", basex * me.step)
                .attr("y", basey * me.step)
                .attr("width", 3.5 * me.step)
                .attr("height", 5 * me.step)
                .attr("class", "do_not_print")
            ;
        }
    }


    fillList(basex = 0, basey = 0, datasource = "ba", styles = {}) {
        let me = this;
        let ox = basex, oy = basey, lines = 1, offset = 0;
        let w = 0, l = 1;
        let stroke = me.user_stroke,
            fill = me.user_fill,
            font = me.user_font,
            size = 0.25
        _.forEach(styles['lefts'], function (e, i) {
            if (e > w) {
                w = e;
            }
        });
        me.daddy = me.front.append("g").attr('class', "list_"+datasource);

        // Labels
        _.forEach(styles['labels'], function (e, i) {
            me.writeText({"x":ox + styles["lefts"][i], "y":oy, "fill":me.draw_fill, "stroke":me.draw_stroke, "size":me.small_font_size/me.step, "text":e});
        });
        //oy += size
        _.forEach(me.data[datasource], function (e, i) {
            // let o = JSON.parse(e);
            let meta = "";
            if (!me.blank) {
                l = 0;
                oy += (me.report.maxlines)*size*1.5
                me.report.maxlines = 0
                //oy = basey + small_inter + offset;
//                 biggest = 0;
//                 _.forEach(styles["properties"], function (y, j) {
//                     if (styles["aligns"][j] == "multiline") {
//                         let data = undefined;
//                         let a = y.split('|');
//                         let x = a[0];
//                         let z = undefined;
//                         if (a.length == 2) {
//                             z = a[1];
//                         }
//
//                         let property_components = x.split('__');
//                         if (property_components.length < 2) {
//                             data = e[x]
//                         } else {
//                             data = e[property_components[0]][property_components[1]]
//                         }
//                         if (z == undefined) {
//
//                         } else if (z == "bool") {
//                             if (data == false) {
//                                 data = "."
//                             } else {
//                                 data = "x";
//                             }
//                         } else if (z == "lower") {
//                             data = data.toLowerCase();
//                         }
//                         lines = me.wrap(data, ox + styles["lefts"][j], oy, styles["widths"][j], font) + 1;
//                     } else {
//                         lines = 0;
//                     }
//                     if (lines > biggest) {
//                         biggest = lines;
//                     }
//                 });
                _.forEach(styles["properties"], function (y, j) {
//                     if (styles["aligns"][j] != "multiline") {
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
                        me.writeText({"x":ox + styles["lefts"][j], "y":oy, "stroke":stroke,"fill": stroke, "size":size, "position":styles["aligns"][j], "text":data, "font":font});

//                     }
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
        me.fillSanity(8.5, 23);
        me.fillGlamour(8.5, 26.5);
        me.fillKarma(8.5, 31);


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
            me.drawText(ox + 1, oy + 1.37, me.user_fill, me.user_stroke, me.big_font_size, "middle", me.data["SA_HUM"], 1.0, me.user_font);
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
            me.drawText(ox + 1, oy + 1.37, me.user_fill, me.user_stroke, me.big_font_size, "middle", me.data["SA_PAS"], 1.0, me.user_font);

        }
        let lines = [0, 0.5, 1.0, 1.5];
        _.forEach(lines, function (e, i) {
            me.drawLine(ox + 0.5, ox + 4.5, oy + 2.5 + e, oy + 2.5 + e, me.shadow_fill, me.shadow_stroke, 0.5, "");
        })
    }


    baseStat(name, value, ox, oy, pos = 0, fat = false) {
        let me = this
        let boxWidth = (pos==0 ? 6 : 2.9)
        let boxHeight = (fat ? 1.75 : 0.8)
        let item = me.daddy.append('g')
            .attr('class', 'fulldesc')
            .attr('transform', (d) => {
                let x = ox + (pos==2 ? boxWidth+0.2 : 0)
                let y = oy
                return `translate(${x*me.step},${y*me.step})`
                })
        if (me.debug) {
            item.append('rect')
                .attr('width', boxWidth*me.step)
                .attr('height', boxHeight*me.step)
                .style('fill', 'lime')
                .style('stroke', 'white')
                .style('stroke-width', '1pt')
                .attr('opacity', 0.5)
        }

        item.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('rx', 8)
            .attr('width', boxWidth*me.step)
            .attr('height', me.step * boxHeight)
            .style('fill', me.white)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '2pt')
            //.style('stroke-dasharray', me.strokedebris_short)
        ;
        item.append('text')
            .attr('x', 0)
            .attr('y', 0)
            .attr("dx", 5+"pt")
            .attr("dy", me.step * 0.65)
            .style("text-anchor", 'start')
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size + 'pt')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.5pt')
            .text(function () {
                return name.charAt(0).toUpperCase() + name.slice(1);
            });
        item.append('text')
            .attr('x', (boxWidth / 2)*me.step)
            .attr('y', (boxHeight / 2)*me.step)
            .attr("dy", fat ? 0 : me.big_font_size*0+"pt")
            .style("text-anchor", (fat ? "middle" :'start'))
            .style("font-family", function (d) {
                return me.user_font;
            })
            .style("font-size", function (d) {
                let res = me.medium_font_size + 'pt'
                if (fat) {
                    res = me.big_font_size*1.2 + 'pt';
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

    drawAttribute(name, desc, value, ox, oy, pos = 1, scale = 10, translation="") {
        let me = this
        let attwidth = 2
        let item = me.daddy.append('g')
            .attr('class', 'attribute')
            .attr('transform',(d) => {
                let x = 0
                let y = oy
                if (pos == 1) {
                    x = ox
                } else if (pos == 2) {
                    x = ox + attwidth
                }
                return `translate(${x*me.step},${y*me.step})`
            })
        if (me.debug) {
            item.append('rect')
                .attr('width', me.step * attwidth)
                .attr('height', me.step * 1)
                .style('fill', 'none')
                .style('stroke', 'cyan')
                .style('stroke-width', '2pt')
                .style('stroke-dasharray', '3 2')
                .attr('opacity',0.75)
        }
        item.append('circle')
            .attr('cx', pos == 2 ? me.step*0.5 : me.step*1.5)
            .attr('cy', me.step * 0.5)
            .attr('r', 0.4 * me.step)
            .style('fill', 'white')
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
            .attr('x', 1 * me.step)
            .attr("y", me.step * 0.4)
            .style("text-anchor", pos == 2 ? "start" : "end")
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size + 'pt')
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.75pt')
            .text(function () {
                return name.charAt(0).toUpperCase() + name.slice(1);
            });
        item.append('text')
            .attr('x', 1 * me.step)
            .attr("y", me.step * 0.4)
            .attr("dy", me.step * 0.2)
            .style("text-anchor", pos == 2 ? "start" : "end")
            .style("font-family", me.base_font)
            .style("font-size", me.small_font_size + 'px')
            .style("fill", me.draw_fill)
            .style("stroke", me.shadow_stroke)
            .style("stroke-width", '0.5pt')
            .text(function (d) {
                return desc;
            });

        if (me.translation){
            item.append('text')
                .attr('x', 1 * me.step)
                .attr("y", me.step * 0.4)
                .attr("dy", me.step * 0.4)
                .style("text-anchor", pos == 2 ? "start" : "end")
                .style("font-family", me.base_font)
                .style("font-size", me.small_font_size + 'px')
                .style("fill", me.draw_fill)
                .style("stroke", me.shadow_stroke)
                .style("stroke-width", '0.5pt')
                .text(function (d) {
                    return translation;
                })
        }


        item.append('text')
            .attr('x', pos==2 ? 0.5*me.step : 1.5*me.step)
            .attr("y", 0.5*me.step)
            .attr("dy", me.big_font_size*.3+'pt')
            .style("text-anchor", 'middle')
            .style("font-family", me.user_font)
            // .style("font-size", (me.medium_font_size * 1.4) + 'px')
            .style("font-size", function () {
                let s = me.big_font_size;
//                 if (scale === 10) {
//                     s = me.medium_font_size * (1 + Math.floor(value / 2) * 0.08);
//                 }
                return s + 'pt';
            })
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.5pt')
            .text(function () {
                if (me.blank) {
                    return "";
                }
                return value;
            });
    }

    fillAttributes(ot) {
        let me = this;
        let bx = 1.25;
        let oy = ot+7;
        me.daddy = me.character
        me.standardBlock({"x":bx,"y":oy,"width":4,"height":6.5,"title":"Primary Attributes"})
        me.drawAttribute("STR", "strength", me.data["PA_STR"], bx, oy, 1,10,"force")
        me.drawAttribute("CON", "constitution", me.data["PA_CON"], bx, oy, 2,10,"constitution")
        me.drawAttribute("BOD", "body", me.data["PA_BOD"], bx, oy + 1 ,  1,10,"carrure")
        me.drawAttribute("MOV", "movement", me.data["PA_MOV"], bx, oy + 1 ,  2,10,"mouvement")

        me.drawAttribute("INT", "intellect", me.data["PA_INT"], bx, oy + 2 ,  1,10,"intellect")
        me.drawAttribute("WIL", "willpower", me.data["PA_WIL"], bx, oy + 2 ,  2,10,"volonté")
        me.drawAttribute("TEM", "temper", me.data["PA_TEM"], bx, oy + 3 ,  1,10,"caractère")
        me.drawAttribute("PRE", "presence", me.data["PA_PRE"], bx, oy + 3 ,  2,10,"présence")

        me.drawAttribute("TEC", "tech", me.data["PA_TEC"], bx, oy + 4 ,  1,10,"tech")
        me.drawAttribute("DEX", "dexterity", me.data["PA_DEX"], bx, oy + 4 , 2,10, "dextérité")
        me.drawAttribute("AGI", "agility", me.data["PA_AGI"], bx, oy + 5 ,  1, 10,"agilité")
        me.drawAttribute("AWA", "awareness", me.data["PA_AWA"], bx, oy + 5 ,  2,10, "vigilance")

        bx = 5.5
        me.standardBlock({"x":bx,"y":oy,"width":4,"height":6.5,"title":"Secondary Attributes"})
        me.drawAttribute("REC", "STR+CON", me.data["SA_REC"], bx, oy,  1, 20)
        me.drawAttribute("STA", "BOD/2-1", me.data["SA_STA"], bx, oy,  2, 5)
        me.drawAttribute("END", "(BOD+CON)x5", me.data["SA_END"], bx, oy + 1 ,  1, 100)
        me.drawAttribute("STU", "BOD+CON", me.data["SA_STU"], bx, oy + 1 ,  2, 20)

        me.drawAttribute("RES", "WIL+PRE", me.data["SA_RES"], bx, oy + 2 ,  1, 20)
        me.drawAttribute("DMG", "STR/2-2", me.data["SA_DMG"], bx, oy + 2 ,  2, 5)
        me.drawAttribute("TOL", "TEM+WIL", me.data["SA_TOL"], bx, oy + 3 ,  1, 20)
        me.drawAttribute("HUM", "(TEM+WIL)x5", me.data["SA_HUM"], bx, oy + 3 ,  2, 100)

        me.drawAttribute("PAS", "TEM+AWA", me.data["SA_PAS"], bx, oy + 4 ,  1, 20)
        me.drawAttribute("WYR", "INT+DEX", me.data["SA_WYR"], bx, oy + 4 ,  2, 20)
        me.drawAttribute("SPD", "MOV/2", me.data["SA_SPD"], bx, oy + 5 ,  1, 100)
        me.drawAttribute("RUN", "MOVx2", me.data["SA_RUN"], bx, oy + 5 ,  2, 20)
    }

    fillBasics(oy) {
        let me = this;
        let bx = 16.75 ;
        let basex = 12;
        let basey = 9;
        me.baseStat("Player", me.data["player"], bx, oy , 0)
        me.baseStat("Caste", me.data["caste"], bx, oy + 1, )
        me.baseStat("Species", me.data["race"], bx, oy + 2, )
        me.baseStat("Rank", me.data["rank"], bx, oy + 3, )
        me.baseStat("Gender", me.data["gender"], bx, oy +  4,  1)
        me.baseStat("Age", me.data["age"], bx, oy +  4, 2)
        me.baseStat("Height (cm)", me.data["height"], bx, oy + 5,  1)
        me.baseStat("Weight (kg)", me.data["weight"], bx, oy + 5,  2)
        bx = 1.25 ;
        me.baseStat("", me.data["full_name"], bx, oy  , 0, true);
        me.baseStat("Alliance", me.data["alliance"], bx, oy + 2);
        bx = 9.25 ;

        bx = 1.25
        me.standardBlock({"x":bx,"y":4.5,"width":6,"height":6.5,"title":"Life Path"})
        let ty = 5
        bx += 0.25
        let yof1 = 0.45
//        let yof2 = 0.3
        let dots = ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
        let pts_dots = ""
        let bxw = 5.5
        let bxg = 0.25
        let f = me.user_font
        me.drawText(bx, ty, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Birthright")
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx, ty, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Upbringing")
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx, ty, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Apprenticeship")
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx, ty, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Early Career")
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx, ty, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Tours of Duty")
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )
        ty += yof1
        me.drawText(bx, ty, me.draw_fill, me.shadow_stroke, me.small_font_size, "start", "Worldly Benefits")
        me.drawText(bx+bxw, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "end", dots,1.0,f )
        me.drawText(bx+bxw+bxg, ty, me.shadow_fill, me.shadow_stroke, me.small_font_size, "start", pts_dots,1.0,f )

        if (!me.blank){
            let up=0
            let tod=0
            _.forEach(me.data["tods"],(v,k) => {
                let label = `${v['valid'] ? "":"* "}${v['reference']}`
                switch (v.category){
                    case "0":
                        ty = 5
                        me.drawText(bx+bxw, ty, me.user_fill, me.user_stroke, me.medium_font_size, "end", label,1.0,f )
                        break
                    case "10":
                        ty = 5+yof1
                        me.drawText(bx+bxw, ty+up*yof1, me.user_fill, me.user_stroke, me.medium_font_size, "end", label,1.0,f )
                        up += 1
                        break
                    case "20":
                        ty = 5+yof1*3
                        me.drawText(bx+bxw, ty, me.user_fill, me.user_stroke, me.medium_font_size, "end", label,1.0,f )
                        break
                    case "30":
                        ty = 5+yof1*4
                        me.drawText(bx+bxw, ty, me.user_fill, me.user_stroke, me.medium_font_size, "end", label,1.0,f )
                        break
                    case "40":
                        ty = 5+yof1*5
                        me.drawText(bx+bxw, ty+tod*yof1, me.user_fill, me.user_stroke, me.medium_font_size, "end", label,1.0,f )
                        tod += 1
                        break
                    case "50":
                        ty = 5+yof1*11
                        me.drawText(bx+bxw, ty, me.user_fill, me.user_stroke, me.medium_font_size, "end", label,1.0,f )
                        break
                }
            })
        }
        me.standardBlock({"x":7.5,"y":4.50,"width":9,"height":6.5,"title":"Story Details"})
//         if (me.blank == false) {
//             let dad = me.daddy
//             let tods_description = []
//             _.forEach(me.data['tods'], (v,k) => {
//                 let new_desc = v.description.replaceAll("; "," § - ")
//                 tods_description.push("▸ "+v.reference.toUpperCase()+" ("+v.value+") § - "+new_desc)
//                 })
//             let all_tods = tods_description.join(" § ")
//             console.log(all_tods)
//             me.daddy = me.front
//             me.wrap(all_tods, 7.75, 5, 11, me.user_font);
//             me.daddy = dad
//         }

        basex = 10
        basey = 9
        if (0){
            me.standardBlock({"x":9.75,"y":9.25,"width":6.75,"height":1.75,"title":"Experience"})
            me.drawCircle(0.4, "5 2", (basex + 1) * me.step, (basey + 1.0) * me.step, 2);
            me.drawText(basex + 1.9, basey+1 , me.draw_fill, me.shadow_stroke, me.small_font_size, "middle", "Earned");
            me.drawCircle(0.4, "5 2", (basex + 3) * me.step, (basey + 1.0) * me.step, 2);
            me.drawText(basex + 3.9, basey + 1, me.draw_fill, me.shadow_stroke, me.small_font_size, "middle", "Spent");
            me.drawCircle(0.4, "5 2", (basex + 5) * me.step, (basey + 1.0) * me.step, 2);
            me.drawText(basex + 5.9, basey + 1, me.draw_fill, me.shadow_stroke, me.small_font_size, "middle", "Pool");
            if (!me.blank){
                me.drawText(basex + 1, basey+1+0.1 , me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["xp_earned"], 1, me.user_font);
                me.drawText(basex + 3, basey + 1+0.1, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["xp_spent"], 1, me.user_font);
                me.drawText(basex + 5, basey + 1+0.1, me.user_fill, me.user_stroke, me.medium_font_size, "middle", me.data["xp_pool"], 1, me.user_font);
            }
        }

        me.standardBlock({"x":16.75,"y":7.50,"width":6,"height":3.5,"title":"Distinguishing features"})
        if (me.blank == false) {
            me.wrap(me.data['entrance'], 17, 8, 6, me.user_font);
        }
    }

    fillSkills(basey) {
        let me = this;
        me.spe_col_max = 3;
        let oy = basey;
        me.column_amount = 10;
        let ox = 10.25;
        let boxWidth = 4.15
        let boxHeight = 0.6
        me.standardBlock({"x":10,"y":basey,"width":12.75,"height":6.5,"title":"Skills"})
        let skills = me.character.append('g').selectAll('g')
            .data(me.data["skills_list"]);
        let skill_in = skills.enter()
            .append('g')
            .attr('class','fics_skill')
            .attr('transform',(d) => {
                let x = (ox + Math.floor(d.idx1 / me.column_amount) * (boxWidth))
                let y = (oy + (d.idx1 % me.column_amount) * boxHeight)
                return `translate(${x*me.step},${y*me.step})`
            })

        if (me.debug) {
            skill_in.append('rect')
                .attr('width', boxWidth*me.step)
                .attr('height', boxHeight*me.step)
                .style('fill', 'none')
                .style('stroke', 'red')
                .style('stroke-width', '1pt')
                .style('stroke-dasharray', '5 4')
                .attr('opacity', 0.75)
        }


        skill_in.append('line')
            .attr('x1', 0)
            .attr('x2', boxWidth*me.step*9/10)
            .attr('y1', boxHeight*me.step*4/5)
            .attr('y2', boxHeight*me.step*4/5)
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
            .attr('x', 0)
            .attr('y', boxHeight * me.step*2/3)
            .style("fill", me.draw_fill)
            .style("stroke", me.draw_stroke)
            .style("stroke-width", '0.5pt')
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
        skill_in.append('rect')
            .attr('x', (boxWidth*5/6)*me.step)
            .attr('y', 1*me.step/12)
            .attr('width', 5*me.step/12)
            .attr('height', 5*me.step/12)
            .style('fill', me.white)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '1pt')
            .attr('opacity', 1)

        skill_in.append('text')
            .attr('x', boxWidth * me.step*9/10)
            .attr('y', boxHeight * me.step *4/5)
            .attr('dy', me.big_font_size*0+"pt")
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.5pt')
            .style("text-anchor", 'end')
            .style("font-family", me.user_font)
            .style("font-size", function (d) {
                    let size = me.big_font_size;
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
                .attr('x1', 0)
                .attr('x2', boxWidth*me.step)
                .attr('y1', boxHeight*me.step)
                .attr('y2', boxHeight*me.step)
                .style("fill", me.shadow_fill)
                .style("stroke", me.shadow_stroke)
                .style("stroke-dasharray", "4 3")
                .style("stroke-width", '2pt')
                .attr("opacity", 0.3)
            ;

        }


//         me.daddy = me.character;
//
//         let rollstable = [
//             "Standard Roll: 1D12 + Skill + Attribute /vs/ DV",
//             "Margin = Roll - DV",
//             "Margin > DV => Critical Success ",
//             "Margin < 0 => Failure ",
//             "Roll < 0 => Critical Failure ",
//             "12 on D12 => Roll += another D12, etc",
//             "1 on D12 => Roll -= another D12, etc"
//         ]
//
//         let dvtable = [
//             "NAME .............. DV ",
//             "Very Hard ......... 30 ",
//             "Hard .............. 25 ",
//             "Challenging ....... 20 ",
//             "Moderate .......... 15 ",
//             "Easy .............. 10 ",
//             "Piece of Cake ..... 5"
//         ];
//         let accenttable = [
//             "[Optimistic Accent Roll]: min(NxD12) + Attribute + Skill (N-1xW) => margin = margin x N",
//             "[Pessimistic Accent Roll]: max(NxD12) + Attribute + Skill (N-1xW)  => margin = margin / N",
//             "[God Mode Roll]: 12! + D12 + Attribute + Skill (4W)  => margin = margin",
//             "[Pancreator Is My Bitch Roll]: GM mid(3D12) + Attribute + Skill (1W)  => margin = margin ",
//             "Melee/Fight additional damage = ((margin div 3)+DMG) x D6 + (margin mod 3) (Ex:8=>2D6+2)",
//             "XP: Primary/Occult Lvl: Tx5xp; Skill: Txp; Occult Power/Fighting Style: Tx3xp",
//
//         ];
//
//         _.forEach(dvtable, function (v, k) {
//             me.drawText(1.5, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
//         });
//         _.forEach(rollstable, function (v, k) {
//             me.drawText(5.0, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
//         });
//         _.forEach(accenttable, function (v, k) {
//             me.drawText(11.5, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
//         });

    }

    fillDegrees(basey) {
        let me = this;
        me.spe_col_max = 3;
        let oy = basey;
        me.column_amount = 10;
        let ox = 1.5;
        let boxWidth = 5
        let boxHeight = 0.5

        if (me.debug)
            console.log(me.data.degrees_list)


        me.standardBlock({"x":ox-0.25,"y":basey-0.25,"width":21.5,"height":4.5,"title":"Degrees"})
        let degrees = me.front.append('g').selectAll('g')
            .data(me.data["degrees_list"]);
        let degree_in = degrees.enter()
            .append('g')
            .attr('class','fics_degree')
            .attr('transform',(d) => {
                let x = (ox + Math.floor(d.idx1 / me.column_amount) * (boxWidth))
                let y = (oy + (d.idx1 % me.column_amount) * boxHeight)
                return `translate(${x*me.step},${y*me.step})`
            })

        if (me.debug) {
            degree_in.append('rect')
                .attr('width', boxWidth*me.step)
                .attr('height', boxHeight*me.step)
                .style('fill', 'none')
                .style('stroke', 'lime')
                .style('stroke-width', '1pt')
                .style('stroke-dasharray', '3 2')
                .attr('opacity', 0.75)
            _.forEach(new Array(11),(v,k) => {
                degree_in.append('line')
                    .attr("x1",boxWidth*me.step*(k/12))
                    .attr("x2",boxWidth*me.step*(k/12))
                    .attr("y1",0*me.step)
                    .attr("y2",boxHeight*me.step)
                    .style('stroke', 'lime')
                    .style('stroke-width', '1pt')
                    .style('stroke-dasharray', '1 2')
                    .attr('opacity', 0.75)
            })
        }


        degree_in.append('line')
            .attr('x1', boxWidth*me.step*1/24)
            .attr('x2', boxWidth*me.step*23/24)
            .attr('y1', boxHeight*me.step*4/5)
            .attr('y2', boxHeight*me.step*4/5)
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
        degree_in.append('text')
            .attr('x', (boxWidth*1/24)*me.step)
            .attr('y', boxHeight * me.step*12/24)
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.5pt')
            .style("text-anchor", 'left')
            .style("font-family", me.user_font)
            .style("font-size", function (d) {
                if (d['is_speciality']) {
                    return me.small_font_size + 'pt';
                } else {
                    return me.small_font_size + 'pt';
                }
            })
            .text((d) => d.group)
            .append('tspan')
                .attr('x', (boxWidth*1/24)*me.step)
                .attr('dy',me.small_font_size*0.75+"pt")
                .text((d) => d.degree)

        degree_in.append('rect')
            .attr('x', (boxWidth*19/24)*me.step)
            .attr('y', 1*me.step/12)
            .attr('width', 10*me.step/12)
            .attr('height', 5*me.step/12)
            .style('fill', me.white)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '1pt')

        degree_in.append('text')
            .attr('x', boxWidth * me.step*21/24)
            .attr('y', boxHeight * me.step *5/5)
            .attr('dy', me.big_font_size*0+"pt")
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.5pt')
            .style("text-anchor", 'middle')
            .style("font-family", me.user_font)
            .style("font-size", function (d) {
                    let size = me.big_font_size;
                    return size + 'pt';
                }
            )
            .text(function (d) {
                    if (me.blank) {
                        return "";
                    }
                    return d.value;
                })

        degrees.exit().remove();

        if (me.blank) {
            let lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];
            degree_in.append('line')
                .data(lines)
                .attr('x1', 0)
                .attr('x2', boxWidth*me.step)
                .attr('y1', boxHeight*me.step)
                .attr('y2', boxHeight*me.step)
                .style("fill", me.shadow_fill)
                .style("stroke", me.shadow_stroke)
                .style("stroke-dasharray", "4 3")
                .style("stroke-width", '2pt')
                .attr("opacity", 0.3)
            ;

        }


//         me.daddy = me.character;
//
//         let rollstable = [
//             "Standard Roll: 1D12 + Skill + Attribute /vs/ DV",
//             "Margin = Roll - DV",
//             "Margin > DV => Critical Success ",
//             "Margin < 0 => Failure ",
//             "Roll < 0 => Critical Failure ",
//             "12 on D12 => Roll += another D12, etc",
//             "1 on D12 => Roll -= another D12, etc"
//         ]
//
//         let dvtable = [
//             "NAME .............. DV ",
//             "Very Hard ......... 30 ",
//             "Hard .............. 25 ",
//             "Challenging ....... 20 ",
//             "Moderate .......... 15 ",
//             "Easy .............. 10 ",
//             "Piece of Cake ..... 5"
//         ];
//         let accenttable = [
//             "[Optimistic Accent Roll]: min(NxD12) + Attribute + Skill (N-1xW) => margin = margin x N",
//             "[Pessimistic Accent Roll]: max(NxD12) + Attribute + Skill (N-1xW)  => margin = margin / N",
//             "[God Mode Roll]: 12! + D12 + Attribute + Skill (4W)  => margin = margin",
//             "[Pancreator Is My Bitch Roll]: GM mid(3D12) + Attribute + Skill (1W)  => margin = margin ",
//             "Melee/Fight additional damage = ((margin div 3)+DMG) x D6 + (margin mod 3) (Ex:8=>2D6+2)",
//             "XP: Primary/Occult Lvl: Tx5xp; Skill: Txp; Occult Power/Fighting Style: Tx3xp",
//
//         ];
//
//         _.forEach(dvtable, function (v, k) {
//             me.drawText(1.5, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
//         });
//         _.forEach(rollstable, function (v, k) {
//             me.drawText(5.0, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
//         });
//         _.forEach(accenttable, function (v, k) {
//             me.drawText(11.5, 22.35 + 0.35 * k, me.draw_fill, me.shadow_stroke, me.small_font_size - 4, "start", v, 1.0, me.mono_font);
//         });

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

    standardBlock(params={}){
        let me = this
        let layer = me.daddy
        layer.append("rect")
            .attr("class","standardBlock")
            .attr("x",params.x*me.step)
            .attr("y",params.y*me.step)
            .attr("width",params.width*me.step)
            .attr("height",params.height*me.step)
            .attr("rx","10pt")
            .attr("ry","10pt")
            .style("fill",me.white)
            .style("stroke",me.draw_stroke)
            .style("stroke-width","2pt")
        if (params.hasOwnProperty("title")){
            layer.append("text")
                .attr("x",(params.x+params.width/2)*me.step)
                .attr("y",(params.y+params.height)*me.step)
                .style("fill",me.draw_fill)
                .style("stroke",me.shadow_stroke)
                .style("stroke-width","0.5pt")
                .style("text-anchor","middle")
                .style("font-family",me.base_font)
                .style("font-size",me.medium_font_size+'pt')
                .attr("dy",-me.large_font_size/4)
                .text(params.title)
        }
    }

    drawDebris(){
        let me = this
        me.debris = me.mid.append("g")
        me.debris.append('path')
            .attr("d",me.scaledPath("M 0,1 L 24,20 0,12 24,14 0,3 7,0 15,34 0,18 24,32 0,31 9,0 5,34 17,0 19,34 22,0 11,34 0,15 24,16 0,7 24,3"))
            .style("fill","none")
            .style("stroke",me.white)
            .style("stroke-width","9pt")
    }

}

