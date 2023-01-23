class SessionSheets extends Sheet {
    constructor(data, parent, collector) {
        super(data, parent, collector)
        this.disposition = "paysage"
        this.init();
        console.log(data.adventure)
        this.adventure_data = [
            {'label': '', 'text': data.adventure.epic_name},
            {'label': '', 'text': ''},
            {'label': 'Title', 'text': data.adventure.name.toUpperCase()},
            {'label': '', 'text': ''},
            {'label': 'Session Part', 'text': data.adventure.full_id},
            {'label': 'Memorandum', 'text': data.adventure.abstract},
            {'label': 'Ingame date', 'text': data.adventure.date_str},
            {'label': '', 'text': ''},
            {'label': 'Session Date', 'text': data.adventure.session_date_str},
            {'label': 'Gamemaster', 'text': data.adventure.gamemaster},
            {'label': '', 'text': ''},
            {'label': 'Max XP Award', 'text': data.adventure.experience}
        ]
    }

    init() {
        super.init();
        let me = this;
        me.figure_width = 5;
        me.setButtonsOrigin(36, 2)
    }

    drawButtons() {
        let me = this;
        me.addButton(0, 'Save SVG');
        me.addButton(1, 'Recto');
        me.addButton(2, 'Verso');
        // me.addButton(3, 'Close');
    }

    drawPages(page = 0) {
        let me = this;
        super.drawPages(page);
        // Sheet content
        me.lines = me.back.append('g');
        me.daddy = me.lines;
        // External lines
        me.drawLine(1, 1, 0.5, me.yunits - 0.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
        me.drawLine(me.xunits - 1, me.xunits - 1, 0.5, me.yunits - 0.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
        me.drawLine(0.5, me.xunits - 0.5, 1, 1, me.draw_fill, me.draw_fill, 6, me.strokedebris);
        me.drawLine(0.5, me.xunits - 0.5, me.yunits - 1, me.yunits - 1, me.draw_fill, me.draw_fill, 6, me.strokedebris);


        me.decorationText(1.5, 0.8, 0, 'start', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, "Players Session Sheet - FuZion Interlock Custom System v8.0", me.back);
        me.decorationText(me.xunits - 1.2, me.yunits - 0.2, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "doc:session_sheets | v" + me.version + " | 2022 | Zaffarelli | generated with DP", me.back);


        let title_text = 'Fading Suns'.toUpperCase();
        me.decorationText(5, 22.32, 0, 'middle', me.title_font, me.fat_font_size * 0.8, '#FFF', '#FFF', 5, title_text, me.back, 1.0);
        me.drawJumpgateLogo(5 * me.stepx, 22 * me.stepy)
        me.decorationText(5, 22.32, 0, 'middle', me.title_font, me.fat_font_size * 0.8, me.draw_fill, me.draw_stroke, 1, title_text, me.back, 1);


        me.characters = me.back.append('g')
            .attr('class', 'session_sheets');

    }

    drawGeneric(ox = 0, oy = 0) {
        let me = this;
        me.generic = me.back.append('g')
            .attr('class', "generic");
        me.daddy = me.generic;
        me.drawRect(ox, oy, 7, 21, "transparent", me.shadow_stroke);
        me.adventure_entry = me.generic.selectAll('.adventure_entry')
            .append('g')
            .attr('transform', "translate(" + (ox * me.stepx) + "," + (6 * me.stepy) + ")")
            .data(me.adventure_data)
            .enter();
        let aei = me.adventure_entry.append('g')
            .attr('class', 'adventure_entry')
        aei.append('text')
            .attr('x', function (d, i) {
                return (ox+0.25) * me.stepx;
            })
            .attr('y', function (d, i) {
                return (oy + (i+1) / 2) * me.stepy;
            })
            .style('fill', me.draw_fill)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', "0.5pt")
            .style('font-family', me.base_font)
            .style('font-size', me.small_font_size)
            .text(function (d) {
                return d["label"];
            });
        aei.append('text')
            .attr('x', function (d, i) {
                return (ox+7-0.25) * me.stepx;
            })
            .attr('y', function (d, i) {
                return (oy + (i+1)/2) * me.stepy;
            })
            .style('fill', me.user_fill)
            .style('stroke', me.user_stroke)
            .style('stroke-width', "0.5pt")
            .style('font-family', me.user_font)
            .style('font-size', me.medium_font_size)
            .style('text-anchor', 'end')
            .text(function (d) {
                return d['text'];
            })

        ;


    }

    drawFigures(ox = 0, oy = 0) {
        let me = this;
        me.player = me.characters.selectAll('.players')
            .append('g')
            .attr('transform', "translate(" + (ox * me.stepx) + "," + (6 * me.stepy) + ")")
            .data(me.data)
            .enter()
        me.player.append('g')
            .attr('class', 'players')
            .append('rect')
            .attr('x', function (d) {
                return d['idx'] * me.stepx * me.figure_width + ox * me.stepx;
            })
            .attr("y", function (d) {
                return me.stepy * (oy);
            })
            .attr('width', function (d) {
                return me.stepx * me.figure_width
            })
            .attr('height', function (d) {
                return me.stepy * 21;
            })
            .style('fill', "none")
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', "0.5mm")
        ;
        me.daddy = me.player;

        let xfunc = function (x) {
            return x * me.stepx * me.figure_width + (ox + 0.25) * me.stepx;
        }
        me.sheetEntry(xfunc, 0.5, ox, oy, "Name", "full_name", me.big_font_size,)
        me.sheetEntry(xfunc, 1.0, ox, oy, "Player", "player")

        me.sheetEntryLeft(xfunc, 2.0, ox, oy, "Hit Points", "SA_END")
        me.sheetEntryRight(xfunc, 2.0, ox, oy, "Recovery", "SA_REC")
        me.sheetEntryLeft(xfunc, 2.5, ox, oy, "Stun", "SA_STU")
        me.sheetEntryRight(xfunc, 2.5, ox, oy, "STA mod", "SA_STA")

        me.sheetEntryLeft(xfunc, 3.0, ox, oy, "DMG mod", "SA_DMG")

        me.sheetEntryLeft(xfunc, 3.5, ox, oy, "Passion", "SA_PAS")
        me.sheetEntryRight(xfunc, 3.5, ox, oy, "Wyrd", "SA_WYR")

        me.sheetEntryLeft(xfunc, 4.5, ox, oy, "STR", "PA_STR")
        me.sheetEntryRight(xfunc, 4.5, ox, oy, "BOD", "PA_BOD")
        me.sheetEntryLeft(xfunc, 5.0, ox, oy, "CON", "PA_CON")
        me.sheetEntryRight(xfunc, 5.0, ox, oy, "MOV", "PA_MOV")

        me.sheetEntryLeft(xfunc, 6.0, ox, oy, "INT", "PA_INT")
        me.sheetEntryRight(xfunc, 6.0, ox, oy, "WIL", "PA_WIL")
        me.sheetEntryLeft(xfunc, 6.5, ox, oy, "TEM", "PA_TEM")
        me.sheetEntryRight(xfunc, 6.5, ox, oy, "PRE", "PA_PRE")

        me.sheetEntryLeft(xfunc, 7.5, ox, oy, "TEC", "PA_TEC")
        me.sheetEntryRight(xfunc, 7.5, ox, oy, "REF", "PA_REF")
        me.sheetEntryLeft(xfunc, 8.0, ox, oy, "AGI", "PA_AGI")
        me.sheetEntryRight(xfunc, 8.0, ox, oy, "AWA", "PA_AWA")

        let any = 9.0;
        me.sheetEntry(xfunc, any, ox, oy, "Academia", "skills_list", 0, "skill", "Academia"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Dodge", "skills_list", 0, "skill", "Dodge"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Empathy", "skills_list", 0, "skill", "Empathy"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Etiquette", "skills_list", 0, "skill", "Etiquette"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Focus", "skills_list", 0, "skill", "Focus"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Observe", "skills_list", 0, "skill", "Observe"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Knavery", "skills_list", 0, "skill", "Knavery"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Seduction", "skills_list", 0, "skill", "Seduction"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Streetwise", "skills_list", 0, "skill", "Streetwise"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Stoic Body", "skills_list", 0, "skill", "Stoic Body"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Stoic Mind", "skills_list", 0, "skill", "Stoic Mind"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Warfare", "skills_list", 0, "skill", "Warfare"); any += 0.5;


        me.drawLine(ox, me.figure_width, oy + any, oy + any, me.draw_fill, me.draw_fill, 1, me.strokedebris); any += 0.5;


        me.sheetEntry(xfunc, any, ox, oy, "Azurites", "azurites"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Diamonds", "diamonds"); any += 0.5;
        me.sheetEntry(xfunc, any, ox, oy, "Rubies", "rubies"); any += 0.5;


        me.drawLine(ox, ox+ me.figure_width, oy + any, oy + any, me.draw_fill, me.draw_fill, 1, me.strokedebris); any += 0.5;


        me.drawLine(ox, ox+ me.figure_width, oy + 1.5, oy + 1.5, me.draw_fill, me.draw_fill, 1, me.strokedebris);any += 0.5;
        me.drawLine(ox, ox+ me.figure_width, oy + 4.0, oy + 4.0, me.draw_fill, me.draw_fill, 1, me.strokedebris);any += 0.5;any += 0.5;
        me.drawLine(ox, ox+ me.figure_width, oy + 5.5, oy + 5.5, me.draw_fill, me.draw_fill, 1, me.strokedebris);any += 0.5;
        me.drawLine(ox, ox+ me.figure_width, oy + 7.0, oy + 7.0, me.draw_fill, me.draw_fill, 1, me.strokedebris);any += 0.5;
        me.drawLine(ox, ox+ me.figure_width, oy + 8.5, oy + 8.5, me.draw_fill, me.draw_fill, 1, me.strokedebris);any += 0.5;


    }

    baseSheetEntry(xfunc, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '', offsetx = 0, offsetx2 = 0) {
        let me = this;
        if (font_size == 0) {
            font_size = me.small_font_size;
        }
        console.log(font_size);
        me.daddy.append('text')
            .attr('x', function (d) {
                return xfunc(d['idx']) + offsetx * me.stepx;
            })
            .attr('y', function (d) {
                return (oy + y) * me.stepy;
            })
            .style('fill', me.draw_fill)
            .style('stroke', me.draw_stroke)
            .style('stroke-width', "0.5pt")
            .style('font-family', me.base_font)
            .style('font-size', (me.small_font_size-2)+'pt')
            .text(function (d) {
                return proplabel;
            })
        ;
        me.daddy.append('text')
            .attr('x', function (d) {
                return xfunc(d['idx']) + offsetx2 * me.stepx;
            })
            .attr('y', function (d) {
                return (oy + y) * me.stepy;
            })
            .style('fill', me.user_fill)
            .style('stroke', me.user_stroke)
            .style('stroke-width', "0.5pt")
            .style('text-anchor', 'end')
            .style('font-family', me.user_font)
            .style('font-size', (font_size) + "pt")
            .text(function (d) {
                let result = d[prop]
                if (direct_value != '') {
                    _.forEach(d[prop], function (e) {
                        if (e[direct_prop] == direct_value) {
                            result = e['value'];
                            return false;
                        }
                    });
                }
                return result
            })
        ;

    }

    sheetEntryLeft(xfunc, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(xfunc, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125, 2.25)
    }

    sheetEntryRight(xfunc, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(xfunc, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, 2.75 - 0.125, 4.5)
    }

    sheetEntry(xfunc, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(xfunc, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125, 4.5)
    }


    perform(character_data = null, page = 0) {
        let me = this;
        console.log('FICS_SHEET: Performing...');
        if (character_data) {
            // me.data = character_data;
            me.data = Array()
            _.forEach(character_data, function (e, k) {
                me.data.push(JSON.parse(e));
            })
            console.log(me.data)
        }

        $(me.parent).css('display', 'block');
        me.drawWatermark(page);

        // me.fillCharacter(page);
        me.drawGeneric(1.5, 1.5);
        me.drawFigures(9, 1.5);
        me.drawButtons();
        me.zoomActivate();
    }
}


