import html

from django.db import models
import json

from django.utils.safestring import SafeString


def RidField():
    return models.CharField(default="", max_length=200, blank=True)

def CypherRidField():
    return models.CharField(default="", max_length=50, blank=True)

class RiddedMixin(models.Model):
    """
    Mixin for rid computation. The ideal place to do so is inside the fix
    """
    class Meta:
        abstract = True



    rid = RidField()
    cypher_rid = CypherRidField()


    # 6CC1AAD28CBBF16BEB0B45

    @property
    def r_i_d(self):
        return SafeString(f"<tt style='color:cyan;'>{self.cypher_rid}</tt>")

    def toRID(self, txt, short=False, prefix="", cypher=False):
        """
        :param txt: the string from which the rid will be built
        :param short: default=False, only keep the first 3 characters of txt
        :param prefix: if blank, use class, else use the given string
        :param cypher: iuse blake2b on txt if true
        :return: the rid, but just for information as it is stored here
        """
        import hashlib
        if txt == '':
            self.rid = ''
        s = txt.lower()
        x = (s.replace(' ', '_').replace("'", '').replace('é', 'e')
            .replace('è', 'e').replace('ë', 'e').replace('â', 'a')
            .replace('ô', 'o').replace('"', '').replace('ï', 'i')
            .replace('à', 'a').replace('-', 'm').replace('ö', 'oe')
            .replace('ä', 'ae').replace('ü', 'ue').replace('ß', 'ss')
            .replace('ç', 'c').replace('?', '').replace('!', '')
            .replace('+', 'p').replace(')', '').replace('(', '')
            .replace('[', '').replace(']', '')
            .replace('(', '').replace(')', '')
            .replace('{', '').replace('}', '')
             )
        if short:
            tmp = f'_{x[:3].lower()}'
        else:
            tmp = f'_{x.lower()}'
        gfg = hashlib.blake2s(digest_size=5)
        gfg.update(bytes(tmp,encoding='utf-8'))
        #print(gfg.digest_size)
        self.cypher_rid = gfg.hexdigest().upper()
        if cypher:
            k = self.cypher_rid
        else:
            k = tmp
        if len(prefix)>0:
            self.rid = f"{prefix}"+k
        else:
            self.rid = f"{type(self).__name__}"+k
        self.rid = self.rid.upper()
        print("Ridding:", self.rid, self.cypher_rid)
        return self.rid


    @classmethod
    def fromRID(cls,txt):
        candidates = cls.objects.filter(rid=txt)
        cnt = len(candidates)
        # print(f"ERROR: {cnt} items found for [{txt}]")
        if cnt == 1:
            return candidates.first()
        elif cnt == 0:
            return None
        else:
            raise ReferenceError(f"Error: {cnt} instances of the rid {txt} found in for {cls}.")
        return None

    def to_json(self):
        from collector.utils.basic import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


