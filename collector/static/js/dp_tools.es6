/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Ghostmark {
    constructor(data,oversize=3, intimacy=0, tgt='') {
        let me = this;
        me.intimacy = intimacy;
        me.tgt = tgt;
        me.oversize = 3;
        if (oversize !== 3){
            me.oversize = oversize;
        }
        me.opacity = 1;
        me.data = data;
    }
    init() {
        let me = this;
        me.size = 6;
        me.size = me.size * me.oversize;
        me.pen = me.size / 6;

        me.width = me.size * 6;
        me.height = me.size * 6;
        me.character = me.data['character'];
        me.alliance = me.data['alliance'];
        me.svg = d3.select('#'+me.tgt+'_'+me.character['id'])
            .append('svg')
            .attr('id','svg_'+me.tgt+'_'+me.character['id'])
            .attr("width", me.width)
            .attr("height", me.height)
            .style("background", "transparent")
            .style("opacity", me.opacity)
            .append('g');
        me.panel_stroke = "#888";
        me.panel_fill = "#CCC";
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

        if (me.intimacy > 0){
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

        me.traits_line_mark = me.ghostmark.append('line')
            .attr("x1", -10)
            .attr("y1", -24)
            .attr("x2", 10)
            .attr("y2", -24 )
            .style('stroke',"#888")
            .style('fill',  "#eee")
            .style('stroke-width',1)
        ;


        me.physical_mark = me.ghostmark.append('circle')
            .attr("cx", -10)
            .attr("cy", -24)
            .attr("r", 4)
            .style('stroke',function(d){
                return (me.character['physical']>=7 ? "#888":'transparent');
                })
            .style('fill',  function(d){
                return (me.character['physical']>=7 ? "#eee":'transparent');
                })
            .style('stroke-width',1)
        ;

        me.mental_mark = me.ghostmark.append('circle')
            .attr("cx", 0)
            .attr("cy", -24)
            .attr("r", 4)
            .style('stroke',function(d){
                return (me.character['mental']>=7 ? "#888":'transparent');
                })
            .style('fill',function(d){
                return (me.character['mental']>=7 ? "#eee":'transparent');
                })
            .style('stroke-width',1)
        ;

        me.combat_mark = me.ghostmark.append('circle')
            .attr("cx", 10)
            .attr("cy", -24)
            .attr("r", 4)
            .style('stroke',function(d){
                return (me.character['combat']>=7) ? "#888":'transparent';
                })
            .style('fill',function(d){
                return (me.character['combat']>=7) ? "#eee":'transparent';
                })
            .style('stroke-width',1)
        ;

        me.balanced_mark = me.ghostmark.append('circle')
            .attr("cx", 0)
            .attr("cy", -12)
            .attr("r", 3)
            .style('stroke','#888')
            .style('fill',function(d){
                return (me.character['balanced']) ? "#fc4":'transparent';
                })
            .style('stroke-width',1)
        ;


        me.tod_mark = me.ghostmark.append('text')
            .attr("x", 30)
            .attr("y", -30)
            .style('font-family',"FatName")
            .style('font-size',"10pt")
            .style('text-anchor',"middle")
            .style('stroke',"#111")
            .style('fill',"#eee")
            .style('stroke-width',"0.5pt")
            .text(function(d){
                return me.character['tod_count'];
            })
        ;

        me.fencing = me.ghostmark.append('text')
            .attr("x", 0)
            .attr("y", -38)
            .style('font-family',"FatName")
            .style('font-size',"10pt")
            .style('text-anchor',"middle")
            .style('stroke',"#111")
            .style('fill',"#eee")
            .style('stroke-width',"0.5pt")
            .text(function(d){
                if(me.character['fencing_league']){
                    return "F";
                }
                return " ";
            })
        ;


        me.race_sym = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    let race = me.character['race'].trim().split(' ')
                    let local_race = race[0]
//                     console.warn(me.character['race']);
                    if (local_race == 'Urthish'){
                        path_str += me.drawSticks(0,0,'1,1 0,0.1 -1,-1 -1,1 0,-0.1 1,-1');
                    }
                    if (local_race == 'Ur-Ukar'){
                        let ukar_str = '0.8,-0.8 ';
                        ukar_str +=    '-0.3,-0.3 0,0.1 0.2,0.2 ';
                        ukar_str +=    '-0.7,0.7 -0.7,-0.7 ';
                        ukar_str +=    '0.2,-0.2 0,-0.1 -0.3,0.3 ';
                        ukar_str +=    '0.8,0.8';
                        path_str += me.drawSticks(0,0.5,ukar_str);
                    }
                    if (local_race == 'Ur-Obun'){
                        let obun_str = '0.8,-0.8 ';
                        obun_str +=    '0.3,0.3 0,-0.1 -0.3,-0.3 ';
                        obun_str +=    '-0.8,0.8 -0.8,-0.8 ';
                        obun_str +=    '-0.3,0.3 0,0.1 0.3,-0.3 ';
                        obun_str +=    '0.8,0.8';
                        path_str += me.drawSticks(0,0.5,obun_str);
                    }

                    if (local_race == 'Vorox'){
                        let st = '0,-0.05 ';
                        st += '0.5,-0.5 0.25,0.25 0.25,-0.25 0.25,0.25 0.25,-0.25 0.5,0.5 ';
                        st += '0,0.05 ';
                        st += '-0.5,-0.5 -0.25,0.25 -0.25,-0.25 -0.25,0.25 -0.25,-0.25 -0.5,0.5 ';
                        path_str += me.drawSticks(-1,0.8,st);


                    }
                    if (local_race == 'Kurgan'){
                        let st = '';
                        st += '0,-0.05 ';
                        st += '0.6,-0.6 0.2,0.2 -0.2,0.2 -0.4,-0.4 0.4,-0.4 0.4,0.4 ';
                        st += '0.4,-0.4 0.4,0.4 -0.4,0.4 -0.2,-0.2 0.2,-0.2 0.6,0.6 ';
                        st += '0,0.05 ';
                        st += '-0.6,-0.6 -0.2,0.2 0.2,0.2 0.4,-0.4 -0.4,-0.4 -0.4,0.4 ';
                        st += '-0.4,-0.4 -0.4,0.4 0.4,0.4 0.2,-0.2 -0.2,-0.2 -0.6,0.6 ';
                        path_str += me.drawSticks(-1,0.5,st,20);
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
                        path_str += me.drawSticks(-2,0,'-0.1,0 0,0.2 -0.2,0 0,0.2 0.2,0 0,1 0.2,0 0,-1 0.2,0 0,-0.2 -0.2,0 0,-0.2 -0.1,0 ');
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
        }else{
            me.erzatz = me.ghostmark.append('circle')
                .attr("cx",0)
                .attr("cy",0)
                .attr("r",me.size)
                .style('stroke',me.panel_fill)
                .style('stroke-width',2)
                .style('fill',me.panel_stroke)
                ;
            me.erzatz_c = me.ghostmark.append('circle')
                .attr("cx",0)
                .attr("cy",0)
                .attr("r",me.size*0.8)
                .style('stroke',me.panel_fill)
                .style('stroke-width',2)
                .style('fill','#333')
                ;

        }
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
        console.log("Here we are")
        me.init();
        me.createLayout();
        me.createGhostMark();
        me.createName();
    }
    performShadow(){
        let me = this;
        me.opacity = 0.3;
        me.init();
        me.createLayout();
        me.createGhostMark();
        me.createName();

    }
}


class Logo {
    constructor(tgt,oversize=0,text) {
        let me = this;
        me.text = text;
        me.size = 5;
        if (oversize !== 0){
            me.size = me.size*oversize;
        }
        me.width = me.size * 3
        me.height = me.size * 4;
        me.dot_stroke = "#424";
        me.dot_fill = "#FC4";
        me.line_stroke = "#888";
        me.line_fill = "#aaaa";
        me.ox = me.size/4;
        me.oy = 3*me.size/4;
        me.init(tgt);
    }
    init(tgt) {
        let me = this;
        me.data = [
            {id:0,x:0,y:0},{id:1,x:me.size,y:0},{id:2,x:me.size*1.5,y:0},{id:3,x:me.size*2.5,y:0},
            {id:4,x:0,y:me.size},{id:5,x:me.size,y:me.size},{id:6,x:me.size*1.5,y:me.size},{id:7,x:me.size*2.5,y:me.size},
            {id:8,x:0,y:me.size*1.5},{id:9,x:me.size,y:me.size*1.5},{id:10,x:me.size*1.5,y:me.size*1.5},{id:11,x:me.size*2.5,y:me.size*1.5},
            {id:12,x:0,y:me.size*2.5},{id:13,x:me.size,y:me.size*2.5},{id:14,x:me.size*1.5,y:me.size*2.5},{id:15,x:me.size*2.5,y:me.size*2.5}
            ];
        me.links_data_dp = [
            {a:5,b:13},{a:12,b:8},{a:3,b:11},{a:14,b:2},  // verticals
            {a:13,b:12},{a:8,b:11},{a:2,b:3},  // horizontals
            {a:0,b:0},{a:1,b:1},{a:4,b:4},{a:15,b:15}     // dots
            ];


        me.links_data_fs = [
             {a:0,b:1},{a:0,b:4},{a:8,b:9},{a:8,b:12} // F
             ,{a:2,b:3},{a:2,b:6},{a:10,b:11}, {a:11,b:15},{a:14,b:15}  // S
            ,{a:5,b:5},{a:7,b:7},{a:10,b:10},{a:13,b:13}     // dots
            ];
        me.svg = d3.select(tgt)
            .append('svg')
            .attr("width", me.width)
            .attr("height", me.height)
            .style("background", "transparent")
            //.style("background", "red")
            .append('g');
    }
    drawBack(){
        let me = this;
        me.links = me.svg.append('g')
            .selectAll('link')
            .data(me.links_data_fs)
            .enter()
                .append('line')
                .attr('class','link fs')
                .attr('x1',function(d){
                    let c = me.data.find(x => x.id === d.a)
                    return c.x+me.ox;
                })
                .attr('y1',function(d){
                    let c = me.data.find(x => x.id === d.a)
                    return c.y+me.oy;
                })
                .attr('x2',function(d){
                    let c = me.data.find(x => x.id === d.b)
                    return c.x+me.ox;
                })
                .attr('y2',function(d){
                    let c = me.data.find(x => x.id === d.b)
                    return c.y+me.oy;
                })
                .style('fill',me.line_fill)
                .style('stroke',me.line_stroke)
                .style('stroke-linecap','round')
                .style('stroke-width',(me.size/3.5)+'pt')
                .style('opacity',.1)
            ;

        me.links_overlay = me.svg.append('g')
            .selectAll('link')
            .data(me.links_data_dp)
            .enter()
                .append('line')
                .attr('class','link dp')
                .attr('x1',function(d){
                    let c = me.data.find(x => x.id === d.a)
                    return c.x+me.ox;
                })
                .attr('y1',function(d){
                    let c = me.data.find(x => x.id === d.a)
                    return c.y+me.oy;
                })
                .attr('x2',function(d){
                    let c = me.data.find(x => x.id === d.b)
                    return c.x+me.ox;
                })
                .attr('y2',function(d){
                    let c = me.data.find(x => x.id === d.b)
                    return c.y+me.oy;
                })
                .attr('r',me.size/10)
                .style('fill',me.line_fill)
                .style('stroke',me.line_stroke)
                .style('stroke-linecap','round')
                .style('stroke-width',(me.size/3.5)+'pt')
                .style('opacity','0.9')

            ;


        me.dots = me.svg.append('g')
            .selectAll('dot')
            .data(me.data)
            .enter()
                .append('circle')
                .attr('class','dot')
                .attr('cx',function(d){
                    return d.x+me.ox;
                })
                .attr('cy',function(d){
                    return d.y+me.oy;
                })
                .attr('r',me.size/10)
                .style('fill',me.dot_fill)
                .style('stroke',me.dot_stroke)
                .style('stroke-width','1pt')
                .style('opacity','0.9')
                .on('mouseover', function(d){
                    d3.selectAll(".dp").style("opacity", 0.1);
                    d3.selectAll(".fs").style("opacity", 0.9);
                })
                .on('mouseout', function(d){
                    d3.selectAll(".dp").style("opacity", 0.9);
                    d3.selectAll(".fs").style("opacity", 0.1);
                })
            ;
    }
    drawText(){
        let me = this;
        if (me.text == 1){
            me.svg.append('text')
                .attr('x',me.ox+me.size*1.25)
                .attr('y',me.oy+me.size*(-0.25))
                .attr('font-family','FatName')
                .attr('text-anchor','middle')
                .style('font-size',(me.size/2.5)+'pt')
                .style('fill',me.line_fill)
                .style('stroke',me.dot_stroke)
                .style('stroke-width','0.5pt')
                .text("Fading Suns")
                ;
            me.svg.append('text')
                .attr('x',me.ox+me.size*1.25)
                .attr('y',me.oy+me.size*2.95)
                .attr('font-family','FatName')
                .attr('text-anchor','middle')
                .style('font-size',(me.size/4)+'pt')
                .style('fill',me.line_fill)
                .style('stroke',me.dot_stroke)
                .style('stroke-width','0.5pt')
                .text("Dramatis Personae")
                ;
            }
        }
    perform(){
        let me = this;
        me.drawBack();
        me.drawText();

    }

}