from collector.models.character import Character

def rollcheck(source):
    all = Character.objects.filter(keyword='party')
    items = source.split(';')
    title = source
    txt = 'Attribute:'+items[0]+' Skill:'+items[1]+' DV:'+items[2]+' --> no options'
    d = []
    for c in all:
        skill = ''
        skill_value = 0
        stat = getattr(c,items[0])
        for s in c.skill_set.all():
            if s.skill_ref.reference == items[1]:
                skill = s.skill_ref.reference
                skill_value = s.value
            else:
                skill = 'no skill'
                skill_value = -2
        score = stat + skill_value
        ch = { 'name': c.full_name,'rid':c.rid,'stat':stat,'skill':items[1], 'value': skill_value, 'score':score }
        d.append(ch)

    print(d)
    sorted_list = sorted(d, key=lambda x:-x['score'])
    print(sorted_list)
    txt = f'For check {items[0]}+{items[1]} at DV {items[2]}'
    txt += '<ul>'
    cnt = 5
    for e in sorted_list:
        cnt -= 1
        txt +=  f'<li><em>{e["name"]}</em>:  {e["stat"]}+{e["value"]}=<strong>{e["score"]}</strong>.</li>'
        if cnt == 0:
            break;

    txt += '</ul>'
    return txt,title