class FICSSheet extends Sheet {
    constructor(data, parent, collector) {
        super(data, parent, collector)
        console.debug("FICS Sheet");
        this.init()
    }

    init() {
        let me = this;
        super.init();
        me.version = '0.9.4'
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
        me.bottom_disclaimer = "Fading Suns FICS character sheet version " + me.version + " - 2024 - Zaffarelli - generated with dP"
        if (page === 0) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            me.drawLine(1, 1, 0.8, 35.2, me.draw_fill, me.draw_fill, 6, "");
            me.drawLine(23, 23, 0.8, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 1, 1, me.draw_fill, me.draw_fill, 6, "");
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);

            me.drawLine(1, 23, 12.25, 12.25, me.draw_fill, me.draw_fill, 6, me.strokedebris);


            me.drawLine(10, 10, 12.25, 25, me.draw_fill, me.draw_fill, 3, me.strokedebris) // West of Skills
            me.drawLine(10, 23, 18, 18, me.draw_fill, me.draw_fill, 3, me.strokedebris) // Below Skills

            //me.drawLine(1, 23, 22, 22, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.drawLine(1, 23, 25, 25, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            let title_text1 = 'Fading'.toUpperCase();
            let title_text2 = 'Suns'.toUpperCase();


            me.decorationText(8, 3.25, 0, 'start', me.title_font, me.fat_font_size * 1.35, '#FFF', '#FFF', 20, title_text1, me.back, 1.0);
            me.decorationText(16, 3.25, 0, 'end', me.title_font, me.fat_font_size * 1.35, '#FFF', '#FFF', 20, title_text2, me.back, 1.0);
            //me.drawJumpgateLogo(12 * me.stepx, 2.6 * me.stepy)
            me.decorationText(8, 3.25, 0, 'start', me.title_font, me.fat_font_size * 1.35, me.shadow_fill+"7f", me.shadow_stroke, 1, title_text1, me.back, 1);
            me.decorationText(16, 3.25, 0, 'end', me.title_font, me.fat_font_size * 1.35, "#2020207f", "#202020", 1, title_text2, me.back, 1);

            //me.decorationText(12, 3.8, 0, 'middle', , me.fat_font_size * 1.35, me.draw_fill, me.draw_stroke, 1, title_text2, me.back, 1);

            let a = 9.35*me.stepx
            let b = 0.25*me.stepy
            me.back.append("path")
                //.style("fill-opacity",0.25)
//                 .attr("x",a)
//                 .attr("y",b)
                .style("fill","#E080E07F")
                .style("stroke","#3010307f")
                .style("stroke-width","0.5pt")
                .attr("transform","translate("+a+","+b+") scale(2)")
                .attr("d", " m 109.953,58.852051 q -0.3048,0.508 -1.1176,1.7272 -0.8128,1.1684 -0.8128,1.6764 0,0.6604 0.508,1.0668 0.508,0.4064 1.4224,0.4064 0.4064,-0.254 0.762,-0.508 0.3556,-0.254 0.5588,-0.6096 0.2032,-0.4064 0.3048,-0.4064 0,0.3048 0.0508,0.6096 -0.0508,0.7112 -0.2032,0.9652 -0.5588,0.4064 -1.2192,0.9144 -0.6604,0.4572 -0.6604,1.0668 0,0.3556 0.1524,0.5588 0.1524,0.1524 0.3556,0.3048 0.254,0.1524 0.2032,0.3048 -0.1524,-0.0508 -0.2032,0.2032 -0.0508,0.2032 0,0.3556 0,0.4572 0.6604,1.0668 0.7112,0.6096 0.6604,0.8128 -0.3556,0.1016 -0.508,0.1524 -0.1016,0 -0.2032,0.0508 0.5588,0.6096 1.5748,1.1684 1.0668,0.508 1.8288,0.508 2.286,0 3.81,-0.6604 1.524,-0.6604 1.8288,-2.6924 0.1524,-0.9144 -0.8636,-2.6924 -1.016,-1.778 -1.016,-2.3368 0,-0.3556 0.1524,-0.8128 0.1016,-0.7112 0.4572,-1.016 0.3556,-0.3556 1.016,-0.6604 0.7112,-0.3048 0.9652,-0.3048 0.3048,0 0.4064,0.3048 -0.1524,-0.0508 -0.4572,0.254 -0.254,0.254 -0.254,0.6604 -0.1524,0.9144 0.7112,1.4224 0.8636,0.4572 1.9304,0.4572 l -0.0508,-0.3556 q 0.0508,-0.3556 0.3556,-0.3556 0.1524,0 0.5588,0.3556 0.4064,0.3556 0.8128,0.7112 1.8288,0.9652 6.604,1.4732 4.7752,0.4572 11.1252,0.6604 6.35,0.1524 11.3284,0.1524 h 5.2832 q 1.6256,0 5.334,-0.254 3.7084,-0.3048 4.7244,-0.3048 4.4196,0.7112 8.4836,1.27 4.064,0.5588 7.112,0.5588 -0.9652,0.1524 -2.032,0.2032 -1.016,0.0508 -2.286,0.0508 -2.1844,0 -6.1976,-0.2032 -4.0132,-0.254 -4.572,-0.254 -1.1684,0 -2.6924,0.762 -1.4732,0.7112 -1.4732,1.27 0,0.508 1.5748,0.508 5.1816,0 8.0772,0.3556 2.8956,0.3048 5.6388,1.9304 0.4572,0.1524 0.762,0.3048 0.3556,0.1524 0.4064,0.4064 -2.4892,-0.3556 -5.1308,-0.762 -2.6416,-0.4064 -4.572,-0.4064 -1.4224,0 -2.6924,0.2032 -1.27,0.1524 -2.6924,0.5588 0,0.4572 1.1176,1.016 1.1176,0.5588 1.1176,1.1176 -2.6924,-0.762 -4.5212,-1.1684 -1.778,-0.4064 -3.7084,-0.4064 -0.8128,0 -1.6256,0.1524 -0.762,0.1016 -0.762,0.3048 0,0.1524 1.1684,0.3556 1.1684,0.1524 2.8956,0.8128 1.7272,0.6604 2.54,1.016 0.8128,0.3048 3.3528,0.4572 2.54,0.1016 2.794,0.8636 -1.27,0.3048 -8.2296,1.117599 -6.9596,0.8128 -6.9596,1.8796 0,0.3048 0.6096,0.9144 0.6096,0.5588 4.3688,1.6764 3.81,1.0668 4.8768,3.2512 l 0.254,0.0508 q -0.508,0 -1.4732,-0.254 -0.9144,-0.3048 -1.6256,-0.508 -0.6604,-0.2032 -2.3368,-0.3048 -1.6256,-0.1016 -3.1496,-0.1016 h -0.8636 q -1.7272,0 -4.3688,0.1524 -2.5908,0.1016 -2.9464,0.1016 -0.9144,0 -1.8796,-0.0508 -0.9144,-0.0508 -1.8288,-0.2032 -0.8636,-0.2032 -1.8796,-0.4572 -0.9652,-0.3048 -1.7272,-0.3048 -1.2192,0 -1.7272,0.762 -0.4572,0.6604 0.9652,1.4224 1.6764,0.7112 3.4036,1.3716 -0.2032,0 -0.762,0 -0.508,-0.0508 -2.6416,-0.3556 -1.7272,-0.4572 -2.54,-0.6604 -0.8128,-0.2032 -1.6256,-0.4572 -0.2032,0.254 -0.2032,0.6096 0,0.7112 0.9652,1.6256 1.016,0.8636 1.6256,1.016 0,-0.1524 0.0508,-0.3048 0.0508,-0.1524 0.1524,-0.3556 0.508,0.3048 1.4732,0.6096 0.9652,0.254 1.6256,0.3556 0.7112,0.0508 1.1176,0.1016 0.4572,0 0.762,0 0.5588,0 1.7272,-0.0508 1.2192,-0.0508 1.778,-0.0508 -0.1016,0.6096 -3.5052,1.27 -3.3528,0.6096 -4.572,0.6096 -2.8448,0 -4.572,-0.4572 -1.6764,-0.4572 -2.1844,-1.778 -0.508,-1.3716 -0.762,-1.778 -0.254,-0.4064 -0.5588,-0.3048 -0.6096,0.2032 -0.6096,0.9652 0,0.5588 0.3048,1.3208 0.3048,0.762 0.508,1.1684 0.0508,0.5588 -0.1016,1.7272 -0.1016,1.1684 -0.508,1.1684 -0.9652,-1.9304 -4.7752,-2.9464 -3.81,-1.0668 -4.064,-1.9304 0.0508,-0.1016 1.4224,0.3048 1.3716,0.3556 1.9812,0.3556 0.762,0 0.762,-0.4064 -0.2032,-0.9652 -2.794,-2.5908 -2.54,-1.6256 -3.556,-1.9812 -1.016,-0.4064 -2.3368,-0.4064 -0.9144,0 -1.524,0.2032 -0.5588,0.1524 -0.6604,0.6096 -0.3556,0.6096 0.3048,1.524 0.7112,0.9144 1.1684,1.6256 0.508,0.7112 1.27,2.4892 0.762,1.778 0.762,3.048 -0.9652,-0.4064 -1.8288,-0.7112 -0.8128,-0.3048 -1.1176,-0.3048 -0.3048,0 -0.4572,0.2032 -0.1524,0.3048 0.1016,1.1176 0.254,0.762 0.4572,1.4224 0.254,0.6604 0.254,1.6764 0,0.3556 -0.0508,0.508 -0.6096,-1.1684 -1.27,-1.7272 -0.6604,-0.5588 -1.6764,-0.5588 -0.6604,-0.1016 -1.3208,1.1684 -0.6604,1.2192 -1.1684,2.286 -0.3556,0.3556 -0.7112,0.762 -0.3048,0.4064 -0.5588,0.7112 l -0.1016,-0.2032 q -0.6604,-1.7272 -1.0668,-2.1844 -0.3556,-0.4572 -1.7272,-1.1684 -0.254,-0.254 -0.762,-0.254 -0.762,0 -0.9144,0.4064 -0.1524,0.1524 -0.254,0.6604 -0.1016,0.508 -0.1016,1.4224 -1.2192,0 -1.9812,-1.8288 -0.7112,-1.8288 -1.2192,-3.6576 -0.254,-0.2032 -0.7112,-0.2032 -0.762,0 -1.0668,0.9652 -0.304799,0.9144 -0.304799,2.0828 -0.3556,0 -0.6096,-0.9144 -0.254,-0.9652 -0.254,-2.0828 0,-1.3208 0.4572,-1.8796 0.4064,-0.6604 0.4064,-0.8128 -0.3556,-0.5588 -0.8636,-0.5588 -0.4064,0 -0.8128,0.4064 -0.4064,0.3556 -0.9144,0.9652 0.254,-2.2352 1.4732,-3.7592 0.5588,-0.3556 0.9652,-0.6604 0.4064,-0.3048 0.558799,-0.8128 0.1016,-0.8128 -0.812799,-1.1176 -0.8636,-0.3556 -2.286,-0.3556 -2.1336,0 -2.9464,0.4572 -1.0668,0.4572 -2.3876,1.27 -1.3208,0.762 -1.3208,2.1336 1.016,0.762 2.4892,0.762 0.5588,0 1.016,-0.1524 -0.0508,0.3048 -0.4064,0.7112 -0.3556,0.4064 -0.9144,0.6604 -0.508,0.254 -1.27,0.254 -0.5588,0 -1.1684,-0.1016 -0.6096,-0.1016 -1.8288,-0.254 -1.1684,-0.1524 -2.4384,-0.1524 -0.7112,0 -1.4224,0 -0.762,0.1524 -1.4732,0.254 -0.6604,0.1016 -1.4224,0.8128 -0.7112,0.6604 -1.3716,1.3716 0.4572,-2.3876 3.9624,-3.6576 3.5052,-1.27 3.3528,-1.8288 -0.2032,-0.6604 -1.0668,-0.9144 -0.8128,-0.3048 -2.1844,-0.3048 -1.6764,0 -3.1496,0.3048 -1.4732,0.254 -2.3876,0.5588 -0.7112,0.508 -0.8128,0.9652 0.762,0.3048 1.27,0.4572 0.508,0.1016 1.2192,0.1016 0,0.1016 0.0508,0.1524 -0.4572,0.2032 -1.016,0.6604 -0.508,0.4572 -1.1684,0.9652 -0.6604,0.508 -1.524,1.1176 -0.8636,0.6096 -1.7272,1.0668 -0.8636,0.4064 -1.3208,0.5588 -0.2032,0 -0.3556,0 0,-0.0508 0.6604,-1.016 0.6604,-1.016 0.5588,-1.6256 -0.0508,-0.508 -0.6604,-0.508 -0.3048,0 -0.508,0.1016 l -3.556,0.3556 q -2.1336,0 -4.5212,1.2192 -2.3368,1.1684 -2.286,1.4732 1.3716,-2.032 3.3528,-3.3528 1.9812,-1.3716 4.0132,-2.6924 0.5588,-0.5588 0.4064,-1.1684 -0.1016,-0.4572 -1.27,-0.7112 -1.1176,-0.254 -2.6416,-0.254 -1.6764,0 -2.794,0.2032 -1.0668,0.1524 -1.778,0.6604 -0.6604,0.4572 -0.6604,0.8128 0,0.4064 1.1684,0.8128 1.2192,0.3556 1.1684,0.5588 l -2.032,0.762 h -2.4384 q -1.524,0 -3.81,-0.0508 -2.286,-0.1016 -2.3368,-0.1016 -1.625599,0 -2.997199,0.1016 -1.3208,0.1016 -2.3876,0.4064 -1.016,0.254 -1.6256,0.4064 0,-1.4732 2.6924,-2.9972 2.6924,-1.5748 5.537199,-3.2004 0,-0.4572 -0.7112,-0.7112 -0.7112,-0.254 -2.082799,-0.254 -0.8128,0 -1.778,-0.0508 -0.9144,-0.0508 -1.778,-0.1016 -2.6924,0 -4.3688,0.6096 -1.6764,0.6096 -1.6764,2.3876 h -0.254 q 0.254,-2.7432 2.8448,-3.9116 2.6416,-1.2192 4.9784,-2.286 0.4064,-0.507999 0.508,-0.660399 0,-0.1016 0,-0.254 v -0.254 q -0.3048,0.0508 -1.27,0.3556 -0.9144,0.3048 -1.6764,0.507999 -0.762,0.2032 -1.2192,0.3048 -0.4572,0.1016 -1.016,0.1016 -0.508,0 -1.524,-0.1524 -1.016,-0.1524 -1.5748,-0.1524 -0.4064,0 -0.6096,0 h -0.508 q -0.5588,0.2032 -1.1176,0.3556 0,-1.320799 -0.762,-1.879599 -0.7112,-0.6096 -2.032,-0.6096 -1.4732,0 -2.8956,0.4572 -1.4224,0.4064 -3.9116,1.3208 0,-1.2192 3.7592,-2.8956 3.81,-1.6764 7.6708,-3.1496 -0.508,0.5588 -0.508,1.016 0,0.4572 0.508,0.7112 0.5588,0.254 1.3716,0.254 1.524,0 2.8448,-0.762 1.3208,-0.762 1.1176,-1.9812 -0.2032,-1.1176 -2.3368,-1.6256 -2.1336,-0.508 -5.5372,-0.508 -3.7084,0 -7.6708,0.508 -3.9624,0.4572 -5.7912,1.0668 1.778,-1.8796 6.858,-2.5908 5.08,-0.762 12.5476,-0.762 4.0132,0 10.972799,0.2032 7.0104,0.1524 8.5344,0.1524 6.2992,0 9.5504,-0.5588 3.2512,-0.6096 3.2512,-2.2352 0,-0.2032 -0.1016,-0.6096 -0.4064,-0.254 -0.762,-0.5588 5.1816,-1.2192 10.3632,-2.4384 2.6416,0 4.4704,1.1176 0.3556,0.3556 0.8636,0.8636 0.5588,0.508 0.8128,0.508 0.1524,0 0.1524,-0.254 0,-0.254 -0.1524,-0.762 l -0.3048,-0.7112 q 0.2032,-0.254 0.5588,-0.0508 0.3556,0.1524 0.7112,0.5588 0.4064,0.4064 0.5588,1.1684 0.2032,0.762 0.2032,1.8796 0,1.1176 0.0508,1.8796 0.1016,0.762 0.3556,1.3716 0.4572,1.4224 1.524,2.1336 1.1176,0.6604 2.4384,0.6604 0.8636,0 2.285999,-0.4064 1.4224,-0.4572 2.2352,-0.9144 0.8128,-0.4572 1.4224,-2.286 0.1524,-0.3048 0.1524,-0.6096 0,-0.9652 -0.8636,-0.9652 -0.254,0 -0.5588,0.1524 -0.2032,0.2032 -0.3556,0.3556 l -0.2032,-0.0508 q -0.1524,-0.3048 -0.1524,-0.9144 0,-0.3048 0.1524,-0.5588 0.1524,-0.4572 0.5588,-0.7112 0.4572,-0.3048 0.9144,-0.6096 l 1.524,-1.7272 q 0.762,-0.8128 1.8288,-1.6764 1.1176,-0.9144 1.9304,-1.3208 z m -3.9624,5.1308 q -0.254,0.2032 -0.3556,0.3556 -0.0508,0.1016 -0.0508,0.1524 0.508,0.1016 0.7112,0 0.1016,-0.0508 0.1016,-0.2032 0.0508,-0.1524 0.1016,-0.3048 -0.4064,-0.1016 -0.5588,-0.0508 z m 8.2296,26.466799 1.1684,0.5588 v -2.032 -2.0828 l -1.1684,0.5588 q -0.4572,-1.524 -1.4732,-2.54 -0.9652,-1.0668 -2.4384,-1.4224 l 0.5588,-1.1176 h -2.0828 -2.0828 l 0.5588,1.1176 q -3.048,0.8128 -3.7592,4.1656 l -1.3208,-0.762 v 2.0828 2.032 l 1.3208,-0.5588 q 0.5588,3.1496 3.7592,4.1656 l -0.5588,0.9144 h 2.0828 2.0828 l -0.4064,-0.9144 z m -4.4704,2.6416 -0.9652,-1.6764 -0.9652,1.6764 q -1.1176,-0.2032 -1.9812,-1.1176 -0.8128,-0.9652 -1.016,-2.286 l 1.524,-0.7112 -1.4732,-0.762 q 0.508,-2.6416 3.1496,-3.4036 l 0.762,1.6764 0.762,-1.7272 q 1.27,0.3048 2.1336,1.2192 0.8636,0.9144 1.0668,2.2352 l -1.524,0.762 1.7272,0.7112 q -0.3048,1.3716 -1.1684,2.286 -0.8636,0.9144 -2.032,1.1176 z")



            me.decorationText(12, 3.5, 0, 'middle', "Syne Mono", me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.back, 0.8);
            me.decorationText(12.0, 3.75, 0, 'middle', "Syne Mono", me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.pre_title, me.back);
            //me.decorationText(4.2, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.scenario, me.back);
            me.decorationText(22.5, 35.65, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.bottom_disclaimer, me.back);

            me.drawLine(8.5, 8.5, 25, 35, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(13.5, 13.5, 25, 35, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.drawLine(8.5, 13.5, 28.5, 28.5, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(8.5, 13.5, 33, 33, me.draw_fill, me.draw_fill, 3, me.strokedebris);


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
            me.drawLine(12, 12, 10, 35, me.draw_fill, me.draw_fill, 3); // East BA/BC
            me.drawLine(1, 12, 29, 29, me.draw_fill, me.draw_fill, 3); // Below shortcuts
            me.drawLine(17, 17, 2.5, 13, me.draw_fill, me.draw_fill, 3, me.strokedebris); // Right Armor/weapons

            me.drawLine(1, 23, 13, 13, me.draw_fill, me.draw_fill, 3, me.strokedebris);
            me.drawLine(1, 23, 20, 20, me.draw_fill, me.draw_fill, 3, me.strokedebris);

            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.back);
            me.decorationText(22.5, 35.8, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.bottom_disclaimer, me.back);

        } else if (page === 2) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(23, 23, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 2.5, 2.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);

            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.back);
            me.decorationText(22.5, 35.8, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.bottom_disclaimer, me.back);

        } else if (page === 3) {
            me.lines = me.back.append('g');
            me.daddy = me.lines;
            // External lines
            me.drawLine(1, 1, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(23, 23, 2.3, 35.2, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 2.5, 2.5, me.draw_fill, me.draw_fill, 6, me.strokedebris);
            me.drawLine(0.8, 23.2, 35, 35, me.draw_fill, me.draw_fill, 6, me.strokedebris);

            me.decorationText(4.0, 2.25, 0, 'middle', me.base_font, me.medium_font_size, me.draw_fill, me.draw_stroke, 0.5, me.post_title, me.back);
            me.decorationText(22.5, 35.8, -16, 'end', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, me.bottom_disclaimer, me.back);

        }

        if (!me.blank) {
            me.decorationText(1.15, 35.8, -16, 'start', me.base_font, me.small_font_size, me.draw_fill, me.draw_stroke, 0.5, "[" + me.data['date'] + "] [" + me.data['rid'] + '] (p'+page+') [' + me.data['id'] + ']', me.back);
        }

        // Sheet content
        me.character = me.front.append('g')
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
            me.fillBasics(1.5 * me.stepy);
            me.fillAttributes(4.5 * me.stepy);
            me.fillSkills(13.0 * me.stepy);
            me.fillExtras(25);
        } else if (page == 1) {
            me.fillName(page);
            me.fillArmors(1.25, 3);
            me.fillWeapons(1.25, 5.5);


            me.fillShield(12.25, 10.5)
            me.fillPicture(1.25, 29.5)
        } else if (page == 2) {
            me.fillName(page);
            me.fillToDs(1.25, 3);
            me.fillBC(1.25, 11.5);
            me.fillBA(1.25, 14.5);
            me.fillOccult(1.25, 24.5)

        } else if (page == 3) {
            me.fillName(page);
            me.fillWallet(17.25, 8.5)
            me.fillGear(12.25, 20.5)
            me.fillShortcuts(1.25, 20.5)
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
        me.drawWatermark(page)
        me.drawPages(page)
        if (me.data['condition'] == "DEAD") {
            me.decorationText(12, 16, 0, 'middle', me.logo_font, me.fat_font_size * 3, me.shadow_fill, me.shadow_stroke, 0.5, "DEAD", me.back, 0.25);
        }

        //me.fillCharacter(page);
        me.drawButtons();
        me.zoomActivate();
    }
}


