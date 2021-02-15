

class Ghostmark {
    constructor(data) {
        let me = this;
        me.init(data);
    }

    init(data) {
        let me = this;
        me.size = 20;
        me.width = me.size * 4;
        me.height = me.size * 9;
        me.data = data;
        me.character = JSON.parse(data['character'])
        me.alliance = JSON.parse(data['alliance'])
        me.svg = d3.select("div.jumpweb")
            .append('svg')
            .attr("width", me.size*20)
            .attr("height", me.size*10)
            .style("background", "black")
            .append('g');
        me.panel_stroke = "#888"
        me.panel_fill = "#CCC"
        me.mark = me.size;
        console.log(me.data)
    }

    createLayout(){
        let me = this;
        me.layout = me.svg.append('g')
            .attr('transform', function(d){
                return "translate("+(me.width)+",10)";
            })

        ;
        me.circ1 = me.layout.append('circle')
                .attr('cx',me.size*2)
                .attr('cy',me.size*2)
                .attr('r',me.size*2)
                .style('stroke',me.panel_stroke)
                .style('stroke-width',(me.size/8)+'pt')
                .style('fill','transparent')
        me.rect2 = me.layout.append('rect')
                .attr('x',0)
                .attr('y',0)
                .attr('width',me.size*4)
                .attr('height',me.size*4)
                .style('stroke',me.panel_stroke)
                .style('stroke-width','0.5pt')
                .style('fill','transparent')
        ;
        me.ghostmark = me.layout.append('g')
    }

    createGhostMark(){
        let me = this;
        me.front = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    path_str += ' M '+( 2.20*x)+','+( 0.50*x);
                    path_str += ' l '+( 1.5 *x)+" "+( 0.25*x);
                    path_str += ' c ';
                    path_str += ( 0.00*x)+' '+( 2.00*x)+',';
                    path_str += (-1.00*x)+' '+( 3.00*x)+',';
                    path_str += (-1.50*x)+' '+( 3.00*x);
                    path_str += ' Z ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','2.0pt')
                .style('fill',me.alliance['color_front'])
        ;
        me.back = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    path_str += ' M '+( 1.80*x)+','+( 0.50*x);
                    path_str += ' l '+(-1.50*x)+' '+( 0.25*x) ;
                    path_str += ' c ';
                    path_str += ( 0.00*x)+' '+(+2.00*x)+',';
                    path_str += ( 1.00*x)+' '+( 3.00*x)+',';
                    path_str += (+1.50*x)+' '+( 3.00*x);

                    path_str += ' Z ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','2.0pt')
                .style('fill',me.alliance['color_back'])
        ;
        me.sex = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                    if (me.character['gender'] == 'male'){
                        path_str += ' M '+(+2.00*x)+','+(+0.25*x);
                        path_str += ' l ';
                        path_str += ( 0.50*x)+' '+(+0.50*x)+',';
                        path_str += (-1.00*x)+' '+(-0.00*x)+',';
                        path_str += ( 0.50*x)+' '+(-0.50*x);
                    }else{
                        path_str += ' M '+(+2.00*x)+','+(+0.75  *x);
                        path_str += ' l ';
                        path_str += ( 0.50*x)+' '+(-0.50*x)+',';
                        path_str += (-1.00*x)+' '+(-0.00*x)+',';
                        path_str += ( 0.50*x)+' '+(+0.50*x);

                    }
                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','1.0pt')
                .style('fill',me.panel_fill)
        ;
        me.race_sym = me.ghostmark.append('path')
                .attr("d", function(){
                    let x = me.size;
                    let path_str = '';
                        path_str += ' M '+(+2.00*x)+','+(+1.00*x);
                        path_str += ' h '+(+0.25*x);
                        path_str += ' v '+(+2.00*x);
                        path_str += ' h '+(-0.50*x);
                        path_str += ' v '+(-2.00*x);
                        path_str += ' h '+(+0.25*x);
                        path_str += ' Z ';

                        path_str += ' M '+(+2.00*x)+','+(+1.00*x);
                        path_str += ' m '+(1.50*x)+' '+(-0.50*x);
                        path_str += ' l '+(-0.75*x)+' '+(+0.75*x);
                        path_str += ' , '+(+0.25*x)+' '+(+0.25*x);
                        path_str += ' , '+(+0.75*x)+' '+(-0.75*x);
                        path_str += ' , '+(-0.25*x)+' '+(-0.25*x);
                        path_str += ' Z ';

                        path_str += ' M '+(2.00*x)+','+(+1.00*x);
                        path_str += ' m '+(-1.50*x)+' '+(-0.50*x);
                        path_str += ' l '+(+0.75*x)+' '+(+0.75*x);
                        path_str += ' , '+(-0.25*x)+' '+(+0.25*x);
                        path_str += ' , '+(-0.75*x)+' '+(-0.75*x);
                        path_str += ' , '+(+0.25*x)+' '+(-0.25*x);
                        path_str += ' Z ';

                    if (me.character['race'] == 'Vorox'){
                        path_str += ' M '+(+2.00*x)+','+(+1.00*x);
                        path_str += ' m '+(0.75*x)+' '+(+1.00*x);
                        path_str += ' l '+(+0.75*x)+' '+(+0.75*x);
                        path_str += ' , '+(-0.25*x)+' '+(+0.25*x);
                        path_str += ' , '+(-0.75*x)+' '+(-0.75*x);
                        path_str += ' , '+(+0.25*x)+' '+(-0.25*x);
                        path_str += ' Z ';

                        path_str += ' M '+(2.00*x)+','+(+1.00*x);
                        path_str += ' m '+(-0.75*x)+' '+(+1.00*x);
                        path_str += ' l '+(-0.75*x)+' '+(+0.75*x);
                        path_str += ' , '+(+0.25*x)+' '+(+0.25*x);
                        path_str += ' , '+(+0.75*x)+' '+(-0.75*x);
                        path_str += ' , '+(-0.25*x)+' '+(-0.25*x);
                        path_str += ' Z ';


                    }

                    if (me.character['race'] == 'Ur-Ukar'){
                        path_str += ' M '+(+1.00*x)+','+(+3.25*x);
                        path_str += ' m '+(0.50*x)+' '+(+0.00*x);
                        path_str += ' l '+(+1.00*x)+' '+(+0.00*x);
                        path_str += ' , '+(+0.00*x)+' '+(+0.25*x);
                        path_str += ' , '+(-1.00*x)+' '+(-0.00*x);
                        path_str += ' , '+(+0.00*x)+' '+(-0.25*x);
                        path_str += ' Z ';




                    }

                    path_str += '  ';
                    return(path_str);
                })
                .style('stroke',me.panel_stroke)
                .style('stroke-width','1.0pt')
                .style('fill',me.panel_fill)
        ;


        me.strength = me.addText(me.character['OP'],4.2,0.5);
        me.name = me.addText(me.character['full_name'],4.2,1.5);
        me.race = me.addText(me.character['race'],4.2,2.5);
        me.alliance = me.addText(me.alliance['reference'],4.2,3.5);
        me.alliance = me.addText(me.character['species_name'],4.2,4.5);

    }

    drawSticks(ox,oy,str){
    }

    addText(t,x,y){
        let me = this;
        let n = me.ghostmark.append('text')
            .attr("x", x*me.size)
            .attr("y", y*me.size)
            .text(function(){
                return(t)
            })
            .style("font-family", "Lato")
            .style("font-size", (me.size/2)+"pt")
            .style("text-anchor", "start")
            .style("fill", me.panel_fill)
            .style("stroke", me.panel_stroke)
            .style("stroke-width", "0.1pt")
        return(n);
    }



    perform(){
        let me = this;
        me.createLayout()
        me.createGhostMark()
    }
}