class EpicDeck {
    constructor(data, parent) {
        this.parent = parent;
        this.data = data;
        this.init();
    }

    init() {
        let me = this;
        me.debug = true;
        me.blank = false;
        me.source = undefined;
        me.version = "1.0.0";
        me.width = parseInt($(me.parent).css("width"), 10) * 0.75;
        me.height = me.width * 1.4;
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        me.stepx = me.width / 24;
        me.stepy = me.height / 36;
        me.small_font_size = 0.25 * me.stepy;
        me.medium_font_size = 0.35 * me.stepy;
        me.big_font_size = 0.5 * me.stepy;
        me.large_font_size = 0.65 * me.stepy;
        me.page = 0;
        me.small_inter = 0.5;
        me.fat_font_size = 8 * me.stepy / 5;
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
        me.user_stroke = '#693';
        me.user_fill = '#231';
        me.user_font = 'Estonia';
        me.mono_font = 'Syne Mono';
        me.title_font = 'Pompiere';
        me.logo_font = 'Trade Winds';
        me.base_font = 'Voltaire';
        me.strokedebris = "190 12 125 5 42 3";
        me.strokedebris_short = "125 5 35 2 3 4 85 9";
        me.x = d3.scaleLinear().domain([0, me.width]).range([0, me.width]);
        me.y = d3.scaleLinear().domain([0, me.height]).range([0, me.height]);
        me.basex = 2;
        me.basey = 2;
        me.row_max = 18;
        me.delta = 0.15;
        me.cardw = 4;
        me.cardh = 6;
        me.initial = true;
        me.group_colors = ["transparent", "#a22", "#284", "#812", "#435", "#69a", "#aa2", "#a3a", "#8c6", "#6cc"]
        me.groupdefs = []
        _.forEach(me.group_colors, function (e, i) {
            me.groupdefs.push({'num': i, 'stroke': e, 'ox': 100000, 'oy': 100000, 'width': 0, 'height': 0});
        })
        me.links = []
    }

    addButton(num, txt) {
        let me = this;
        let ox = -2 * me.stepy;
        let oy = 0.5 * me.stepy;
        let button = me.back.append('g')
            .attr('class', 'buttons do_not_print')
            .on('mouseover', function (d) {
                me.svg.select('#button' + num).style("fill", "#fcc");
            })
            .on('mouseout', function (d) {
                me.svg.select('#button' + num).style("fill", "#ccc");
            })
            .on('click', function (d) {
                if (num == 0) {
                    me.save();
                } else if (num == 1) {
                    me.load();
                } else if (num == 2) {
                    me.reset();
                } else if (num == 3) {
                    $("#d3area").css("display", "none");
                }
            })
        ;
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
        ;
    }

    drawButtons() {
        let me = this;
        me.addButton(0, 'Save');
        me.addButton(1, 'Load');
        me.addButton(2, 'Reset');
    }

    save() {
        let me = this;
        $.ajax({
            url: 'ajax/deck/save/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: {'reference': 'deck_lineup', 'order': 0, 'data': JSON.stringify(me.data)},
            dataType: 'json',
            success: function (answer) {
                me.source = undefined;
            },
            error: function (answer) {
                console.error(me.data);
            }
        });
    }

    load() {
        let me = this;
        $.ajax({
            url: 'ajax/deck/load/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: {'reference': 'deck_lineup', 'order': 0},
            dataType: 'json',
            success: function (answer) {
                let data = JSON.parse(answer['data'])
                me.source = undefined;
                _.forEach(me.data, function (e, i) {
                    _.forEach(data, function (f, j) {
                        if (e.rid == f.rid) {
                            e.full_name = f.full_name;
                            e.idx = f.idx;
                            e.entrance = f.entrance;
                            e.alliance = f.alliance;
                            e.alliance_color1 = f.alliance_color1;
                            e.alliance_color2 = f.alliance_color2;
                            e.ox = f.ox;
                            e.oy = f.oy;
                            e.selected = f.selected;
                            e.group = f.group;
                            e.links = f.links;
                        }
                    });
                });
                // console.log(me.data)
                me.updateGroup();
                me.updateCard();
                me.updateLink();
            },
            error: function (answer) {
                console.error(me.data);
            }
        });
    }

    reset() {
        let me = this;
        me.source = undefined;
        _.forEach(me.data, function (e, i) {
            e.ox = (e.idx % me.row_max) * (me.cardw + 1) + me.basex;
            e.oy = Math.floor(e.idx / me.row_max) * (me.cardh + 1) + me.basey;
            e.selected = false;
            e.group = 0;
            e.links = []
        });
        me.updateGroup();
        me.updateCard();
        me.updateLink();
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

    drawLine(x1 = 1, x2 = 23, y1 = 1, y2 = 35, stroke = '#888888', size = 1, dasharray = "", opacity = 1) {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawLine !')
        } else {
            me.daddy.append('line')
                .attr('x1', function (d) {
                    return me.stepx * (d.ox + x1);
                })
                .attr('y1', function (d) {
                        return me.stepy * (d.oy + y1);
                    }
                )
                .attr('x2', function (d) {
                    return me.stepx * (d.ox + x2);
                })
                .attr('y2', function (d) {
                        return me.stepy * (d.oy + y2);
                    }
                )
                .style('stroke', function (d) {
                    if (d.selected) {
                        return "#A22";
                    }
                    return stroke;
                })
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
                .attr('x', function (d) {
                    return (d.ox + x) * me.stepx;
                })
                .attr('y', function (d) {
                    return (d.oy + y) * me.stepy;
                })
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
                .attr('x', function (d) {
                    return me.stepx * (d.ox + x);
                })
                .attr('y', function (d) {
                        return me.stepy * (d.oy + y);
                    }
                )
                .style('fill', fill)
                .style('stroke', stroke)
                .style('stroke-width', '0.05pt')
                .style("text-anchor", position)
                .style("font-size", size + 'pt')
                .style("font-family", f)
                .text(function (d) {
                    let words = text.split('__');
                    if (words.length == 1) {
                        return text;
                    }
                    return d[words[1]];
                });
        }
    }

    drawCircle(radius, dash, x = 0, y = 0, width = 1, name = undefined, field = undefined) {
        let me = this;
        if (!me.daddy) {
            console.error('Daddy is undefined for drawCircle !')
        } else {
            let group = me.daddy.append('g')
                .attr("id", function (d) {
                    if (name != undefined) {
                        return d["rid"] + "__" + name;
                    } else {
                        return ""
                    }
                })
                .on("click", function (e, d) {
                    e.preventDefault()
                    if (e.ctrlKey) {
                        if (field != undefined) {
                            d.group += 1;
                            d.group = d.group % 10;
                        }
                        me.updateCard();
                    }
                })
            ;
            group.append('circle')
                .attr('cx', function (d) {
                    return me.stepx * (d.ox + x);
                })
                .attr('cy', function (d) {
                        return me.stepy * (d.oy + y);
                    }
                )
                .attr('r', radius * me.stepx)
                .style('fill', function (d) {
                    if (field != undefined) {
                        if (field.startsWith('alliance_color')) {
                            return d[field];
                        }
                    }
                    return '#fff';
                })
                .style('stroke', function (d) {
                    if (field != undefined) {
                        if (field == 'group') {
                            if (d[field] != 0) {
                                return me.group_colors[d[field]]
                            }
                        }
                    }
                    return me.draw_fill
                })
                .style('stroke-dasharray', dash)
                .style('stroke-width', width + 'pt')
            ;
            group.append('text')
                .attr('x', function (d) {
                        return me.stepx * (d.ox + x);
                    }
                )
                .attr('y', function (d) {
                        return me.stepy * (d.oy + y);
                    }
                )
                .attr('dx', 0)
                .attr('dy', '4pt')
                .style('fill', me.draw_fill)
                .style('stroke', me.draw_stroke)
                .style('stroke-width', '0.05pt')
                .style("text-anchor", 'middle')
                .style("font-size", '10pt')
                .style("font-family", me.base_font)
                .text(function (d) {
                        if (field != undefined) {
                            if (field.startsWith('alliance_color') == false) {
                                return d[field];
                            }
                        }
                    }
                )
        }
    }

    buildLinks() {
        let me = this;
        _.forEach(me.links, function (e, i) {
            e.removable = true;
        })
        _.forEach(me.data, function (e, i) {
            _.forEach(e.links, function (l, j) {
                let existing = _.find(me.links, {start:e.rid, stop:l})
                if (existing) {
                    e.removable = false;
                }else{
                    me.links.push({
                        "start": e.rid,
                        "stop": l,
                        "removable":false
                    });
                }
            });
        });
        _.forEach(me.links, function (e, i) {
            if (e.removable){
                me.links.splice(i,1);
            }
        })
        console.log("Build links")
        console.log(me.links)
        me.drawLinks();
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
            .attr('d', 'M -1,-3 L9,0 L-1,3 z ')
            .style('fill', me.draw_fill)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '0pt')
        ;
        me.spanwidth = 4;
        me.spanheight = 2;
        me.rows = 24 * me.spanwidth;
        me.cols = 36 * me.spanheight;
        me.back.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', me.width * me.spanwidth)
            .attr('height', me.height * me.spanheight)
            .style('fill', '#999')
            .style('stroke', me.draw_stroke)
            .style('stroke-width', '0')
            .attr('opacity', 1.0)
        ;

        // Grid
        if (me.debug) {
            let verticals = me.back.append('g')
                .attr('class', 'verticals')
                .selectAll("g")
                .data(d3.range(0, me.rows, 1));
            verticals.enter()
                .append('line')
                .attr('x1', function (d) {
                    return d * me.stepx
                })
                .attr('y1', 0)
                .attr('x2', function (d) {
                    return d * me.stepx
                })
                .attr('y2', me.cols * me.stepy)
                .style('fill', 'transparent')
                .style('stroke', '#000')
                .style('stroke-width', '0.25pt');
            let horizontals = me.back.append('g')
                .attr('class', 'horizontals')
                .selectAll("g")
                .data(d3.range(0, me.cols, 1));
            horizontals.enter()
                .append('line')
                .attr('x1', 0)
                .attr('x2', me.rows * me.stepx)
                .attr('y1', function (d) {
                    return d * me.stepy
                })
                .attr('y2', function (d) {
                    return d * me.stepy
                })
                .style('fill', 'transparent')
                .style('stroke', '#000')
                .style('stroke-width', '0.25pt');
        }
        me.groups = me.back.append('g')
            .attr('class', 'groups');
        me.deck = me.back.append('g')
            .attr('class', 'deck');
        me.relations = me.back.append('g')
            .attr('class', 'relations');
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
            .style("font-size", me.medium_font_size + 'pt')
            .style("fill", me.user_fill)
            .style("stroke", me.user_stroke)
            .style("stroke-width", '0.05pt');
        let words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = me.small_font_size,
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
                    .style("font-size", me.medium_font_size + 'pt')
                    .style("stroke-width", '0.05pt')
                    .text(word);
            }
        }
        return (lineNumber);
    }

    fillPicture(basex, basey, text) {
        let me = this;
        me.daddy.append("rect")
            .attr('x', function (d) {
                return me.stepx * (d.ox + basex + 0.5);
            })
            .attr('y', function (d) {
                    return me.stepy * (d.oy + basey + 1.25);
                }
            )
            .attr("stroke-width", "1pt")
            .attr("stroke", me.draw_fill)
            .attr("fill", me.shadow_fill)
            .attr("width", 3 * me.stepx)
            .attr("height", 4 * me.stepy)
        ;
        me.daddy.append("svg:image")
            .attr("xlink:href", function (d) {
                let imglnk = 'media/images/f_' + d[text] + ".jpg";
                return imglnk;
            })
            .attr('x', function (d) {
                return me.stepx * (d.ox + basex + 0.5);
            })
            .attr('y', function (d) {
                    return me.stepy * (d.oy + basey + 1.25);
                }
            )
            .attr("width", 3 * me.stepx)
            .attr("height", 4 * me.stepy)

        ;
    }

    drawCards() {
        let me = this;
        if (me.initial == true) {
            let idx = 0;
            _.forEach(me.data, function (e, i) {
                e.idx = idx;
                e.ox = (idx % me.row_max) * (me.cardw + 1) + me.basex;
                e.oy = Math.floor(idx / me.row_max) * (me.cardh + 1) + me.basey;
                e.selected = false;
                e.group = 0;
                e.tapped = false;
                e.links = [];
                idx++;
            });
            // me.data[26].links = ["sanjuk_oj_kaval", "neiad_shafeer_almalik"];
            // me.data[14].links = ["drunn_paarlkretzzer"];
            me.initial = false;
        }
        me.card = me.deck.selectAll('.card')
            .data(me.data)
            .enter()
        ;
        me.card_enter = me.card.append('g')
            .attr('class', 'card draggable')
            .attr('id', function (d) {
                return d['rid'];
            });
        me.card_exit = me.card.exit().remove();
        me.updateCard();

    }

    drawLinks() {
        let me = this;
        me.link = me.relations.selectAll('.link')
            .data(me.links)
            .enter()
        ;
        me.link_enter = me.link.append('g')
            .attr('class', 'link')
            .attr("id",function(d){
                return d.start+"__"+d.stop;
            })
        ;
        me.link_exit = me.link.exit().remove();
        me.updateLink();
    }

    drawGroups() {
        let me = this;
        me.group = me.groups.selectAll('.group')
            .data(me.groupdefs)
            .enter()
        ;
        me.group_enter = me.group.append('g')
            .attr('class', 'group')
            .attr('id', function (d) {
                return "group_" + d['num'];
            });
        me.group_exit = me.group.exit().remove();
        me.updateGroup();
    }

    updateGroup() {
        let me = this;
        me.group_enter.select('g.group_back').remove()
        me.group_back = me.group_enter.append('g')
            .attr("class", "group_back");
        me.group_back.append('rect')
            .attr("x", function (d) {
                let olddox = d.ox
                d.ox = undefined;
                _.forEach(me.data, function (e, i) {
                    if (e.group == d["num"]) {
                        if (d.ox == undefined) {
                            d.ox = e.ox;
                        } else if (e.ox < d.ox) {
                            d.ox = e.ox;
                        }

                    }
                })
                if (d.ox == undefined) {
                    d.ox = olddox
                }
                return (d.ox - 1) * me.stepx;
            })
            .attr("y", function (d) {
                let olddoy = d.oy;
                d.oy = undefined;
                _.forEach(me.data, function (e, i) {
                    if (e.group == d.num) {
                        if (d.oy == undefined) {
                            d.oy = e.oy
                        } else if (e.oy < d.oy) {
                            d.oy = e.oy;
                        }
                    }

                })
                if (d.oy == undefined) {
                    d.oy = olddoy
                }
                return (d.oy - 1) * me.stepy;
            })
            .attr("width", function (d) {
                let xmax = d.ox;
                _.forEach(me.data, function (e, i) {
                    if (e.group == d.num) {
                        if (e.ox >= xmax) {
                            xmax = e.ox;
                        }
                    }
                })
                return (xmax - d.ox + me.cardw + 2) * me.stepx;
            })
            .attr("height", function (d) {
                let ymax = d.oy;
                _.forEach(me.data, function (e, i) {
                    if (e.group == d.num) {
                        if (e.oy >= ymax) {
                            ymax = e.oy;
                        }
                    }
                })
                return (ymax - d.oy + me.cardh + 2) * me.stepy;
            })
            .attr("rx", "15pt")
            .style("stroke", function (d) {
                return d.stroke;
            })
            .style("stroke-width", "10pt")
            .style("fill", function (d) {
                return d.stroke;
            })
            .style("stroke-dasharray", "3 3")
            .attr("fill-opacity", 0.5)
        ;
    }

    updateCard() {
        let me = this;
        me.daddy = me.card_enter;
        me.daddy.attr("tapped", function (d) {
            return d.tapped;
        })
        me.daddy.select('g.card_back').remove()
        me.daddy.select('g.card_top').remove()
        me.card_back = me.daddy.append('g')
            .attr("class", "card_back")
            .attr("tapped", function (d) {
                return d.tapped;
            })
        ;
        me.card_top = me.daddy.append('g')
            .attr("class", "card_top")
            .attr("tapped", function (d) {
                return d.tapped;
            })
        ;
        me.daddy = me.card_back;
        me.fillCardBack();
        me.daddy = me.card_top;
        me.fillCardTop();
    }

    updateLink() {
        let me = this;
        let c1 = undefined;
        let c2 = undefined;
        let offset = 0;
        console.log("updateLink")
        console.log(me.links)
        me.daddy = me.link_enter;
        me.daddy.select('g.link_back').remove()
        me.link_back = me.daddy.append('g')
            .attr("class", "link_back")
        ;
        me.link_back.append('line')
            .attr('x1', function (d) {
                c1 = _.find(me.data, {rid: d.start});
                c2 = _.find(me.data, {rid: d.stop});
                if (c1 && c2) {
                    if (Math.abs(c1.ox - c2.ox) < me.cardw) {
                        offset = 0
                    } else if (c1.ox - c2.ox - me.cardw < 0) {
                        offset = me.cardw / 2 + me.delta;
                    } else {
                        offset = -(me.cardw / 2 + me.delta);
                    }
                    return (offset + c1.ox + me.cardw / 2) * me.stepx;
                }
                return 0;

            })
            .attr('y1', function (d) {
                c1 = _.find(me.data, {rid: d.start});
                c2 = _.find(me.data, {rid: d.stop});
                if (c1 && c2) {
                    if (Math.abs(c1.oy - c2.oy) < me.cardh) {
                        offset = 0
                    } else if (c1.oy - c2.oy - me.cardh < 0) {
                        offset = me.cardh / 2 + me.delta;
                    } else {
                        offset = -(me.cardh / 2 + me.delta);
                    }
                    return (offset + c1.oy + me.cardh / 2) * me.stepy;
                }
                return 0;
            })
            .attr('x2', function (d) {
                c1 = _.find(me.data, {rid: d.start});
                c2 = _.find(me.data, {rid: d.stop});
                if (c1 && c2) {
                    if (Math.abs(c2.ox - c1.ox) < me.cardw) {
                        offset = 0
                    } else if (c2.ox - c1.ox - me.cardw < 0) {
                        offset = me.cardw / 2 + me.delta;
                    } else {
                        offset = -(me.cardw / 2 + me.delta);
                    }
                    return (offset + c2.ox + me.cardw / 2) * me.stepx;
                }
                return 0
            })
            .attr('y2', function (d) {
                c1 = _.find(me.data, {rid: d.start});
                c2 = _.find(me.data, {rid: d.stop});
                if (c1 && c2) {
                    if (Math.abs(c1.oy - c2.oy) < me.cardh) {
                        offset = 0
                    } else if (c2.oy - c1.oy - me.cardh < 0) {
                        offset = me.cardh / 2 + me.delta;
                    } else {
                        offset = -(me.cardh / 2 + me.delta);
                    }
                    return (offset + c2.oy + me.cardh / 2) * me.stepy;
                }
                return 0;
            })
            .style("stroke", "#111")

            .style("stroke-width", "3pt")
            .style("stroke-linecap", "round")
            .attr('marker-end', 'url(#arrowhead)')
            .attr("opacity", 0.8)
        ;
    }


    fillCardBack() {
        let me = this;
        // console.log("Card is actually " + me.daddy.attr("tapped"))
        if (me.daddy.attr("tapped") == 'true') {
            // console.log("tapped card")
            me.drawRect(0 - me.delta * 2, 0 - me.delta * 2, me.cardw + 4 * me.delta, me.cardh + 4 * me.delta, "#fff", "#111", 1, "2 1", 1, 10)
            me.drawRect(0, 0, me.cardw, me.cardh, "#828", "#111", 1, "", 1, 5)
        } else {
            // console.log("visible card")
            me.drawRect(0 - me.delta * 2, 0 - me.delta * 2, me.cardw + 4 * me.delta, me.cardh + 4 * me.delta, "#fff", "#111", 1, "2 1", 1, 10)
            me.drawLine(0 - me.delta, 0 + me.cardw + me.delta, 0, 0, me.draw_fill, 3);
            me.drawLine(0 - me.delta, 0 + me.cardw + me.delta, 0 + me.cardh, 0 + 6, me.draw_fill, 3);
            me.drawLine(0, 0, 0 - me.delta, 0 + 6 + me.delta, me.draw_fill, 3);
            me.drawLine(0 + me.cardw, 0 + me.cardw, 0 - me.delta, 0 + me.cardh + me.delta, me.draw_fill, 3);

            me.drawCircle(0.1, "", 0 + me.cardw * 0, 0 + 0 * me.cardh / 5)
            me.drawCircle(0.1, "", 0 + me.cardw, 0 + me.cardh)
            me.drawCircle(0.1, "", 0 + me.cardw * 0, 0 + me.cardh)
            me.drawCircle(0.1, "", 0 + me.cardw, 0 + me.cardh * 0)
            me.drawCircle(0.1, "", 0 + me.cardw, 17 * me.cardh / 20, 1, '', 'alliance_color1')
            me.drawCircle(0.1, "", 0 + me.cardw, 18 * me.cardh / 20, 1, '', 'alliance_color2')

            me.drawText(0 + me.cardw / 2, 0 - 0.07, me.draw_fill, me.shadow_stroke, me.small_font_size * 0.5, "middle", "DE AUTOMATUM LEGIS");
            me.drawCircle(0.25, "", 0 + me.cardw * 0, 0 + 1 * me.cardh / 10, 2, 'idx', 'idx')
            me.drawCircle(0.25, "", 0 + me.cardw * 0, 0 + 7 * me.cardh / 10, 2,)
            me.drawCircle(0.25, "", 0 + me.cardw * 0, 0 + 8 * me.cardh / 10, 2, 'group', 'group')
        }
    }

    fillCardTop() {
        let me = this;
        if (me.daddy.attr("tapped") == 'true') {

        } else {
            me.drawText(0 + me.cardw / 2, 0 + 0.5, me.draw_fill, me.shadow_stroke, me.medium_font_size * 0.8, "middle", "__full_name");
            me.drawText(0 + me.cardw / 2, 0 + 1.0, me.draw_fill, me.shadow_stroke, me.medium_font_size * 0.8, "middle", "__alliance");
            me.drawText(0 + me.cardw / 2, 0 + 5.8, me.draw_fill, me.shadow_stroke, me.small_font_size, "middle", "__entrance");
            me.fillPicture(0, 0, "rid");

            me.daddy.append('rect')
                .attr('x', function (d) {
                    return (d.ox - 0.125 + 10 * me.cardw / 10) * me.stepx;
                })
                .attr('y', function (d) {
                    return (d.oy + 7 * me.cardh / 10) * me.stepy;
                })
                .attr('width', 0.25 * me.stepx)
                .attr('height', 0.25 * me.stepy)
                .style("stroke", me.draw_fill)
                .style("fill", function (d) {
                    if (me.source == d) {
                        return "#A22";
                    }
                    return "#EEE";
                })
                .style("stroke-width", "1pt")
                .style("cursor", "pointer")
                .on("click", function (e, d) {
                    if (e.ctrlKey == true) {
                        if (me.source == undefined) {
                            me.source = d;
                        } else if (me.source == d) {
                            me.source = undefined;
                        } else if (me.source.links.indexOf(d.rid) != -1) {
                            let x = me.source.links.indexOf(d.rid);
                            me.source.links.splice(x, 1);
                        } else {
                            me.source.links.push(d.rid);
                            me.source.links.sort();
                            me.source = undefined;
                        }
                        me.buildLinks()
                        console.log("link click")
                        console.log(me.links)
                        me.updateGroup();
                        me.updateCard();
                        me.updateLink();
                    }
                })
            ;

        }
    }

    zoomActivate() {
        let me = this;
        me.zoom = d3.zoom()
            .scaleExtent([0.25, 4])
            .on('zoom', function (event) {
                // if (event.sourceEvent.altKey) {
                me.svg.attr('transform', event.transform)
                // }
            });
        me.vis.call(me.zoom);
    }

    dragActivate() {
        let me = this;
        me.drag = d3.drag();
        me.drag
            .on("start", function (e, d) {
                d.selected = true
                me.updateCard();
            })
            .on("drag", function (e, d) {
                d.ox = d.ox + e.dx / me.stepx;
                d.oy = d.oy + e.dy / me.stepy;
                me.updateCard();
            })
            .on("end", function (e, d) {
                d.ox = Math.round(d.ox);
                d.oy = Math.round(d.oy);
                if (d.selected == true) {
                    d.tapped = false;
                    // console.log("yo")
                }
                d.selected = false;
                // console.log("untap")
                me.updateGroup();
                me.updateCard();
                me.updateLink();
            })
        ;
        me.svg.selectAll(".draggable").call(me.drag);
    }


    perform() {
        let me = this;

        me.drawWatermark();
        me.drawGroups();
        me.drawCards();
        me.drawLinks();

        me.drawButtons();
        me.zoomActivate();
        me.dragActivate();
        $(me.parent).css('display', 'block');
    }
}


