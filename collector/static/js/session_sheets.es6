class SessionSheets extends Sheet {
    constructor(data, parent, collector) {
        super(data, parent, collector)
        this.disposition = "paysage"
        this.init();
        this.adventure_data = [
            {'label': 'Title', 'text': 'The Tiger of Istakhr'},
            {'label': '', 'text': ''},
            {'label': 'Session Part', 'text': '#7'},
            {'label': 'Memorandum', 'text': 'The Grand Finale'},
            {'label': 'Ingame date', 'text': '5022-01-28'},
            {'label': 'Session Date', 'text': '2022-05-20'},
            {'label': 'Gamemaster', 'text': 'Zaffarelli'},
            {'label': '', 'text': ''},
            {'label': 'Experience', 'text': '5+21 per PC'}
        ]
    }

    init() {
        super.init();
        let me = this;
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


        me.decorationText(1.5, 0.8, 0, 'start', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, "Players Session Sheet - FuZion Interlock Custom System v10", me.back);
        me.decorationText(me.xunits - 1.2, me.yunits - 0.2, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "doc:session_sheets | v" + me.version + " | 2025 | Zaffarelli | generated with DP", me.back);


        let title_text = 'Fading Suns'.toUpperCase();
        me.decorationText(4.5, 22.32, 0, 'middle', me.title_font, me.fat_font_size * 0.8, '#FFF', '#FFF', 5, title_text, me.back, 1.0);
//         me.drawJumpgateLogo(5 * me.step, 22 * me.step)
        me.decorationText(4.5, 22.32, 0, 'middle', me.title_font, me.fat_font_size * 0.8, me.draw_fill, me.draw_stroke, 1, title_text, me.back, 1);

        me.characters = me.back.append('g')
            .attr('class', 'players');


    }

    drawGeneric(ox = 0, oy = 0) {
        let me = this;
        me.generic = me.back.append('g')
            .attr('class', "generic");
        me.daddy = me.generic;
        me.drawRect(ox, oy, 6, 21, "transparent", me.shadow_stroke);
        me.adventure_entry = me.generic.selectAll('.adventure_entry')
            .append('g')
            .attr('transform', "translate(" + (ox * me.step) + "," + (6 * me.step) + ")")
            .data(me.adventure_data)
            .enter();
        let aei = me.adventure_entry.append('g')
            .attr('class', 'adventure_entry')
        aei.append('text')
            .attr('x', function (d, i) {
                return (ox+0.25) * me.step;
            })
            .attr('y', function (d, i) {
                return (oy + (i+1) / 2) * me.step;
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
                return (ox+6-0.25) * me.step;
            })
            .attr('y', function (d, i) {
                return (oy + (i+1)/2) * me.step;
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
        me.players = me.characters.selectAll('.players')
            .append('g')
            .data(me.data)
        me.player = me.players.enter()
        me.player_item = me.player.append('g')
            .attr('class', 'player')
        me.player_item.append('rect')
            .attr('x', function (d) {
                return d['idx'] * me.step * 5 + ox * me.step;
            })
            .attr("y", function (d) {
                return me.step * (oy);
            })
            .attr('width', function (d) {
                return me.step * 5
            })
            .attr('height', function (d) {
                return me.step * 21;
            })
            .style('fill', "none")
            .style('stroke', me.shadow_stroke)
            .style('stroke-width', "0.5mm")
        ;
        me.daddy = me.player;

        let xfunc = function (x) {
            return x * me.step * 5 + (ox + 0.25) * me.step;
        }

        let xfunc2 = function (x) {
            return x * (me.step * 5)+ (me.step*5)%3 + (ox + 0.25) * me.step;
        }


        me.sheetEntry(xfunc, 0.5, ox, oy, "Name", "full_name", me.medium_font_size,)
        me.sheetEntry(xfunc, 1.0, ox, oy, "Player", "player")

        me.sheetEntryLeft(xfunc, 2.0, ox, oy, "Hit Points", "SA_END")
        me.sheetEntryRight(xfunc, 2.0, ox, oy, "Recovery", "SA_REC")
        me.sheetEntryLeft(xfunc, 2.5, ox, oy, "Stun", "SA_STU")
        me.sheetEntryRight(xfunc, 2.5, ox, oy, "STA mod", "SA_STA")

        me.sheetEntryLeft(xfunc, 3.0, ox, oy, "DMG mod", "SA_DMG")

        me.sheetEntryLeft(xfunc, 3.5, ox, oy, "Passion", "SA_PAS")
        me.sheetEntryRight(xfunc, 3.5, ox, oy, "Wyrd", "SA_WYR")

        me.sheetEntryTriA(xfunc2, 4.5, ox, oy, "STR", "PA_STR")
        me.sheetEntryTriA(xfunc2, 5.0, ox, oy, "BOD", "PA_BOD")
        me.sheetEntryTriA(xfunc2, 5.5, ox, oy, "CON", "PA_CON")
        me.sheetEntryTriA(xfunc2, 6.0, ox, oy, "MOV", "PA_MOV")

        me.sheetEntryTriB(xfunc2, 4.5, ox, oy, "INT", "PA_INT")
        me.sheetEntryTriB(xfunc2, 5.0, ox, oy, "WIL", "PA_WIL")
        me.sheetEntryTriB(xfunc2, 5.5, ox, oy, "TEM", "PA_TEM")
        me.sheetEntryTriB(xfunc2, 6.0, ox, oy, "PRE", "PA_PRE")

        me.sheetEntryTriC(xfunc2, 4.5, ox, oy, "TEC", "PA_TEC")
        me.sheetEntryTriC(xfunc2, 5.0, ox, oy, "DEX", "PA_DEX")
        me.sheetEntryTriC(xfunc2, 5.5, ox, oy, "AGI", "PA_AGI")
        me.sheetEntryTriC(xfunc2, 6.0, ox, oy, "AWA", "PA_AWA")

        let sy = 6.75
        let fs = 1
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Academia", "skills_list", fs, "skill", "Academia"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Adaptation", "skills_list", fs, "skill", "Adaptation"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Alchemy", "skills_list", fs, "skill", "Alchemy"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Athletics", "skills_list", fs, "skill", "Athletics"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Beastcraft", "skills_list", fs, "skill", "Beastcraft"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Bureaucracy", "skills_list", fs, "skill", "Bureaucracy"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Demolition", "skills_list", fs, "skill", "Demolition"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Disguise", "skills_list", fs, "skill", "Disguise"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Empathy", "skills_list", fs, "skill", "Empathy"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Etiquette", "skills_list", fs, "skill", "Etiquette"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Fight", "skills_list", fs, "skill", "Fight"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Focus", "skills_list", fs, "skill", "Focus"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Gunnery", "skills_list", fs, "skill", "Gunnery"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Impress", "skills_list", fs, "skill", "Impress"); sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Inquiry", "skills_list", fs, "skill", "Inquiry"); sy += 0.5
        sy = 6.75
        me.sheetEntryRight(xfunc, sy, ox, oy, "Knavery", "skills_list", fs, "skill", "Knavery"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Leadership", "skills_list", fs, "skill", "Leadership"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Maneuver", "skills_list", fs, "skill", "Maneuver"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Melee", "skills_list", fs, "skill", "Melee"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Observe", "skills_list", fs, "skill", "Observe"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Performance", "skills_list", fs, "skill", "Performance"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Redemption", "skills_list", fs, "skill", "Redemption"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Remedy", "skills_list", fs, "skill", "Remedy"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Riddles", "skills_list", fs, "skill", "Riddles"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Search", "skills_list", fs, "skill", "Search"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Seduction", "skills_list", fs, "skill", "Seduction"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Shoot", "skills_list", fs, "skill", "Shoot"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Sneak", "skills_list", fs, "skill", "Sneak"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Surveillance", "skills_list", fs, "skill", "Surveillance"); sy += 0.5
        me.sheetEntryRight(xfunc, sy, ox, oy, "Teaching", "skills_list", fs, "skill", "Teaching"); sy += 0.5




        me.daddy = me.lines
        me.drawLine(ox, me.xunits - 1.25, oy + 1.25, oy + 1.25, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.drawLine(ox, me.xunits - 1.25, oy + 4.0, oy + 4.0, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.drawLine(ox, me.xunits - 1.25, oy + 6.25, oy + 6.25, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.drawLine(ox, me.xunits - 1.25, oy + 14.0, oy + 14.0, me.draw_fill, me.draw_fill, 1, me.strokedebris);

    }

    baseSheetEntry(func, y, ox = 0, oy = 0, proplabel, prop = '', font = 0, direct_prop = '', direct_value = '', offsetx = 0, offsetx2 = 0) {
        let me = this;
        let font_size = font
        if (font == 0) {
            font_size = me.small_font_size;
        }else
        if (font == 1) {
            font_size = me.small_font_size*1.5
        }
        me.daddy.append('text')
            .attr('x', function (d) {
                return func(d['idx']) + offsetx * me.step;
            })
            .attr('y', function (d) {
                return (oy + y) * me.step;
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
                return func(d['idx']) + offsetx2 * me.step;
            })
            .attr('y', function (d) {
                return (oy + y) * me.step;
            })
            .style('fill', me.user_fill)
            .style('stroke', me.user_stroke)
            .style('stroke-width', "0.5pt")
            .style('text-anchor', 'end')
            .style('font-family', me.user_font)
            .style('font-size', (font_size) + "pt")
            .text((d) => {
                let result = d[prop]
                let tmp = ""
                if (direct_value != '') {
                    _.forEach(d[prop], function (e) {
                        if (e[direct_prop] == direct_value) {
                            result = e['value'];
                            return false;
                        }
                    });
                }

                if (false){
                if (!isNaN(parseInt(result)) && (font==1)) {
                    let v = parseInt(result)
                    if (v<5){
                        for(let r=0;r<4;r++){
                            if (r<v){
                                tmp = "●"+tmp
                            }else{
                                tmp = "○"+tmp
                                }
                        }
                    }else{
                        tmp = "◈"
                        for(let r=6;r<10;r++){
                            if (r<v){
                                tmp = "◆"+tmp
                            }else{
                                tmp = "◇"+tmp
                                }
                        }
                    }
                    result = tmp
                }else{
                    }
                }
                return result
            })

    }

    sheetEntryLeft(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125, 2.25)
    }

    sheetEntryRight(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, 2.75 - 0.125, 4.5)
    }

    sheetEntry(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125, 4.5)
    }

    sheetEntryTriA(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125, 1.5-0.25)
    }

    sheetEntryTriB(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125+1.5+0.25, 3-0.25)
    }

    sheetEntryTriC(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, -0.125+3+0.25, 4.5-0.25)
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
        me.drawGeneric(1.5, 1.5);
        me.drawPages(9, 1.5);
        me.drawFigures(7.8, 1.5);
        me.drawButtons();
        me.zoomActivate();
    }
}


