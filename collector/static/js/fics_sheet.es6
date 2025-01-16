class FICSSheet extends Sheet {
    constructor(data, parent, collector) {
        super(data, parent, collector)
//         console.debug("FICS Sheet");
        this.init()
    }

    init() {
        let me = this;
        super.init();
        //me.version = '0.9.4'
        me.bottom_disclaimer = "Fading Suns FICS " + me.version + " character sheet - 2025 - Zaffarelli - generated with dP "
    }

    drawButtons() {
        let me = this;
        me.setButtonsOrigin(27, 1);
        me.addButton(0, 'Save SVG', '');
        me.addButton(1, 'Page 1', 'browse');
        me.addButton(2, 'Page 2', 'browse');
        me.addButton(3, 'Page 3', 'browse');
        me.addButton(4, 'Page 4', 'browse');
    }


    drawPages(page = 0) {
        super.drawPages(page);
        let me = this;

        if (page === 0) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            me.drawLine(1, 1, 0.8, 33.2, me.draw_fill, me.draw_fill, 6)
            me.drawLine(23, 23, 0.8, 33.2, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 1, 1, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 33, 33, me.draw_fill, me.draw_fill, 6)

            me.drawLine(1, 23, 11.25, 11.25, me.draw_fill, me.draw_fill, 6)


            //me.drawLine(9.75, 9.75, 11.25, 18, me.draw_fill, me.draw_fill, 6, me.strokedebris) // West of Skills
            //me.drawLine(10, 23, 17, 17, me.draw_fill, me.draw_fill, 3, me.strokedebris) // Below Skills
            //me.drawLine(1, 23, 18.25, 18.25, me.draw_fill, me.draw_fill, 6, me.strokedebris) // Below Attributes / Skills
            //me.drawLine(1, 23, 23, 23, me.draw_fill, me.draw_fill, 6, me.strokedebris) // Below Degrees

//             let a = 9.35*me.step
//             let b = 0.25*me.step

            //me.drawLine(8.5, 8.5, 23, 33, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            //me.drawLine(13.5, 13.5, 23, 33, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            //me.drawLine(8.5, 13.5, 26.5, 26.5, me.draw_fill, me.draw_fill, 3, me.strokedebris) // Between Sanity and Glamour
            //me.drawLine(8.5, 13.5, 31, 31, me.draw_fill, me.draw_fill, 3, me.strokedebris) // Between Glamour and Wyrd


        } else if (page === 1) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 0.8, 33.2, me.draw_fill, me.draw_fill, 6);
            me.drawLine(23, 23, 0.8, 33.2, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 1, 1, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 33, 33, me.draw_fill, me.draw_fill, 6)


            me.drawLine(1, 17, 5, 5, me.draw_fill, me.draw_fill, 3) // Weapons/Armors separator
            me.drawLine(1, 17, 10, 10, me.draw_fill, me.draw_fill, 3) // Below weapons
            me.drawLine(17, 23, 8, 8, me.draw_fill, me.draw_fill, 3) // Shields / Sanity
            me.drawLine(17, 17, 1, 33, me.draw_fill, me.draw_fill, 3); // Right Armor/weapons
            me.drawLine(17, 23, 18, 18, me.draw_fill, me.draw_fill, 3) // Wyrd / Money
            me.drawLine(1, 17, 21.5, 21.5, me.draw_fill, me.draw_fill, 3) // Health / Cyberware



        } else if (page === 2) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 0.8, 33.2, me.draw_fill, me.draw_fill, 6);
            me.drawLine(23, 23, 0.8, 33.2, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 1, 1, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 33, 33, me.draw_fill, me.draw_fill, 6)



        } else if (page === 3) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 0.8, 33.2, me.draw_fill, me.draw_fill, 6);
            me.drawLine(23, 23, 0.8, 33.2, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 1, 1, me.draw_fill, me.draw_fill, 6)
            me.drawLine(0.8, 23.2, 33, 33, me.draw_fill, me.draw_fill, 6)


            me.daddy = me.front;
            me.drawRect( 1.5, 1.5, 21, 21,"white", me.draw_fill, 1)
            me.writeText({"x":2,"y": 3, "size": me.small_font_size/me.step, "text":"Small font size"})
            me.writeText({"x":2,"y": 4, "size": me.medium_font_size/me.step, "text":"Medium font size"})
            me.writeText({"x":2,"y": 5, "size": me.big_font_size/me.step, "text":"Big font size"})
            me.writeText({"x":2,"y": 6, "size": me.large_font_size/me.step, "text":"Large font size"})
            me.writeText({"x":2,"y": 8, "size": me.fat_font_size/me.step, "text":"FADING SUNS fat font size", "font":me.title_font})

            me.writeText({"x":12,"y": 3, "size": me.small_font_size/me.step, "text":"Small font size", "font":me.user_font})
            me.writeText({"x":12,"y": 4, "size": me.medium_font_size/me.step, "text":"Medium font size", "font":me.user_font})
            me.writeText({"x":12,"y": 5, "size": me.big_font_size/me.step, "text":"Big font size", "font":me.user_font})
            me.writeText({"x":12,"y": 6, "size": me.large_font_size/me.step, "text":"Large font size", "font":me.user_font})



        }

        // Texts
        if (me.page != 0){
            me.decorationText(2.0, 0.85, 0, 'start', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.front);
        }
        me.decorationText(22.85, 33.5, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.bottom_disclaimer, me.front);

        if (!me.blank) {
            me.decorationText(1.15, 33.5, -16, 'start', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "[" + me.data['date'] + "] [" + me.data['rid'] + '] (p'+page+') [' + me.data['id'] + ']', me.front);
        }

        // Sheet content
        me.character = me.front.append('g')
            .attr('class', 'fics_sheet');
    }


    fillTitle(){
        let me = this
        me.daddy = me.front
        let title_text1 = 'Fading'.toUpperCase();
        let title_text2 = 'Suns'.toUpperCase();
        me.decorationText(7.5, 3.25, 0, 'start', me.title_font, me.fat_font_size * 1.35, "FFFFFFCF", "FFFFFFCF", 20, title_text1, me.front, 1.0);
        me.decorationText(16.5, 3.25, 0, 'end', me.title_font, me.fat_font_size * 1.35, "FFFFFFCF", "FFFFFFCF", 20, title_text2, me.front, 1.0);
        //me.drawJumpgateLogo(12 * me.step, 2.6 * me.step)
        me.decorationText(7.5, 3.25, 0, 'start', me.title_font, me.fat_font_size * 1.35, me.shadow_fill+"7f", me.shadow_stroke, 1, title_text1, me.front, 1);
        me.decorationText(16.5, 3.25, 0, 'end', me.title_font, me.fat_font_size * 1.35, "#2020207f", "#202020", 1, title_text2, me.front, 1);
        me.decorationText(12, 3.5, 0, 'middle', "Syne Mono", me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.front, 0.8);
        //if (me.data.keyword.includes("SANFRANCIS")){
            me.decorationText(12.0, 4.0, 0, 'middle', "Rationale", me.big_font_size, me.draw_fill, me.draw_stroke, 0.5, me.pre_title, me.front);
        //    }else{
        //    me.decorationText(12.0, 4.0, 0, 'middle', "Rationale", me.big_font_size, me.draw_fill, me.draw_stroke, 0.5, me.pre_title, me.front);
        //}
        //me.decorationText(4.2, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.scenario, me.back);



    }

    fillName(page){
        let me = this;
        let dad = me.daddy
        me.daddy = me.front
        // Page Number
        me.drawText(1.5, 0.85, me.draw_fill, me.draw_stroke, me.medium_font_size, "middle", ""+(page+1)+"/4", 1.0, me.draw_font,me.front);
        if (!me.blank) {
            // Characters name
            me.drawText(22.85, 0.75, me.user_fill, me.user_stroke, me.medium_font_size, "end", me.data['full_name'].toUpperCase(), 1.0, me.user_font);
        }
        me.daddy = dad
    }

    fillCharacter(page = 0) {
        let me = this;
        if (page == 0) {
            me.fillTitle()
            me.fillBasics(1.5)
            me.fillLifePaths(4.5)
            me.fillAttributes(4.5)
            me.fillSkills(11.5)
            me.fillDegrees(18.75)
        } else if (page == 1) {
            me.fillName(page);
            me.fillArmors(1.25, 1.5);
            me.fillWeapons(1.25, 5.5);
            me.fillShield(17.5, 1.5)
            //me.fillPicture(1.25, 29.5)
            me.fillSanity(17, 8);
            me.fillGlamour(17, 12);
            me.fillKarma(17, 16);
            me.fillExtras(1.5,10.25)
            me.fillCyberware(1.25,22)
            me.fillWallet(17, 18)
        } else if (page == 2) {
            me.fillName(page)
            me.fillToDs(1.5, 1.5)
            me.fillBC(1.5, 16.5)
            me.fillBA(11.5, 16.5)
            me.fillOccult(1.5, 23.75)

        } else if (page == 3) {
            me.fillName(page)
            me.fillGear(12.25, 20.5)
            me.fillShortcuts(1.25, 20.5)
        }
    }

    scaledPath(path){
        let me = this
        let new_path = ""
        let sentences = path.split(" ")
        _.forEach(sentences,(s,k)=>{
            let new_sentence = s
            if (s.length>1){
                let words = s.split(",")
                let x = (words[0] == "0" ? 0.5 : (words[0] == "24" ? 23.5 : parseInt(words[0])))
                let y = (words[1] == "0" ? 0.5 : (words[1] == "36" ? 35.5 : parseInt(words[1])))
                new_sentence = `${x*me.step},${y*me.step}`
            }
            new_path += new_sentence+" "
        })
//         console.log(new_path)
        return new_path
    }



    perform(character_data = null, page = 0) {
        super.perform(character_data, page);
        let me = this;
//         console.log('FICS_SHEET: Performing...');
        if (character_data) {
            me.data = character_data;
            // console.debug(me.data);
        }
        me.guideline = me.data['guideline'];
        $(me.parent).css('display', 'block');

        me.drawWatermark(page)
        me.drawPages(page)
        me.drawDebris()
        if (me.data['condition'] == "DEAD") {
            me.decorationText(12, 16, 0, 'middle', me.logo_font, me.fat_font_size * 3, me.shadow_fill, me.shadow_stroke, 0.5, "DEAD", me.back, 0.25);
        }

        me.fillCharacter(page);
        me.drawJumpgateLogo(12*me.step,5*me.step)
        me.drawButtons();
        me.zoomActivate();
    }
}


