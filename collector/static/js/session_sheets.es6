
class SessionSheets extends Sheet {
    constructor(data, parent, collector) {
        super(data, parent, collector)

        this.disposition = "paysage"
        this.init();
        this.adventure = data.adventure
        this.adventure_data = [
            {'label': 'Title', 'text': this.adventure.title.toUpperCase()},
            {'label': 'Campaign', 'text': this.adventure.campaign},
            {'label': 'Session Part', 'text': this.adventure.session_part},
            {'label': 'Memorandum', 'text': this.adventure.memorandum},
            {'label': 'Ingame date', 'text': this.adventure.date},
            {'label': 'Session Date', 'text': this.adventure.sessiondate},
            {'label': 'Gamemaster', 'text': this.adventure.gamemaster},
            {'label': 'Experience', 'text': this.adventure.total_challenge}
        ]
        this.part = 4.5/4
    }

    init() {
        super.init();
        let me = this;
        me.setButtonsOrigin(36, 2)
        me.nope = "-"
        me.user_font = 'Julee'
        me.user_font = 'Economica'
    }

    drawButtons() {
        let me = this;
        me.addButton(0, 'PDF Export');
        for(let x=1;x<=me.pages_number;x++){
            me.addButton(x, `Page ${x}`, "browse")
        }
    }

    drawPages(page = 0) {
        let me = this;
        super.drawPages(page);
        // Sheet content
        me.lines = me.back.append('g');
        me.daddy = me.lines;
        // External lines
        me.drawLine(1, 1, 0.5, me.yunits - 0.5, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.drawLine(me.xunits - 1, me.xunits - 1, 0.5, me.yunits - 0.5, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.drawLine(0.5, me.xunits - 0.5, 1, 1, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.drawLine(0.5, me.xunits - 0.5, me.yunits - 1, me.yunits - 1, me.draw_fill, me.draw_fill, 1, me.strokedebris);
        me.decorationText(1.5, 0.8, 0, 'start', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, "Players Session Sheet - FuZion Interlock Custom System v10", me.back);
        me.decorationText(me.xunits - 1.2, me.yunits - 0.2, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "doc:session_sheets | v" + me.version + " | 2025 | Zaffarelli | generated with DP", me.back);


        let title_text = 'Fading Suns'.toUpperCase();
        me.decorationText(4.5, 22.32, 0, 'middle', me.title_font, me.fat_font_size * 0.8, '#FFF', '#FFF', 5, title_text, me.back, 1.0);
        me.decorationText(4.5, 22.32, 0, 'middle', me.title_font, me.fat_font_size * 0.8, me.draw_fill, me.draw_stroke, 1, title_text, me.back, 1);

        me.characters = me.back.append('g')
            .attr('class', 'players');


    }

    drawGeneric(ox = 0, oy = 0) {
        let me = this;
        me.generic = me.back.append('g')
            .attr('class', "generic");
        me.daddy = me.generic;
        me.drawRect(ox, oy, 6, 21, "none", me.shadow_stroke);
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
            .style('font-family', me.base_font)
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
            .attr('id', (d) => d.rid)
        me.player_item.append('rect')
            .attr('x', function (d) {
//                 console.log("d.idx >>",d.idx)
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
        me.daddy = me.lines
        me.drawLine(ox, me.xunits - 1.25, oy + 1.25, oy + 1.25, me.draw_fill, me.draw_fill, 1, me.strokedebris)
        me.drawLine(ox, me.xunits - 1.25, oy + 3.5, oy + 3.5, me.draw_fill, me.draw_fill, 1, me.strokedebris)
        me.drawLine(ox, me.xunits - 1.25, oy + 5.25, oy + 5.25, me.draw_fill, me.draw_fill, 1, me.strokedebris)
        me.drawLine(ox, me.xunits - 1.25, oy + 9.5, oy + 9.5, me.draw_fill, me.draw_fill, 1, me.strokedebris)
        me.daddy = me.player_item;
        let xfunc = function (x) {
            return x * me.step * 5 + (ox + 0.25) * me.step;
        }
        let xfunc2 = function (x) {
            return x * (me.step * 5)+ (me.step*5)%3 + (ox + 0.25) * me.step;
        }
        me.sheetEntry(xfunc, 0.5, ox, oy, "Name", "full_name", me.medium_font_size,)
        me.sheetEntry(xfunc, 1.0, ox, oy, "Player", "player")
        let sy = 1.75
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Hit Points", "SA_END")
        me.sheetEntryRight(xfunc, sy, ox, oy, "Recovery", "SA_REC")
        sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Stun", "SA_STU")
        me.sheetEntryRight(xfunc, sy, ox, oy, "STA mod", "SA_STA")
        sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "DMG mod", "SA_DMG")
        me.sheetEntryRight(xfunc, sy, ox, oy, "Wyrd", "SA_WYR")
        sy += 0.5
        me.sheetEntryLeft(xfunc, sy, ox, oy, "Passion", "SA_PAS")
        // Attributes
        sy = 4.0
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "STR", "PA_STR")
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "BOD", "PA_BOD")
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "CON", "PA_CON")
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "MOV", "PA_MOV")
        sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "INT", "PA_INT")
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "WIL", "PA_WIL")
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "TEM", "PA_TEM")
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "PRE", "PA_PRE")
        sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "TEC", "PA_TEC")
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "DEX", "PA_DEX")
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "AGI", "PA_AGI")
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "AWA", "PA_AWA")
        sy = 5.75
        let fs = 0
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "ACA", "skills_list", fs, "skill", "Academia"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "ADA", "skills_list", fs, "skill", "Adaptation"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "ALC", "skills_list", fs, "skill", "Alchemy"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "ATH", "skills_list", fs, "skill", "Athletics"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "BEA", "skills_list", fs, "skill", "Beastcraft"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "BUR", "skills_list", fs, "skill", "Bureaucracy"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "DEM", "skills_list", fs, "skill", "Demolition"); sy += 0.5
        me.sheetEntryQuadA(xfunc, sy, ox, oy, "DIS", "skills_list", fs, "skill", "Disguise"); sy += 0.5
        sy = 5.75
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "EMP", "skills_list", fs, "skill", "Empathy"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "ETI", "skills_list", fs, "skill", "Etiquette"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "FIG", "skills_list", fs, "skill", "Fight"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "FOC", "skills_list", fs, "skill", "Focus"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "GUN", "skills_list", fs, "skill", "Gunnery"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "IMP", "skills_list", fs, "skill", "Impress"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "INQ", "skills_list", fs, "skill", "Inquiry"); sy += 0.5
        me.sheetEntryQuadB(xfunc, sy, ox, oy, "KNA", "skills_list", fs, "skill", "Knavery"); sy += 0.5
        sy = 5.75
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "LEA", "skills_list", fs, "skill", "Leadership"); sy += 0.5
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "MAN", "skills_list", fs, "skill", "Maneuver"); sy += 0.5
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "MEL", "skills_list", fs, "skill", "Melee"); sy += 0.5
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "OBS", "skills_list", fs, "skill", "Observe"); sy += 0.5
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "PER", "skills_list", fs, "skill", "Performance"); sy += 0.5
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "RED", "skills_list", fs, "skill", "Redemption"); sy += 0.5
        me.sheetEntryQuadC(xfunc, sy, ox, oy, "REM", "skills_list", fs, "skill", "Remedy"); sy += 0.5
        sy = 5.75
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "RID", "skills_list", fs, "skill", "Riddles"); sy += 0.5
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "SEA", "skills_list", fs, "skill", "Search"); sy += 0.5
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "SED", "skills_list", fs, "skill", "Seduction"); sy += 0.5
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "SHO", "skills_list", fs, "skill", "Shoot"); sy += 0.5
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "SNE", "skills_list", fs, "skill", "Sneak"); sy += 0.5
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "SUR", "skills_list", fs, "skill", "Surveillance"); sy += 0.5
        me.sheetEntryQuadD(xfunc, sy, ox, oy, "TEA", "skills_list", fs, "skill", "Teaching"); sy += 0.5
        sy = 10.0
        let tinyjump = .275
        me.baseSheetEntry(xfunc, sy, ox, oy, "Degrees"); sy += 0.35
        for(let dloop=0;dloop<50;dloop++){
            if ((me.baseSheetEntry(xfunc, sy, ox, oy, "", "degrees_list",0,":"+dloop+"::grp","",0,0.75) != me.nope)
            && (me.baseSheetEntry(xfunc, sy, ox, oy, "", "degrees_list",0,":"+dloop+"::refval","",0,3.75) != me.nope)
            && (me.baseSheetEntry(xfunc, sy, ox, oy, "", "degrees_list",0,":"+dloop+"::level","",0,4.25) != me.nope)
            && (me.baseSheetEntry(xfunc, sy, ox, oy, "", "degrees_list",0,":"+dloop+"::value","",0,4.5) != me.nope)){
                sy += tinyjump
            }
        }
        sy += tinyjump
        me.baseSheetEntry(xfunc, sy, ox, oy, "Blessings/Curses"); sy += 0.35
        for(let bcloop=0;bcloop<10;bcloop++){
            if (me.baseSheetEntry(xfunc, sy, ox, oy, "", "BC",0,":"+bcloop+":shortcut","",0,4.5)!= me.nope) {
                sy += tinyjump
            }
        }
        sy += tinyjump
        me.baseSheetEntry(xfunc, sy, ox, oy, "Benefices/Afflictions"); sy += 0.35
        for(let baloop=0;baloop<10;baloop++){
            if (me.baseSheetEntry(xfunc, sy, ox, oy, "", "BA",0,":"+baloop+":benefice_affliction_ref:refval","",0,4.5)!= me.nope){
                sy += tinyjump
            }
        }
    }



    baseSheetEntry(func, y, ox = 0, oy = 0, proplabel, prop = '', font = 0, direct_prop = '', direct_value = '', offsetx_lab = 0, offsetx_dat = 0) {
        let me = this
        let global_result = 1
        let font_size = 0
        let local_opacity = 1
        // Font selection
        switch (font){
            case 0:
                font_size = me.tiny_font_size
                break;
            case 1:
                font_size = me.small_font_size
                break;
            default:
                font_size = font
                break;
            }
        // Label (proplabel can be "")
        me.daddy.append('text')
            .attr('x', function (d) {
                return func(d['idx']) + offsetx_lab * me.step;
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
        // Text data
        let stroke_width = "0.5pt"
        me.daddy.append('text')
            .attr('x', (d) => func(d['idx']) + offsetx_dat * me.step )
            .attr('y', (d) => (oy + y) * me.step )
            .style('stroke', me.user_stroke)
            .style('fill', me.user_fill)
            .style('text-anchor', 'end')
            .style('font-family', me.user_font)
            .style('font-size', (font_size) + "pt")
            .text((d) => {
                let result = d[prop]
                let tmp = ""
                if (direct_prop.startsWith(":")) {
                    let mapping = direct_prop.split(":")
                    let depth = mapping.length
                    global_result = 0
                    local_opacity = 1
                    let i = 0
                    _.forEach(d[prop], function (e) {
                        // If we have the good object index match (i.e. BC #i)
                        if (`${i}` == mapping[1]){
                            let de = 1
                            let f = e
                            while (de < depth-1){
                                if (f.hasOwnProperty(mapping[de])){
                                    f = f[mapping[de]]
                                }
                                de += 1
                            }
                            if (f.hasOwnProperty(mapping[de])){
                                result = f[mapping[de]]
                                global_result = 1
                            }
                        }
                        i += 1
                    })
                    if (global_result == 0){
                        result = ""
                        global_result = me.nope
                        local_opacity = 0
                    }
                } else if (direct_value != '') {
                    _.forEach(d[prop], function (e) {
                        if (e[direct_prop] == direct_value) {
                            result = `${e['value']}`
                            if (""+parseInt(result) == result){
                                result = `${e['value']}`
                                stroke_width = "0.125pt"
                                if (parseInt(result) >= 5){
                                    result = "("+result+")"
                                }else if (parseInt(result) >= 3){
                                    result += "*"
                                }
                            }
                        }
                    })
                }
                return result
            })
            .attr("opacity",local_opacity)
            .style('stroke-width', stroke_width)
        return global_result
    }



    sheetEntryQuadA(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, 0+0.125, me.part-0.125)
    }

    sheetEntryQuadB(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, me.part+0.125, me.part*2-0.125)
    }

    sheetEntryQuadC(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, me.part*2+0.125, me.part*3-0.125)
    }

    sheetEntryQuadD(func, y, ox = 0, oy = 0, proplabel, prop = '', font_size = 0, direct_prop = '', direct_value = '') {
        let me = this
        me.baseSheetEntry(func, y, ox, oy, proplabel, prop, font_size, direct_prop, direct_value, me.part*3+0.125, me.part*4-0.125)
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
//         console.log('FICS_SHEET: Performing...');
        if (character_data) {
            //me.data = character_data;
            me.sets = Array()
            me.data = Array()
            let nb_chars = 0
            _.forEach(character_data, function (e, k) {
                let x = JSON.parse(e)
                x['idx'] = x['idx'] % 5
                me.data.push(x);
                nb_chars += 1
                if (nb_chars % 5 == 0){
//                     console.warn(me.data)
                    me.sets.push(me.data)
                    me.data = Array()
                }
            })
            me.sets.push(me.data)
            me.pages_number = Math.ceil(nb_chars/5)
//             console.log("Pages Number:",me.pages_number," (",nb_chars," characters)")
        }

        $(me.parent).css('display', 'block');
        me.rid = me.adventure.full_id
        me.page = page
        me.data = me.sets[me.page]
//         console.log(me.page,"/",me.pages_number)
        me.drawWatermark(me.page)
        me.drawGeneric(1.5, 1.5)
        me.drawPages(9, 1.5)
        me.drawFigures(7.8, 1.5)
        me.drawButtons()
        me.zoomActivate()
    }
}


