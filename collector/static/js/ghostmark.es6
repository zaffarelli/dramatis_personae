/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Ghostmark {
    constructor(data,oversize=0) {
        let me = this;

        me.oversize = 3;
        if (oversize !== 0){
            me.oversize = oversize;
        }
        me.init(data);
    }

    init(data) {
        let me = this;
        me.size = 6;
        me.size = me.size * me.oversize;
        me.pen = me.size / 6;
        me.width = me.size * 6;
        me.height = me.size * 6;
        me.data = data;
        me.character = data['character'];
        me.alliance = data['alliance'];
        me.svg = d3.select('#ghostmark_'+me.character['id'])
            .append('svg')
            .attr('id',me.character['rid'])
            .attr("width", me.width)
            .attr("height", me.height)
            .style("background", "transparent")
            .append('g');
        me.panel_stroke = "#888"
        me.panel_fill = "#CCC"
        me.ox = me.size*3;
        me.oy = me.size*3;
        me.mark = me.size;
    }

    createLayout(){
        let me = this;
        me.layout = me.svg.append('g')
            .attr('transform', function(d){
                let t = 'translate('+me.ox+','+me.oy+')';
                return t;
            })
        ;
        me.circ1 = me.layout.append('circle')
                .attr('cx',0)
                .attr('cy',0)
                .attr('r',me.size*2)
                .style('stroke',me.panel_stroke)
                .style('stroke-width',1)
                .style('fill','#333')
        me.circ2 = me.layout.append('circle')
                .attr('cx',0)
                .attr('cy',0)
                .attr('r',me.size*2.5)
                .style('stroke',me.panel_stroke)
                .style('stroke-width',1)
                .style('fill','transparent')

        me.rect1 = me.layout.append('rect')
                .attr('x',-2*me.size)
                .attr('y',-2*me.size)
                .attr('width',me.size*4)
                .attr('height',me.size*4)
                .style('stroke',me.panel_stroke)
                .style('stroke-width',1)
                .style('fill','transparent')
        ;

        me.rect2 = me.layout.append('rect')
                .attr('x',-2*me.size)
                .attr('y',-2*me.size)
                .attr('width',me.size*4)
                .attr('height',me.size*4)
                .style('stroke',me.panel_stroke)
                .style('stroke-width',1)
                .style('fill','transparent')
                .attr('transform',function(x){
                        let t = '';
                        t += 'rotate(45)';
                        return t;
                    })
        ;

    }

    createGhostMark(){
        let me = this;
        me.ghostmark = me.svg.append('g')
            .attr('transform', function(d){
                let t = 'translate('+me.ox+','+me.oy+')';
                return t;
            })
        ;
        me.back = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    path_str += ' M '+( -2.00*x)+','+( -2.50*x);
                    path_str += ' l '+( 1.0 *x)+" "+( 0.25*x);
                    path_str += ' c ';
                    path_str += ( 0.00*x)+' '+( 1.50*x)+',';
                    path_str += (-1.00*x)+' '+( 2.00*x)+',';
                    path_str += (-1.00*x)+' '+( 2.00*x);
                    path_str += ' Z ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width',1)
                .style('opacity','0.85')
                .style('fill',me.alliance['color_back'])
        ;
        me.front = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    path_str += ' M '+(-2.00*x)+','+( -2.50*x);
                    path_str += ' l '+(-1.0*x)+' '+( 0.25*x) ;
                    path_str += ' c ';
                    path_str += ( 0.00*x)+' '+(+1.50*x)+',';
                    path_str += ( 1.00*x)+' '+( 2.00*x)+',';
                    path_str += (+1.00*x)+' '+( 2.00*x);

                    path_str += ' Z ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width',1)
                .style('opacity','1.0')
                .style('fill',me.alliance['color_front'])
        ;

        me.icon_simple = me.ghostmark.append('text')
            .attr("x", -2*me.size)
            .attr("y", -me.size)
            .text(function(){
                let t  = ''
                if (me.alliance['icon_simple'] != ''){
                    t = me.alliance['icon_simple'];
                }
                return(t)
            })
            .style("font-family", "FadingSunsIcons")
            .style("font-size", (me.size*1.25)+"pt")
            .style("text-anchor", "middle")
            .style("fill", me.alliance['color_icon_fill'])
            .style("stroke", me.alliance['color_icon_stroke'])
            .style("stroke-width", "0.5pt")
            .style('opacity','1.0')
          ;


            me.icon_complex = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    if (me.alliance['icon_complex'] == 'kurgan'){
                        path_str += me.drawSticks(-12.0,-12,'7,0 -1,2 -3,0 2,1 -2,1 -2,-1 1,2 -2,0 0,-2 1,-1 -1,-1',3);
                        path_str += me.drawSticks(-12.0,-12,'-7,0 1,2 3,0 -2,1 2,1 2,-1 -1,2 2,0 0,-2 -1,-1 1,-1',3 );
                    }
                    if (me.alliance['icon_complex'] == 'gesar'){
                        path_str += me.drawSticks(-9.0,-9,'2,-1 1,1 -1,0 -1,1 0,1 -2,1 -2,-2',4);
                    }

                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke','#000')
                .style('stroke-width','0.5pt')
                .style('fill','#333')
            ;

        me.sex = me.ghostmark.append('path')
            .attr("d", function(){
                let x = me.size;
                let path_str = '';
                if (me.character['gender'] == 'male'){
                    path_str += me.drawSticks(0,0.75,'0.5,0.5 0,0.1 -0.5,-0.5 -0.5,0.5 0,-0.1 0.5,-0.5');
                }else{
                    path_str += me.drawSticks(0,1.25,'0.5,-0.5 0,-0.1 -0.5,0.5 -0.5,-0.5 0,0.1 0.5,0.5');
                }
                path_str += '  ';
                return(path_str);
            })
            .style('stroke',me.panel_fill)
            .style('stroke-width',1)
            .style('fill',me.panel_stroke)
        ;
        me.race_sym = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    let race = me.character['race'].split(' ')
                    if (race[0] == 'Urthish'){
                        path_str += me.drawSticks(0,0,'1,1 0,0.1 -1,-1 -1,1 0,-0.1 1,-1');
                    }
                    if (race[0] == 'Ur-Ukar'){
                        let ukar_str = '0.8,-0.8 ';
                        ukar_str +=    '-0.3,-0.3 0,0.1 0.2,0.2 ';
                        ukar_str +=    '-0.7,0.7 -0.7,-0.7 ';
                        ukar_str +=    '0.2,-0.2 0,-0.1 -0.3,0.3 ';
                        ukar_str +=    '0.8,0.8';
                        path_str += me.drawSticks(0,1,ukar_str);
                    }
                    if (race[0] == 'Ur-Obun'){
                        let obun_str = '0.8,-0.8 ';
                        obun_str +=    '0.3,0.3 0,-0.1 -0.3,-0.3 ';
                        obun_str +=    '-0.8,0.8 -0.8,-0.8 ';
                        obun_str +=    '-0.3,0.3 0,0.1 0.3,-0.3 ';
                        obun_str +=    '0.8,0.8';
                        path_str += me.drawSticks(0,1,obun_str);
                    }

                    if (race[0] == 'Vorox'){
                        path_str += me.drawSticks(-1,1,'1,-1 1,1');
                        path_str += me.drawSticks(-1,0,'1,1 1,-1');

                    }
                    if (race[0] == 'Kurgan'){
                        path_str += me.drawSticks(0,0,'0.6,0.6 0,0.1 -0.6,-0.6 -0.6,0.6 0,-0.1 0.6,-0.6');
                    }

                    path_str += '  ';
                    return(path_str);
                })
            .style('stroke',me.panel_fill)
            .style('stroke-width',1)
            .style('fill',me.panel_stroke)
        ;
        me.magic = me.ghostmark.append('path')
            .attr("d", function(){
                let x = me.size;
                let path_str = '';
                let small_square_str = '-0.05,0 0,0.1 0.1,0 0,-0.1 -0.05,0';
                let square_str = '-0.1,0 0,0.2 0.2,0 0,-0.2 -0.1,0';
                if (me.character['OCC_LVL'] > 0){
                    // Dark side marks
                    if (me.character['OCC_DRK'] > 2){
                        path_str += me.drawSticks(-1.75,-0.25,small_square_str);
                        path_str += me.drawSticks(-2.25,-0.25,small_square_str);
                    } else if (me.character['OCC_DRK'] > 0){
                        path_str += me.drawSticks(-2,-0.25,small_square_str);
                    }
                    // Occult category icon
                    if (me.character['occult'] == 'Theurgy'){
                        path_str += me.drawSticks(-2,0,'-0.1,0 0,0.2 -0.2,0 0,0.2 0.2,0 0,1 0.2,0 0,-1 0.2,0 0,-0.2 -0.2,0 0,-0.2 -0.1,0');
                    }else{
                        let str = ''
                        str += '-0.1,0 0,0.6 '
                        str += '-0.2,0 0,0.2 0.2,0 '
                        str += '0,0.2 '
                        str += '-0.2,0 0,0.2 0.2,0 '
                        str += '0,0.2 0.2,0 0,-0.2 '
                        str += '0.2,0 0,-0.2 -0.2,0 '
                        str += '0,-0.2 '
                        str += '0.2,0 0,-0.2 -0.2,0 '
                        str += '0,-0.6 -0.1,0'
                        path_str += me.drawSticks(-2,0,str);
                    }
                    // Power marks
                    if (me.character['OCC_LVL'] > 7){
                        path_str += me.drawSticks(-2,1.5,square_str);
                        path_str += me.drawSticks(-1.75,1.8,square_str);
                        path_str += me.drawSticks(-2.25,1.8,square_str);
                    }else if (me.character['OCC_LVL'] > 4){
                        path_str += me.drawSticks(-1.75,1.8,square_str);
                        path_str += me.drawSticks(-2.25,1.8,square_str);
                    } else {
                        path_str += me.drawSticks(-2,1.5,square_str);
                    }
                }
                path_str += '  ';
                return(path_str);
            })
            .style('stroke',me.panel_fill)
            .style('stroke-width',1)
            .style('fill',me.panel_stroke)
        ;

        me.ranking = me.ghostmark.append('path')
            .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    let small_stick = '-0.05,0 0,0.5 0.1,0 0,-0.5 -0.05,0';
                    if (me.character['ranking'] > 3){
                        path_str += me.drawSticks(0.0,1.75,small_stick);
                    }
                    if (me.character['ranking'] > 5){
                        path_str += me.drawSticks(0.25,1.75,small_stick);
                    }
                    if (me.character['ranking'] > 7){
                        path_str += me.drawSticks(-0.25,1.75,small_stick);
                    }
                    if (me.character['ranking'] > 9){
                        path_str += me.drawSticks(0.5,1.75,small_stick);
                    }
                    if (me.character['ranking'] > 11){
                        path_str += me.drawSticks(-0.5,1.75,small_stick);
                    }
                    if (me.character['ranking'] > 13){
                        path_str += me.drawSticks(0.75,1.75,small_stick);
                    }
                    if (me.character['ranking'] > 15){
                        path_str += me.drawSticks(-0.75,1.75,small_stick);
                    }
                    path_str += '  ';
                    return(path_str);
                })
            .style('stroke',me.panel_fill)
            .style('stroke-width',1)
            .style('fill',me.panel_stroke)
        ;
    }

    polarToCartesian(centerX, centerY, radius, angleInDegrees) {
        let angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
        return {
            x: centerX + (radius * Math.cos(angleInRadians)),
            y: centerY + (radius * Math.sin(angleInRadians))
        };
    }

    describeArc(x, y, radius, startAngle, endAngle){
        let me = this;
        let start = me.polarToCartesian(x, y, radius, endAngle);
        let end = me.polarToCartesian(x, y, radius, startAngle);
        let largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
        let d = [
            "M", start.x, start.y,
            "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
        ].join(" ");
        return d;
    }

    createName(){
        let me = this;
        let pi = Math.PI;
        let rad = 2.85;

        let arc_str = me.describeArc(0,0,me.size*2.85,-180,180);
        me.acronymPath = me.ghostmark.append('path')
            .attr('id','acropath')
            .attr("d",arc_str)
            .attr('transform','rotate('+135+')')
            .style("fill", 'transparent')
            .style("stroke", 'transparent')
            .style("stroke-width", '0')
            ;

        me.acronym = me.ghostmark.append('text')
                .attr("dx", 0)
                .attr("dy", 0)
                .style("fill", '#fff')
                .style("stroke", '#333')
                .style("stroke-width", "0.5pt")
                .style("font-family", "FatName")
                .style("font-size", (me.size/2)+"pt")
                .style("text-anchor", "middle")
                .style("opacity", "0.85")
                .append('textPath')
                .attr('xlink:href','#acropath')
                .text('-'+me.character["full_name"]+'-')
                .attr('startOffset','50%')
              ;


    }

    drawSticks(ox,oy,str,size){
        let me = this;
        let pts = str.split(' ');
        let p = '';
        let s = me.size;
        if (size != undefined){
            s = size;
        }
        let sep = ' l '
        p += ' M '+(ox*s)+','+(oy*s);
        _.forEach(pts, function(e, i) {
            let coords = e.split(',');
            p += sep+(coords[0]*s)+' '+(coords[1]*s);
            if (sep == ' l '){
                sep = ',';
            }

        })
        p += '  ';
        return(p);
    }

    addText(t,x,y){
        let me = this;
        let n = me.ghostmark.append('text')
            .attr("x", x*me.size)
            .attr("y", y*me.size)
            .text(function(){
                return(t)
            })
            .style("font-family", "Lato-Regular")
            .style("font-size", (me.size/2)+"pt")
            .style("text-anchor", "start")
            .style("fill", me.panel_fill)
            .style("stroke", me.panel_stroke)
            .style("stroke-width", "0.1pt")
        return(n);
    }

    perform(){
        let me = this;
        me.createLayout();
        me.createGhostMark();
        me.createName();
    }
}