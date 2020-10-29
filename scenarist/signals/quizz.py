from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scenarist.models.quizz import QuizzAnswer, QuizzQuestion
import hashlib
import logging


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=QuizzAnswer, dispatch_uid='fix_quizz_answer')
def fix_quizz_answer(sender, instance, **kwargs):
    instance.name = hashlib.sha3_256(bytes(f'{instance.text}{instance.question.num:03}', 'utf-8')).hexdigest()
    if instance.num == 0:
        all = QuizzAnswer.objects.filter(question=instance.question)
        instance.num = len(all)+1


@receiver(post_save, sender=QuizzAnswer, dispatch_uid='fix_quizz_question')
def fix_quizz_question(sender, instance, **kwargs):
    all = QuizzQuestion.objects.all()
    for qo in all:
        qo_aos = QuizzAnswer.objects.filter(question=qo)
        new_size = len(qo_aos)
        if qo.size != new_size:
            qo.size = new_size
            qo.save()


