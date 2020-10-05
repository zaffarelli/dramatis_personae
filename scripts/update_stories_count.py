from collector.models.character import Character

all = Character.objects.all()
for c in all:
    c.update_stories_count()
    c.save()
    if c.stories_count > 0:
        print("%s ---> %d" % (c.full_name, c.stories_count))


