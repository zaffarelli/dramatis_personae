/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Ghostmark {
    constructor(data) {
        let me = this;
        me.init(data);
    }

    init(data) {
        let me = this;
        me.size = 20;
        me.width = me.size * 6;
        me.height = me.size * 6;
        me.data = data;
        me.character = data['character'];
        me.alliance = data['alliance'];
        me.svg = d3.select('.mark #ghostmark_'+me.character['id'])
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
        //console.log(me.data)
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
                .style('stroke-width',(me.size/32)+'pt')
                .style('fill','#333')
        me.circ2 = me.layout.append('circle')
                .attr('cx',0)
                .attr('cy',0)
                .attr('r',me.size*2.5)
                .style('stroke',me.panel_stroke)
                .style('stroke-width',(me.size/16)+'pt')
                .style('fill','transparent')

        me.rect1 = me.layout.append('rect')
                .attr('x',-2*me.size)
                .attr('y',-2*me.size)
                .attr('width',me.size*4)
                .attr('height',me.size*4)
                .style('stroke',me.panel_stroke)
                .style('stroke-width','0.5pt')
                .style('fill','transparent')
        ;

        me.rect2 = me.layout.append('rect')
                .attr('x',-2*me.size)
                .attr('y',-2*me.size)
                .attr('width',me.size*4)
                .attr('height',me.size*4)
                .style('stroke',me.panel_stroke)
                .style('stroke-width','0.5pt')
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
                .style('stroke-width','0.5pt')
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
                .style('stroke-width','0.5pt')
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


        me.acronym = me.ghostmark.append('text')
            .attr("x", 0)
            .attr("y", -0.5*me.size)
            .text(function(){
                let t  = ''
                let words = me.character["full_name"].split(" ");
                _.each(words,function(e,i){
                    t += e[0];
                })
                //t += ' '+me.character["ranking"]
                return(t)
            })
            .style("font-family", "Lato-Regular")
            .style("font-size", (me.size*0.5)+"pt")
            .style("text-anchor", "middle")
            .style("fill", me.panel_fill)
            .style("stroke", me.panel_stroke)
            .style("stroke-width", "0.5pt")
            .style('opacity','0.9')
          ;

        me.sex = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    if (me.character['gender'] == 'male'){
                        path_str += me.drawSticks(-0.5,1,'0.5,-0.5 0.5,0.5');
                    }else{
                        path_str += me.drawSticks(-0.5,1,'0.5,0.5 0.5,-0.5');
                    }
                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','3pt')
                .style('fill','transparent')
        ;
        me.race_sym = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    let race = me.character['race'].split(' ')
                    if (race[0] == 'Urthish'){
                        path_str += me.drawSticks(-1,1,'1,-1 1,1');
                    }
                    if (race[0] == 'Ur-Ukar'){
                        path_str += me.drawSticks(-1,0,'1,1 1,-1');
                    }
                    if (race[0] == 'Ur-Obun'){
                        path_str += me.drawSticks(-1,1,'0,-1 1,1 1,-1 0,1');
                    }

                    if (race[0] == 'Vorox'){
                        path_str += me.drawSticks(-1,1,'1,-1 1,1');
                        path_str += me.drawSticks(-1,0,'1,1 1,-1');

                    }
                    if (race[0] == 'Kurgan'){
                        path_str += me.drawSticks(-1,1,'1,-1 1,1');
                        path_str += me.drawSticks(0,0,'0,1');

                    }

                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','3pt')
                .style('fill',"transparent")
        ;
        me.magic = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    if (me.character['OCC_LVL'] > 0){

                        if (me.character['OCC_DRK'] > 0){
                            path_str += me.drawSticks(-1.5,-0.25,'-0.33,0.33');
                        }else{
                            path_str += me.drawSticks(-1.5,-0.25,'0.33,0.33');
                        }
                        if (me.character['occult'] == 'Theurgy'){
                            path_str += me.drawSticks(-1.5,0.25,'0.33,0.33');
                        }else{
                            path_str += me.drawSticks(-1.5,0.25,'-0.33,0.33');
                        }
                        if (me.character['OCC_LVL'] > 4){
                          path_str += me.drawSticks(-1.5,-0.75,'0,0.5');
                        }
                    }
                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','3pt')
                .style('fill','transparent')
        ;

        me.ranking = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    if (me.character['ranking'] > 3){
                        path_str += me.drawSticks(1.5,-0.0,'0,0.50');
                    }
                    if (me.character['ranking'] > 5){
                        path_str += me.drawSticks(2.0,-0.0,'0,0.50');
                    }
                    if (me.character['ranking'] > 7){
                        path_str += me.drawSticks(2.5,-0.0,'0,0.50');
                    }
                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','3pt')
                .style('fill','transparent')
        ;

    }

    drawSticks(ox,oy,str){
        let me = this;
        let pts = str.split(' ');
        let p = '';
        let s = me.size;
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
        console.log('Layout done');
        me.createGhostMark();
        console.log('Ghostmark');
    }
}