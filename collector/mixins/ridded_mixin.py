from django.db import models


class RiddedMixin(models.Model):
    class Meta:
        abstract = True

    rid = models.CharField(default="", max_length=128, blank=True)

    def toRID(self, txt):
        """
        :param txt: the string from which the rid will be built
        :return: the rid, but just for information as it is stored here
        """
        if txt == '':
            self.rid = ''
        txt += f"__{type(self).__name__}"
        s = txt.lower()
        x = (s.replace(' ', '_').replace("'", '').replace('é', 'e') \
            .replace('è', 'e').replace('ë', 'e').replace('â', 'a') \
            .replace('ô', 'o').replace('"', '').replace('ï', 'i') \
            .replace('à', 'a').replace('-', '').replace('ö', 'oe') \
            .replace('ä', 'ae').replace('ü', 'ue').replace('ß', 'ss')
             .replace('ç', 'c').replace('?', '').replace('!', ''))
        self.rid = f'_{x.lower()}'
        print("Ridding:", txt, self.rid)
        return self.rid

    @classmethod
    def fromRID(klass,txt):
        candidates = klass.objects.filter(rid=txt)
        cnt = len(candidates)
        if cnt == 1:
            return candidates.first()
        elif cnt == 0:
            return None
        else:
            raise ReferenceError(f"Many instances of the rid found in the class.",cnt,txt,klass)
        return None



