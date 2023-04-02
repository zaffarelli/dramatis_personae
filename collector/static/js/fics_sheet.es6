class FICSSheet extends Sheet {
    constructor(data, parent, collector) {
        super(data, parent, collector)
        console.debug("FICS Sheet");
        this.init()
    }

    init() {
        let me = this;
        super.init();
        me.version = '0.9.6';
        me.fics_release = "FuZion Interlock Custom System v8.0";
    }

    drawButtons() {
        let me = this;
        me.setButtonsOrigin(27, 1);
        me.addButton(0, 'Save SVG', '');
        me.addButton(1, 'Page 1', 'browse');
        me.addButton(2, 'Page 2', 'browse');
        me.addButton(3, 'Page 3', 'browse');
        me.addButton(4, 'Page 4', 'browse');
        me.addButton(5, 'Create PDF', '');
    }


    drawPages(page = 0) {
        super.drawPages(page);
        let me = this;
        if (page === 0) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            me.drawLine(1, 1, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(23, 23, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 2.5, 2.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);

            // Skills
            me.drawLine(1, 23, 12.25, 12.25, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            // Specialities
            me.drawLine(1, 23, 18.75, 18.75, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.drawLine(1, 23, 22, 22, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.drawLine(1, 23, 25, 25, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            let title_text = 'Fading Suns'.toUpperCase();
            me.decorationText(12, 3.82, 0, 'middle', me.title_font, me.fat_font_size * 1.35, '#FFF', '#FFF', 25, title_text, me.back, 1.0);
            me.drawJumpgateLogo(12 * me.stepx, 2.6 * me.stepy)
            me.decorationText(12, 3.82, 0, 'middle', me.title_font, me.fat_font_size * 1.35, me.draw_fill, me.draw_stroke, 1, title_text, me.back, 1);
            me.decorationText(12, 4.8, 0, 'middle', me.title_font, 3 * me.fat_font_size / 5, me.draw_fill, me.draw_stroke, 0.5, me.scenario, me.back, 0.8);
            // me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.back);
            me.decorationText(20, 2.25, 0, 'middle', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.pre_title, me.back);
            me.decorationText(22.5, 35.65, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "Fading Suns FICS character sheet version " + me.version + " - 2021 - Zaffarelli - generated with dP", me.back);

            me.drawLine(8.5, 8.5, 25, 35, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(13.5, 13.5, 25, 35, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.drawLine(8.5, 13.5, 28.5, 28.5, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(8.5, 13.5, 33, 33, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.fics_release, me.back);


        } else if (page === 1) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(23, 23, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 2.5, 2.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);


            me.drawLine(1, 17, 5, 5, me.draw_fill, me.draw_fill, 3, me.strokedebris); // Weapons/Armors separator
            me.drawLine(1, 17, 10, 10, me.draw_fill, me.draw_fill, 3, me.strokedebris); // Below weapons
            me.drawLine(17, 23, 8, 8, me.draw_fill, me.draw_fill, 3, me.strokedebris); // Below tods
            // me.drawLine(12, 12, 10, 35, me.draw_fill, me.draw_fill, 3); // East BA/BC
            me.drawLine(1, 12, 29, 29, me.draw_fill, me.draw_fill, 3); // Below shortcuts
            me.drawLine(17, 17, 2.5, 13, me.draw_fill, me.draw_fill, 3, me.strokedebris); // Right Armor/weapons

            me.drawLine(1, 23, 13, 13, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(1, 23, 20, 20, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.fics_release, me.back);
            me.decorationText(22.5, 35.8, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "fics_Sheet v" + me.version + ", 2021, Zaffarelli, generated with DP", me.back);

        } else if (page === 2) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(23, 23, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 2.5, 2.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);

            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.fics_release, me.back);
            me.decorationText(22.5, 35.8, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "fics_Sheet | v" + me.version + " | 2022 | Zaffarelli | generated with DP", me.back);

            me.drawLine(1, 23, 11, 11, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(1, 23, 14, 14, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(1, 23, 26, 26, me.draw_fill, me.draw_fill, 3, me.strokedebris);

        } else if (page === 3) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(23, 23, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 2.5, 2.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);

            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.fics_release, me.back);
            me.decorationText(22.5, 35.8, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "fics_Sheet | v" + me.version + " | 2022 | Zaffarelli | generated with DP", me.back);

            me.drawLine(12, 12, 2.5, 35, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(12, 23, 10, 10, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(12, 23, 24, 24, me.draw_fill, me.draw_fill, 3, me.strokedebris);
        }

        if (!me.blank) {
            me.decorationText(1.15, 35.8, -16, 'start', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "[" + me.data['date'] + "] [" + me.data['rid'] + '] (p'+page+') [' + me.data['id'] + ']', me.back);
        }

        // Sheet content
        me.character = me.back.append('g')
            .attr('class', 'fics_sheet');
    }

    fillName(page){
        let me = this;
        me.drawText(1, 2, me.draw_fill, me.draw_stroke, me.medium_font_size, "middle", ""+(page+1)+"/4", 1.0, me.draw_font);
        if (!me.blank) {
            me.drawText(23, 2, me.user_fill, me.user_stroke, me.medium_font_size, "end", me.data['full_name'].toUpperCase(), 1.0, me.user_font);
        }
    }

    fillCharacter(page = 0) {
        let me = this;
        if (page == 0) {
            me.fillBasics(3 * me.stepy);
            me.fillAttributes(5 * me.stepy);
            me.fillSkills(13.0 * me.stepy);
            me.fillExtras(25);
        } else if (page == 1) {
            me.fillName(page);
            me.fillArmors(1.25, 3);
            me.fillWeapons(1.25, 5.5);
            me.fillShield(1.25, 10.5);
            me.fillCyber(1.25, 13.5);
            me.fillPicture(1.25, 29.5);
        } else if (page == 2) {
            me.fillName(page);
            me.fillToDs(1.25, 3);
            me.fillBC(1.25, 11.5);
            me.fillBA(1.25, 14.5);
            me.fillOccult(1.25, 26.5)

        } else if (page == 3) {
            me.fillName(page);
            me.fillWallet(12.25, 3)
            me.fillGear(12.25, 10.5)
            me.fillShortcuts(1.25, 3)
            me.fillExperience(12.25, 24.5)
        }
    }

    perform(character_data = null, page = 0) {
        super.perform(character_data, page);
        let me = this;
        console.log('FICS_SHEET: Performing...');
        if (character_data) {
            me.data = character_data;
            // console.debug(me.data);
        }
        me.guideline = me.data['guideline'];
        $(me.parent).css('display', 'block');
        me.drawWatermark(page);
        if (me.data['condition'] == "DEAD") {
            me.decorationText(12, 16, 0, 'middle', me.logo_font, me.fat_font_size * 3, me.shadow_fill, me.shadow_stroke, 0.5, "DEAD", me.back, 0.25);
        }
        me.fillCharacter(page);
        me.drawButtons();
        me.zoomActivate();
        me.createPDF();
    }
}


